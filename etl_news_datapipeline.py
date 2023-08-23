import logging
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook

from datetime import datetime, timedelta
from news_fetcher_etl import runner


# set logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# set default args
default_args = {
    'owner': 'Tomiwa Famutimi',
    'start_date': days_ago(0),
    'email': ['tb.famutimi@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delays': timedelta(minutes=1)
}


dag = DAG(
    'snowflake_automation_dag',
    default_args=default_args,
    description = 'ETL pipeline that pulls data from news api to local block storage to s3 to snowflake',
    schedule_interval=None
)


with dag:

    extract_news_info = PythonOperator(
        task_id = 'extract_news_info',
        python_callable = runner,
        dag = dag,
    )


    move_file_to_s3 = BashOperator(
        task_id = 'move_file_to_s3',
        bash_command = 'aws s3 mv {{ ti.xcom_pull("extract_news_info") }} s3://detomfam-news-data-lake',
        dag = dag,
    )


    