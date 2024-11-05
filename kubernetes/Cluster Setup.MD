# Install Kubectl on one machine
https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl

kubectl version --client




# Install Containerd/Docker on all machines
https://github.com/containerd/containerd/blob/main/docs/getting-started.md

for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin




# Install Kubeadm on all machines
https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet

kubeadm version


# Add containerd to CRI
cat > /etc/containerd/config.toml << EOF
version = 2
[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    sandbox_image = "registry.k8s.io/pause:3.9"
    [plugins."io.containerd.grpc.v1.cri".containerd]
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            SystemdCgroup = true
EOF

systemctl restart containerd

# Disable Swap
swapoff -a
sed -i '/ swap / s/^/#/' /etc/fstab

sudo nano /etc/fstab
#Comment out the swap line 


## Load br netfilter
modprobe br_netfilter
modprobe overlay

## Make filter persistent
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

## Set required sysctl params
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

## Apply sysctl params without reboot
sysctl --system

# Stop and disable Docker
systemctl stop docker.socket
systemctl stop docker
systemctl disable docker





# Create a cluster
https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/

# Initiate Kubeadm
kubeadm init --apiserver-advertise-address=192.168.1.150 --pod-network-cidr=192.168.0.0/16 --v=5


# Use Cluster:
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Use Cluster as Root
export KUBECONFIG=/etc/kubernetes/admin.conf


# Deploy a pod network to cluster
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
https://kubernetes.io/docs/concepts/cluster-administration/addons/

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/custom-resources.yaml
watch kubectl get pods -n calico-system
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl get nodes -o wide

# Then you can join any number of worker nodes by running the following on each as root:

kubeadm join ... etc from the terminal


# Rook-Ceph
https://computingforgeeks.com/how-to-deploy-rook-ceph-storage-on-kubernetes-cluster/

cd ~/
git clone --single-branch --branch release-1.15 https://github.com/rook/rook.git
cd rook/deploy/examples/
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



# Install Portainer

kubectl create namespace portainer
kubectl config set-context --current --namespace portainer
kubectl patch storageclass portainer-local-storage -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

kubectl get sc

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
sudo ./get_helm.sh

helm version

helm repo add portainer https://portainer.github.io/k8s/

helm repo update

helm install --create-namespace -n portainer portainer portainer/portainer \
    --set service.type=LoadBalancer
helm install --create-namespace -n portainer portainer portainer/portainer

helm install --create-namespace -n portainer portainer portainer/portainer \
  --set service.type=ClusterIP \
  --set ingress.enabled=true \
  --set ingress.annotations.'kubernetes\.io/ingress\.class'=nginx \
  --set ingress.annotations."nginx\.ingress\.kubernetes\.io/backend-protocol"=HTTPS \
  --set ingress.hosts[0].host=portainer.example.io \
  --set ingress.hosts[0].paths[0].path="/"

  kubectl get pods


# Useful Kubernetes Commands
kubectl get all -A
kubectl get pods -A 
kubectl get nodes -A 
watch kubectl get pods -n <namespace>