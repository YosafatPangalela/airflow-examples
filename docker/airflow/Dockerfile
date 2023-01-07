# Base Image
FROM spark-base:latest
LABEL maintainer="YPangalela"

# Arguments that can be set with docker build
ARG AIRFLOW_VERSION=2.5.0
ARG AIRFLOW_HOME=/opt/airflow

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Install dependencies and tools
RUN apt-get update -y && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    chromium \
    python3-dev \
    wget \
    libczmq-dev \
    curl \
    libssl-dev \
    git \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libffi-dev libpq-dev \
    freetds-bin build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    gcc \
    vim \
    netcat \
    && apt-get autoremove -yqq --purge && apt-get clean

# Upgrade pip
# Create airflow user 
# Install apache airflow with subpackages
RUN pip install --upgrade "pip==22.3.1" && \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install apache-airflow==${AIRFLOW_VERSION} --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.7.txt && \
    pip install apache-airflow[crypto,celery,postgres,hdfs,hive,jdbc,mysql,redis,ssh,slack]==${AIRFLOW_VERSION} --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.7.txt && \
    pip install apache-airflow-providers-apache-spark==4.0.0

RUN pip install --no-cache-dir \
  python-dotenv==0.20.0 \
  selenium==4.2.0 \
  webdriver-manager==3.5.3 \
  psycopg2==2.7.7 \
  joblib==1.1.0 \
  xlrd==2.0.1 \
  pdblp==0.1.8

# Copy the airflow.cfg file (config)
#COPY ./config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# Set the owner of the files in AIRFLOW_HOME to the user airflow
RUN chown -R airflow: ${AIRFLOW_HOME}

# Copy the entrypoint.sh from host to container (at path AIRFLOW_HOME)
COPY ./start-airflow.sh ./start-airflow.sh

# Set the entrypoint.sh file to be executable
RUN chmod +x ./start-airflow.sh

# Set the username to use
USER airflow

# Create the folder dags inside $AIRFLOW_HOME
RUN mkdir -p ${AIRFLOW_HOME}/dags

# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080

# Execute start-airflow.sh
CMD [ "./start-airflow.sh" ]

    