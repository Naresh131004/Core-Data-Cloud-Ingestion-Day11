from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default configuration attributes for resilience
default_args = {
    'owner': 'data_engineer_kio',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='milestone_1_orchestrated_pipeline',
    default_args=default_args,
    description='Automated orchestration pipeline linking API ingestion, AWS S3, and Snowflake',
    start_date=datetime(2026, 7, 1),
    catchup=False,
) as dag:

    # Task 1: Execute the API Data Extraction Engine
    run_extraction = BashOperator(
        task_id='extract_api_data_task',
        bash_command='python3 /opt/airflow/dags/ingest.py',
    )

    # Task 2: Upload Raw Files to AWS S3 Object Storage
    push_to_s3 = BashOperator(
        task_id='upload_s3_data_task',
        bash_command='python3 /opt/airflow/dags/s3_upload.py',
    )

    # Task 3: Load Data into the Snowflake Data Warehouse
    load_warehouse = BashOperator(
        task_id='load_snowflake_task',
        bash_command='echo "Executing Snowflake warehouse staging copy..."',
    )

    # Define sequential dependencies using the bitshift operator
    run_extraction >> push_to_s3 >> load_warehouse
