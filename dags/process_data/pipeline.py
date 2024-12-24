from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
import dlt
from dlt.sources.filesystem import filesystem
from dlt.common.destination import Destination
from config_parser import load_and_validate_config
import os
from source import get_dlt_source, apply_column_transformations
from destination import get_dlt_destination

# Define paths to config and schema files (relative to the dags folder)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'pipeline_config.json')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'pipeline_schema.json')

def load_config():
    config = load_and_validate_config(CONFIG_PATH, SCHEMA_PATH)
    return config

def run_dlt_pipeline(source, destination, config):
    pipeline_name = config.get("pipeline_name", "data_pipeline")
    dataset_name = config.get("dataset_name", "data_dataset")
    behavior = config["destination"]["behavior"]

    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination=destination,
        dataset_name=dataset_name,
    )

    load_info = pipeline.run(
        source,
        write_disposition=behavior,
        table_name=config["destination"]["table"]
    )

    print(load_info)