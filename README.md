# Open Data Platform

This Repo is a guide to building the Open Data Platform in Ubuntu using Open Source Software in both Docker and Kubernetes.

![Open Data Platform ](https://github.com/DataCraftsmanAustralia/open-data-platform/blob/main/images/opendataplatform.png)

TLS is out of scope. Use nginx or mount certs to your deployment, or use a cloud load balancer or whatever suits your needs. Will add it one day.

# Data Analytics Use Case Flow Chart
![Data Analytics Use Case Flow Chart ](https://github.com/DataCraftsmanAustralia/open-data-platform/blob/main/images/usecaseflowdiagram.png)

# Data Architecture
![Data Architecture ](https://github.com/DataCraftsmanAustralia/open-data-platform/blob/main/images/dataarchitecture.png)

# Big Data Architecture
![Big Data Architecture ](https://github.com/DataCraftsmanAustralia/open-data-platform/blob/main/images/bigdataarchitecture.png)

# System Architecture (WIP)
![System Architecture (WIP) ](https://github.com/DataCraftsmanAustralia/open-data-platform/blob/main/images/systemarchitecture.png)

# dbt CI/CD Pipeline
![dbt CI/CD Pipeline ](https://github.com/DataCraftsmanAustralia/open-data-platform/blob/main/images/dbt-cicd.png)


# Roadmap

1. [ ] Data Lakehouse Architecture Deployment with Dremio
2. [ ] Data Streaming Deployment with Kafka, Flink / Druid
3. [ ] RAG Architecture Deployment
4. [ ] Apache airflow data pipeline. Maybe swap to a dlt based approach. https://github.com/dlt-hub/dlt
5. [ ] Develop Flask front end integration platform.