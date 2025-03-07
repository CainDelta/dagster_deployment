from dagster import IOManager, ConfigurableIOManager,io_manager,MetadataValue,InputContext,OutputContext
from contextlib  import contextmanager
from sqlalchemy import create_engine
import os
import pandas as pd


@contextmanager
def connect_postgres(credentials):

    connection = None
    try:
        user=credentials['user']
        password=credentials['password']
        host=credentials['host']
        database=credentials['database']
        connection = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
        yield connection

    except (Exception) as error:
        print("Error while connecting to Postgres", error)
        raise error
    finally:
        if (connection):
            connection.dispose()



class PostgresIOManager(ConfigurableIOManager):

    user: str
    password: str
    database: str
    host: str

    @property
    def _config(self):
        return self.dict()

    def handle_output(self, context, obj):
        table = context.metadata["table"]
        # schema = context.metadata["schema"]
        # asset_key = context.asset_key
        # table  = asset_key.path[-1]
        cols = [x.lower() for x in list(obj)] ###lowecase all columns
        obj.columns = cols

        with connect_postgres(credentials=self._config) as conn:
            obj.to_sql(name=table, con=conn, if_exists='replace')

        ##add output metadata
        context.add_output_metadata(
            {
                "preview": MetadataValue.md(obj.head().to_markdown()),
                "description": MetadataValue.md(obj.describe().to_markdown()),
                "num_rows": len(obj)
            }
        )


    def load_input(self, context):
        asset_key = context.asset_key
        table  = asset_key.path[-1]
        with connect_postgres(credentials=self._config) as conn:
            table =  pd.read_sql_query(f'select * from {table}',conn)
