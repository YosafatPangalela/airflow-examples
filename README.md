# Installation
1. run `./start.sh`
2. go to `localhost:8080` (default)
3. login (**username**: airflow, **pw**: airflow)
4. run the DAG (needs internet connection!)


================ SETUP CONNECTION IN AIRFLOW UI ================

1) dag: scrapping_msci_ftse_data

1.1) 
connection id: msci_data_api
connection type: HTTP
host: https://app2.msci.com/

1.2)
connection id: msci_data_path
connection type: File (path)
extra: {"path":"/opt/airflow/dags/scrapping_msci_data/files"}

1.3)
connection id: hive_conn
connection type: Hive Server 2 Thrift
host: hive-server
login: hive
password: hive
port: 10000

1.4)
connection id: spark_conn
connection type: Spark
host: spark://spark-master
port: 7077