import airflow
from airflow import DAG
from airflow.sensors.http_sensor import HttpSensor
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.email_operator import EmailOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

import os
import datetime
import urllib.request
from shutil import move
import pendulum
import sys

list_email = ["airflow@gmail.com"]
local_tz = pendulum.timezone("Asia/Jakarta")
default_args = {
            "owner": "Airflow",
            "start_date": datetime.datetime(2019, 1, 1, tzinfo=local_tz),
            "depends_on_past": False,
            "email_on_failure": True,
            "email_on_retry": False,
            "email": list_email,
            "retries": 1,
            "retry_delay": datetime.timedelta(minutes=5)
        }

dir_curr = os.path.dirname(os.path.abspath(__file__))
dir_out =  dir_curr + '//files//'
sys.path.append(dir_curr)
date_data = datetime.date.today() - datetime.timedelta(days = 1)
date_data_str = date_data.strftime("%Y%m%d")

def download_msci_data():
    # download MSCI data
    name_msci_file = 'indonesia_performance.xls'
    url = 'https://app2.msci.com/eqb/custom_indexes/indonesia_performance.xls'
    urllib.request.urlretrieve(url, dir_out + name_msci_file)

def copy_msci_data():
    import pandas as pd
    import numpy as np
    import datetime

    name_msci_file = 'indonesia_performance.xls'
    # read date from the file
    data = pd.read_excel(dir_out + name_msci_file)
    date_loc = np.where(data.values == 'Date')[0][0]
    date_data = data.iloc[date_loc + 4,0]
    date_data = date_data[date_data.index(',')+2:]
    date_data = datetime.datetime.strptime(date_data, '%B %d, %Y')
    date_data_str_loc = date_data.strftime('%Y%m%d')
    
    # make json file
    msci_loc = np.where(data.values == 'MSCI Code')[0][1]
    data_json = pd.read_excel(dir_out + name_msci_file, skiprows=msci_loc+1)

    data_res = pd.DataFrame()
    data_res['code'] = data_json['Reuters Code (RIC)']
    data_res['security_name'] = data_json['Security Name']
    data_res['price'] = data_json['Price']
    data_res['shares'] = data_json['Shares FIF Adjusted']
    data_res['weight'] = data_json['Weight%']/100
    data_res['currency'] = data_json['Currency']
    data_res['last_update'] = date_data.strftime('%Y-%m-%d')
    data_res = data_res.dropna()
    data_res['code'] = [x[:x.find(".")] for x in data_res['code']]
    data_res['security_name'] = [x.upper() for x in data_res['security_name']]
    data_res = data_res.sort_values(by=['code'])

    data_res.to_json(dir_out + 'data_msci.json',orient="records")

    # copy msci data
    dir_out_final = dir_out + date_data_str_loc + '//'
    if not os.path.exists(dir_out_final):
        os.makedirs(dir_out_final)

    data_out = dir_out_final + date_data_str_loc + ' MXID Data.xls'
    if not os.path.exists(data_out):
        move(dir_out + name_msci_file, data_out)

# time based on Asia/Jakarta
# see crontab.guru to see the format of schedule_interval
with DAG(dag_id="scrapping_msci_data", schedule_interval="30 0 * * 2-6", default_args=default_args, catchup=False) as dag:
    name_msci_file = 'indonesia_performance.xls'

    ### start collecting and processing MSCI data ###
    # Checking if msci data are available
    is_msci_conn_available = HttpSensor(
            task_id="is_msci_conn_available",
            method="GET",
            http_conn_id="msci_data_api",
            endpoint="eqb/custom_indexes/" + name_msci_file,
            poke_interval=5,
            timeout=20
    )

    # download msci data
    downloading_msci_data = PythonOperator(
        task_id="downloading_msci_data",
        python_callable=download_msci_data
    )

    # checking if the file containing msci data we want to observe is arrived
    is_msci_file_available = FileSensor(
            task_id="is_msci_file_available",
            fs_conn_id="msci_data_path",
            filepath=name_msci_file,
            poke_interval=5,
            timeout=20
    )

    # make json, copy and rename data
    copying_msci_data = PythonOperator(
        task_id="copying_msci_data",
        python_callable=copy_msci_data
    )

    # save msci json data
    saving_msci_data = BashOperator(
        task_id="saving_msci_data",
        bash_command="""
            hdfs dfs -mkdir -p /data && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/scrapping_msci_data/files/data_msci.json /data
        """
    )

    # create hdfs table for msci (if does not exist)
    creating_msci_data_table = HiveOperator(
        task_id="creating_msci_data_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS data_msci(
                code STRING,
                security_name STRING,
                price DOUBLE,
                shares DOUBLE,
                weight FLOAT,
                currency STRING,
                last_update DATE
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """
    )

    # use spark to insert msci hdfs table
    msci_processing = SparkSubmitOperator(
        task_id="msci_processing",
        application="/opt/airflow/dags/scrapping_msci_data/scripts/msci_processing.py",
        conn_id="spark_conn",
        verbose=False
    )

    is_msci_conn_available >> downloading_msci_data >>  is_msci_file_available  >> copying_msci_data
    copying_msci_data >> saving_msci_data >> creating_msci_data_table >> msci_processing