Follow this to setup a Rook-Ceph storage cluster. Make sure you have RAW disks on each VM for Rook-Ceph to acquire.

# Rook-Ceph
https://computingforgeeks.com/how-to-deploy-rook-ceph-storage-on-kubernetes-cluster/

cd ~/
git clone --single-branch --branch release-1.15 https://github.com/rook/rook.git
cd rook/deploy/examples/

Go into the operator.yaml file and make sure the following is set to true, by default it is false:
- name: ROOK_HOSTPATH_REQUIRES_PRIVILEGED
    value: "true"

kubectl create -f crds.yaml
kubectl create -f common.yaml
kubectl create -f operator.yaml
watch kubectl -n rook-ceph get pod
kubectl config set-context --current --namespace rook-ceph

# Create Cluster
kubectl create -f cluster.yaml
watch kubectl get all -n rook-ceph
kubectl get pods -n rook-ceph -w
kubectl -n rook-ceph get cephcluster

# Ceph Toolbox
kubectl apply -f toolbox.yaml
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- bash
ceph status
ceph osd status
ceph df
rados df


# NFS Storage
vi filesystem.yaml
kubectl create -f filesystem.yaml
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- bash
ceph fs ls
ceph osd lspools
exit
vi csi/cephfs/storageclass.yaml
kubectl create -f csi/cephfs/storageclass.yaml
kubectl get sc
kubectl create -f csi/cephfs/pvc.yaml
kubectl get pvc
kubectl create -f csi/cephfs/pod.yaml
kubectl get pods

# Block Storage
kubectl create -f csi/rbd/storageclass.yaml
kubectl create -f csi/rbd/pvc.yaml
kubectl get sc
kubectl get pvc rbd-pvc


kubectl get svc -n rook-ceph
kubectl port-forward service/rook-ceph-mgr-dashboard 8443:8443 -n rook-ceph

# Get password - user is admin by default
kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo
vi dashboard-external-https.yaml
kubectl create -f dashboard-external-https.yaml
kubectl -n rook-ceph get service rook-ceph-mgr-dashboard-external-https

Access the site at:
https://yourvmipaddress:30638<the port number your nodeport created>


# Object Storage
kubectl create -f object.yaml
kubectl -n rook-ceph get pod -l app=rook-ceph-rgw

kubectl create -f storageclass-bucket-delete.yaml
kubectl create -f object-bucket-claim-delete.yaml
kubectl create -f rgw-external.yaml
kubectl create -f object-user.yaml

kubectl -n rook-ceph get service rook-ceph-rgw-my-store rook-ceph-rgw-my-store-external

kubectl -n rook-ceph get secret rook-ceph-object-user-my-store-my-user -o jsonpath='{.data.AccessKey}' | base64 --decode
kubectl -n rook-ceph get secret rook-ceph-object-user-my-store-my-user -o jsonpath='{.data.SecretKey}' | base64 --decode

# Enable the Object Gateway in Dashboard
radosgw-admin user create --uid=dashboard --display-name=dashboard --system

# Add this to PVC YAMLSs on deployments to use the block storage
spec:
  storageClassName: "rook-ceph-block"