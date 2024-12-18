from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ingestion.process_data import DataProcessor
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_storage_config():
    """Get storage configuration from environment"""
    return {
        'type': os.getenv('STORAGE_TYPE', 'minio'),
        'endpoint_url': os.getenv('STORAGE_ENDPOINT'),
        'access_key': os.getenv('STORAGE_ACCESS_KEY'),
        'secret_key': os.getenv('STORAGE_SECRET_KEY')
    }

def get_scheduled_configs(ds, **kwargs):
    """Get configurations that need to be processed based on schedule"""
    processor = DataProcessor(
        db_connection_string=os.getenv('POSTGRES_CONNECTION'),
        storage_config=get_storage_config()
    )
    try:
        return processor.get_scheduled_configs()
    finally:
        processor.dispose()

def process_config(config, **kwargs):
    """Process a single configuration"""
    processor = DataProcessor(
        db_connection_string=os.getenv('POSTGRES_CONNECTION'),
        storage_config=get_storage_config()
    )
    try:
        processor.process(config)
    finally:
        processor.dispose()

with DAG(
    'scheduled_ingestion',
    default_args=default_args,
    description='DAG for scheduled data ingestion',
    schedule_interval='*/15 * * * *',  # Every 15 minutes
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    get_configs = PythonOperator(
        task_id='get_configs',
        python_callable=get_scheduled_configs,
        provide_context=True,
    )
    
    def create_process_task(config):
        return PythonOperator(
            task_id=f'process_{config["config_id"]}',
            python_callable=process_config,
            op_kwargs={'config': config},
            provide_context=True,
        )
    
    # Dynamic task creation based on configs
    get_configs >> [create_process_task(config) for config in get_scheduled_configs(None)]