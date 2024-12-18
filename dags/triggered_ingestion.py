from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ingestion.process_data import DataProcessor
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def process_triggered_data(config, **kwargs):
    """Process data based on triggered configuration"""
    processor = DataProcessor(
        db_conn_id=Variable.get('database_connection_id', 'postgres_default'),
        storage_conn_id=Variable.get('storage_connection_id', 'storage_default')
    )
    try:
        processor.process(config)
    finally:
        processor.dispose()

with DAG(
    'triggered_ingestion',
    default_args=default_args,
    description='DAG for triggered data ingestion',
    schedule_interval=None,  # Triggered manually
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    process_data = PythonOperator(
        task_id='process_data',
        python_callable=process_triggered_data,
        provide_context=True,
        # Config will be provided when triggering the DAG
        op_kwargs={'config': "{{ dag_run.conf }}"}
    ) 