# Helm Chart:
https://github.com/open-webui/helm-charts

helm repo add open-webui https://helm.openwebui.com/
helm repo update

Update the values.yaml to suit your platform. I have gpu turned off as my server has none.

helm template --values values.yaml open-webui open-webui/open-webui

# Deploy
kubectl apply -f ./open-webui


# If you are having trouble downloading models (connection errors)
# Check for internet access DNS
kubectl run dns-test --image=busybox:1.28 --rm -it -- nslookup kubernetes.default <!-- General -->
kubectl run dns-test --image=busybox:1.28 --rm -it -- nslookup registry.ollama.ai <!-- website -->

kubectl logs -n kube-system -l k8s-app=kube-dns

# Add IP to host file
dig +short registry.ollama.ai  <!-- get your ip -->
echo "172.67.188.176 registry.ollama.ai" >> /etc/hosts

# Edit CoreDNS Config
kubectl get configmap coredns -n kube-system -o yaml

forward . 8.8.8.8 8.8.4.4 { <!-- Change forward to google DNS -->
   max_concurrent 1000
}

kubectl rollout restart deployment coredns -n kube-system