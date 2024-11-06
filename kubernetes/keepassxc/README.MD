kubectl create -f deployment.yaml
kubectl create -f pvc.yaml
kubectl create -f service.yaml

# TODO Need to fix storage issues with Rook-Ceph permissions.