# Official Helm Chart:
https://superset.apache.org/docs/installation/kubernetes#environment-variables

helm repo add superset https://apache.github.io/superset
helm search repo superset

# Modify the values.yaml to suit your deployment
https://github.com/apache/superset/blob/master/helm/superset/values.yaml

# Generate SECRET_KEY
openssl rand -base64 42

Uncomment the values.yaml where it has the following and add your generated key
secret: |
    SECRET_KEY = ''

# Create a template based on the values (or you can just do helm install, I like to keep my files)
helm template --values values.yaml superset superset/superset

# Deploy redis
kubectl apply -f application.yaml
kubectl apply -f configmap.yaml
kubectl apply -f headless-svc.yaml
kubectl apply -f health-configmap.yaml
kubectl apply -f scripts-configmap.yaml
kubectl apply -f service.yaml
kubectl apply -f serviceaccount.yaml

# Deploy Postgres
kubectl apply -f svc-headless.yaml
kubectl apply -f secrets.yaml
kubectl apply -f svc.yaml
kubectl apply -f statefulset.yaml

# Deploy Superset
kubectl apply -f secret-env.yaml
kubectl apply -f secret-superset-config.yaml
kubectl apply -f service.yaml
kubectl apply -f deployment-worker.yaml
kubectl apply -f deployment.yaml
kubectl apply -f init-job.yaml