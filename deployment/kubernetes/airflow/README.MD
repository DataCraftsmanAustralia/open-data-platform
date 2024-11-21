helm repo add apache-airflow https://airflow.apache.org
helm search repo apache-airflow
helm show values apache-airflow/airflow

helm template --values values.yaml airflow apache-airflow/airflow --namespace airflow --create-namespace

kubectl create namespace airflow
kubectl apply -f all.yaml -n airflow

https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#webserver-secret-key