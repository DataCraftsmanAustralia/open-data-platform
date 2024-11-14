# Deploy yamls
Change the localhost references throughout.

kubectl apply -f ./monitoring/cadvisor
kubectl apply -f ./monitoring/grafana
kubectl apply -f ./monitoring/node-exporter
kubectl apply -f ./monitoring/prometheus

login to grafana with admin/admin
Change password.
Change the localhost references throughout.
Add the promethus server as a data source.
`http://localhost:30003`
Add the monitoring jsons as dashboards, ensuring the data source is selected.
