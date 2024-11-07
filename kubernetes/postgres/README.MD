# Base64 encode your username and password
## Linux
echo -n "your_password" | base64

# Windows
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your_password"))

# Deploy
kubectl apply -f service.yaml
kubectl apply -f secret.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml