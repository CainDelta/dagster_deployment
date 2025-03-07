from dagster import Definitions, load_assets_from_modules,AutomationConditionSensorDefinition,AssetSelection
from . import assets
from .postgres_io_manager import PostgresIOManager
import os
from .dbt_assets import dbt_resource
from . import dbt_assets
from dotenv import load_dotenv


load_dotenv()



##load core assets
core_assets = load_assets_from_modules([assets])
dbt_asset = load_assets_from_modules([dbt_assets])
all_assets = [*core_assets,*dbt_asset]


###LOAD DB CREDENTIALS
postgres_credentials = {
    "user": os.environ.get("user"),
    "password" : os.environ.get("password"),
    "host" : os.environ.get("host"),
    "database" : os.environ.get("database")
}

###AUTOMATION CONDITION SENSOR
auto_materialize_sensor = AutomationConditionSensorDefinition(
    "taxi_auto_materialize_sensor",
    target=AssetSelection.all(include_sources=True),
    minimum_interval_seconds=60 * 2,
)


defs = Definitions(
    assets=all_assets,
    resources={"postgres_io_manager":PostgresIOManager(**postgres_credentials),
              "dbt" : dbt_resource},
    sensors=[auto_materialize_sensor]
)
