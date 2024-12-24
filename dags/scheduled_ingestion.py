from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from dags.process_data.pipeline import (
    load_config,
    run_dlt_pipeline
)
from dags.process_data.source import (
    get_dlt_source,
    apply_column_transformations
)

from dags.process_data.destination import (
    get_dlt_destination
)

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
    dag_id='scheduled_data_pipeline',
    default_args=default_args,
    description='A scheduled data pipeline using dlt',
    schedule_interval=timedelta(days=1),  # Run daily, adjust as needed
    start_date=days_ago(2),
    catchup=False,  # Set to True if you want to backfill
    tags=['dlt', 'data-pipeline', 'scheduled'],
) as dag:
    # Tasks
    load_config_task = PythonOperator(
        task_id='load_config',
        python_callable=load_config,
    )

    create_dlt_source_task = PythonOperator(
        task_id='create_dlt_source',
        python_callable=get_dlt_source,
        op_kwargs={'config': '{{ ti.xcom_pull(task_ids="load_config") }}'},
    )

    create_dlt_destination_task = PythonOperator(
        task_id='create_dlt_destination',
        python_callable=get_dlt_destination,
        op_kwargs={'config': '{{ ti.xcom_pull(task_ids="load_config") }}'},
    )

    transform_resource_task = PythonOperator(
        task_id='transform_resource',
        python_callable=apply_column_transformations,
        op_kwargs={
            'resource': '{{ ti.xcom_pull(task_ids="create_dlt_source") }}',
            'config': '{{ ti.xcom_pull(task_ids="load_config") }}',
        },
    )

    run_pipeline_task = PythonOperator(
        task_id='run_dlt_pipeline',
        python_callable=run_dlt_pipeline,
        op_kwargs={
            'source': '{{ ti.xcom_pull(task_ids="transform_resource") }}',
            'destination': '{{ ti.xcom_pull(task_ids="create_dlt_destination") }}',
            'config': '{{ ti.xcom_pull(task_ids="load_config") }}',
        },
    )

    load_config_task >> create_dlt_source_task >> create_dlt_destination_task >> transform_resource_task >> run_pipeline_task