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

Check for the latest version
https://github.com/projectcalico/calico/tree/master/manifests

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.0/manifests/custom-resources.yaml
watch kubectl get pods -n calico-system
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl get nodes -o wide

# Then you can join any number of worker nodes by running the following on each as root:

kubeadm join ... etc from the terminal

# Install Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
sudo ./get_helm.sh

helm version


# Move to the README.MD in Rook-Ceph to setup Cluster Storage

# Useful Kubernetes Commands
kubectl get all -A
kubectl get pods -A 
kubectl get nodes -A 
watch kubectl get pods -n <namespace>

kubectl describe pods
kubectl describe pod mysql-6cc489dcd5-5jc8t

kubectl create namespace datacraftsman
kubectl config set-context --current --namespace=datacraftsman

kubectl create -f file.yaml

helm install --values values.yaml name name/name
helm install <ChartName> --dry-run --debug

kubectl exec -it deploy/ollama -- bash


# Patch a deployment
kubectl patch deployment prometheus -p '{"spec":{"template":{"spec":{"serviceAccountName":"prometheus"}}}}'

# Restart a pod
kubectl rollout restart deployment prometheus

## Add a new node
kubeadm token create --print-join-command

# Check for internet access DNS
kubectl run dns-test --image=busybox:1.28 --rm -it -- nslookup kubernetes.default <!-- General -->
kubectl run dns-test --image=busybox:1.28 --rm -it -- nslookup registry.ollama.ai <!-- website -->

kubectl logs -n kube-system -l k8s-app=kube-dns

# Add IP to host file
dig +short registry.ollama.ai
echo "172.67.188.176 registry.ollama.ai" >> /etc/hosts

# Edit CoreDNS Config
kubectl get configmap coredns -n kube-system -o yaml

forward . 8.8.8.8 8.8.4.4 { <!-- Change forward to google DNS -->
   max_concurrent 1000
}

kubectl rollout restart deployment coredns -n kube-system