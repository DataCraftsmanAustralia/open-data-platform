# Reset kubeadm
kubeadm reset -f

# Stop kubelet and containerd
systemctl stop kubelet
systemctl stop containerd

# Clean up directories
rm -rf /etc/kubernetes/
rm -rf /var/lib/kubelet/
rm -rf /var/lib/etcd/
rm -rf $HOME/.kube/
rm -rf /var/lib/containerd/*

# Reset iptables
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
ipvsadm -C
ip link set docker0 down 2>/dev/null
ip link delete docker0 2>/dev/null

# Restart containerd
systemctl restart containerd