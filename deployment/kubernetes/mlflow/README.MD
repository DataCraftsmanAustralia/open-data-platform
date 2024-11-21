# Deploy postgres as per Postgres README

## Log into S3 Browser using keys below

kubectl -n rook-ceph get secret rook-ceph-object-user-my-store-my-user -o jsonpath='{.data.AccessKey}' | base64 --decode
kubectl -n rook-ceph get secret rook-ceph-object-user-my-store-my-user -o jsonpath='{.data.SecretKey}' | base64 --decode

## Create a bucket named mlartifacts in S3 Browser

# base64 encode keys and update secret.yaml
echo -n "<AWS_ACCESS_KEY_ID>" | base64
echo -n "<AWS_SECRET_ACCESS_KEY>" | base64

# Deploy MLflow Tracking Server
kubectl apply -f secret.yaml
kubectl apply -f service.yaml
kubectl apply -f deployment.yaml