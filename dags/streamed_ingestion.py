from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from datetime import timedelta
from dags.process_data.pipeline import (
    load_config
)
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='streaming_data_pipeline',
    default_args=default_args,
    description='A streaming data pipeline using dlt',
    schedule_interval=timedelta(minutes=5),  # Check for new files every 5 minutes
    start_date=days_ago(2),
    catchup=False,
    tags=['dlt', 'data-pipeline', 'streaming'],
) as dag:

    # Task to load and validate the configuration
    load_config_task = PythonOperator(
        task_id='load_config',
        python_callable=load_config,
    )

    # Sensor to watch for new files in the config directory
    # Note: This assumes your config files are updated externally
    wait_for_config_update = FileSensor(
        task_id='wait_for_config_update',
        filepath='/opt/airflow/config/pipeline_config.json',  # Adjust path if needed
        poke_interval=30,  # Check every 30 seconds
        timeout=60 * 5,  # Timeout after 5 minutes
        mode='poke',  # Use 'poke' mode for continuous monitoring
    )

    # Trigger the triggered_data_pipeline DAG
    trigger_pipeline = TriggerDagRunOperator(
        task_id='trigger_pipeline',
        trigger_dag_id='triggered_data_pipeline',  # Ensure this matches the ID of your triggered DAG
        wait_for_completion=True,  # Wait for the triggered DAG to complete before proceeding
        reset_dag_run=True,  # Reset the triggered DAG run each time
        trigger_rule='all_success',  # Trigger only if all upstream tasks have succeeded
    )

    # Define the task sequence
    load_config_task >> wait_for_config_update >> trigger_pipeline