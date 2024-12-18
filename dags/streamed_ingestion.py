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

def get_stream_configs():
    """Get configurations for stream processing"""
    processor = DataProcessor(
        db_connection_string=os.getenv('POSTGRES_CONNECTION'),
        storage_config=get_storage_config()
    )
    try:
        return processor.get_stream_configs()
    finally:
        processor.dispose()

def process_stream(config, **kwargs):
    """Process streaming data for a given configuration"""
    processor = DataProcessor(
        db_connection_string=os.getenv('POSTGRES_CONNECTION'),
        storage_config=get_storage_config()
    )
    
    try:
        # Modify config for streaming context
        stream_config = config.copy()
        stream_config['source']['key'] = f"{config['source']['key_prefix']}/{kwargs['ds']}"
        
        processor.process(stream_config)
    finally:
        processor.dispose()

with DAG(
    'streamed_ingestion',
    default_args=default_args,
    description='DAG for streaming data ingestion',
    schedule_interval='@hourly',  # Process stream data hourly
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    get_configs = PythonOperator(
        task_id='get_configs',
        python_callable=get_stream_configs,
    )
    
    def create_stream_task(config):
        return PythonOperator(
            task_id=f'process_stream_{config["config_id"]}',
            python_callable=process_stream,
            op_kwargs={'config': config},
            provide_context=True,
        )
    
    # Dynamic task creation based on stream configs
    get_configs >> [create_stream_task(config) for config in get_stream_configs()]