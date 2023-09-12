# connect to vm via ssh
ssh -i airflow-ec2.pem ubuntu@54.246.14.105

# update all packages
sudo apt update

# install python
sudo apt install python3-pip

# install sqlite
sudo apt install sqlite3

# install other dependencies
sudo apt-get install libpq-dev

# update the aws cli
pip3 install --upgrade awscli

# install virtual env for python
sudo pip3 install virtualenv

# create virtual environment
virtualenv venv

# activate env
source venv/bin/activate

# install airflow
pip install "apache-airflow[postgres]==2.5.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.7.txt"

# install more dependecis for airdlow
pip install pandas apache-airflow-providers-snowflake==2.1.0 snowflake-connector-python snowflake-sqlalchemy==1.2.5 # install latset version of Snowflake connector

# download other dependencies
pip  install pyarrow fastparquet


# initalize airflow
airflow db init

# install psql for airflow
sudo apt-get install postgresql postgresql-contrib


# switch to postgres user
sudo -i -u postgres

# enter psql cli
psql


# sql stuff
# CREATE DATABASE airflow;
# CREATE USER airflow WITH PASSWORD 'airflow';
# GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
# exit

cd airflow

sed -i 's#sqlite:////home/ubuntu/airflow/airflow.db#postgresql+psycopg2://airflow:airflow@localhost/airflow#g' airflow.cfg
sed -i 's#SequentialExecutor#LocalExecutor#g' airflow.cfg


airflow db init


airflow users create -u airflow -f airflow -l airflow -r Admin -e airflow@gmail.com


mkdir /home/ubuntu/dags




vim airflow.cfg

airflow db init

airflow webserver

source venv/bin/activate
airflow scheduler




scp -i airflow-ec2.pem news_fetcher_etl.py ubuntu@34.252.12.48:/home/ubuntu/dags

scp -i airflow-ec2.pem etl_news_datapipeline.py ubuntu@34.252.12.48:/home/ubuntu/dags

scp -i airflow-ec2.pem credential.py ubuntu@34.252.12.48:/home/ubuntu/dags
