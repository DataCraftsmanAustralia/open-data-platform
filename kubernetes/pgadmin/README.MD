# Base64 encode your PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD
## Linux
echo -n "your_password" | base64

# Windows
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your_password"))

# Deploy
kubectl apply -f service.yaml
kubectl apply -f secret.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml