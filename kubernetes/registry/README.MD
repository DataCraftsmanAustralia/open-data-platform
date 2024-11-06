# Install apache2-utils
sudo apt install apache2-utils

# Create auth directory
mkdir auth

# Generate htpasswd file
htpasswd -Bbn <USERNAME> <PASSWORD> > auth/htpasswd


# Registry Deployment
kubectl create secret generic registry-auth --from-file=htpasswd=./auth/htpasswd -n datacraftsman
kubectl create -f deployment.yaml
kubectl create -f pvc.yaml
kubectl create -f service.yaml


# Connecting to the Registry
## For Linux, edit /etc/docker/daemon.json:
{
  "insecure-registries" : ["192.168.1.150:30777"]
}

## For Windows, using Docker Desktop:

Open Docker Desktop
Go to Settings
Click on "Docker Engine"
Add the configuration:
{
  "insecure-registries": ["192.168.1.150:30777"]
}

Click "Apply & Restart"