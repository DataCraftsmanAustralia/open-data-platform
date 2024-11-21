# Deploy
kubectl apply -f service.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml

# Logging in - get the token
kubectl logs <podname> 

This will work but if you want to get the password currently you need to get the token from the server each time you restart it. See the following to setup a proper password, can probably mount it in the volume or something idk.
https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html