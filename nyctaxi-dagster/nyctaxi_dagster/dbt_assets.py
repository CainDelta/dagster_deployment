import json
import os
import pathlib
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets
from dagster import AutomationCondition,AssetSelection,OpExecutionContext


##change directory to dagster
path = f'{pathlib.Path(__file__).parent.resolve()}/nyctaxi_dbt'


DBT_PROJECT_DIR = path
profiles_dir = path + '/config'

dbt_resource = DbtCliResource(
    project_dir=path,
    profiles_dir = profiles_dir
)
dbt_parse_invocation = dbt_resource.cli(["parse"], manifest={}).wait()
dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    """Custom transalator to pick out folder name in dbt as dagster group name """
    @classmethod
    def get_group_name(cls, dbt_resource_props):
        group = dbt_resource_props.get("original_file_path", {}).split('/')[1]

        if group.endswith('.sql'):
            return "monitoring"
        else:
            return group


    @classmethod
    def get_automation_condition(cls,dbt_resource_props):
        automation_condition  = AutomationCondition.eager().all_deps_match(AutomationCondition.missing() | AutomationCondition.will_be_requested() |(AutomationCondition.newly_updated() & ~AutomationCondition.newly_requested()) )
        return automation_condition



@dbt_assets(manifest=dbt_manifest_path,dagster_dbt_translator=CustomDagsterDbtTranslator())
def dbt_project_assets(context: OpExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
