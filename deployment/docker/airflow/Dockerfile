FROM apache/airflow:2.7.1

USER root

# Install system dependencies for Oracle client
RUN apt-get update \
    && apt-get install -y libaio1 wget unzip \
    && mkdir -p /opt/oracle \
    && cd /opt/oracle \
    && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
    && unzip instantclient-basiclite-linuxx64.zip \
    && rm instantclient-basiclite-linuxx64.zip \
    && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

USER airflow

# Copy requirements file
COPY requirements.txt /opt/airflow/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Set environment variables for Oracle client
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1:$LD_LIBRARY_PATH
ENV ORACLE_HOME=/opt/oracle/instantclient_21_1
ENV PATH=$PATH:$ORACLE_HOME

# Copy DAGs and other files
COPY dags/ /opt/airflow/dags/ 