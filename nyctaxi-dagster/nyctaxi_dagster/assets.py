
import pandas as pd
from dagster import asset,MetadataValue
import requests


###define Taxi data assets

@asset(group_name='raw',kinds={"parquet", "pandas"})
def taxi_rides(context):
    """Asset downloads yellow taxi tripdata"""
    rides = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet')

    context.add_output_metadata(
        {
            "preview": MetadataValue.md(rides.head().to_markdown()),
            "description": MetadataValue.md(rides.describe().to_markdown()),
            "num_rows": len(rides)
        }
    )

    return rides


@asset(group_name='raw',key_prefix='raw',io_manager_key="postgres_io_manager",kinds={"pandas", "postgres"},metadata={"table":'rides'})
def rides(context,taxi_rides):
    """Remove rides without passengers"""
    filtered_rides = taxi_rides[taxi_rides['passenger_count'] >= 1][:500000] ##filter for 500k rows for this small project
    return filtered_rides
