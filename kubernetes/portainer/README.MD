https://raw.githubusercontent.com/portainer/k8s/master/deploy/manifests/portainer/portainer.yaml

Copy this folder to the machine and run kubectl apply -f /home/user/kubernetes/portainer/deployment.yaml etc

# Deploy
kubectl apply -f namespace.yaml
kubectl apply -f serviceaccount.yaml
kubectl apply -f rbac.yaml
kubectl apply -f service.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml