# Kubernetes Demo Application: Client-Server Communication

This project demonstrates a simple client-server architecture deployed on Kubernetes using Minikube. Two client pods communicate with a server pod, with messages being logged.

## Prerequisites

Before getting started, ensure you have the following installed:
- Docker
- Minikube
- kubectl

## Execution Steps

### 1. Setup Environment

Start your Minikube cluster:

```bash
minikube start
```

### 2. Build Docker Images

Build the server and client images:

```bash
# Build server image
docker build -t server:latest -f Dockerfile.server .

# Build client image
docker build -t client:latest -f Dockerfile.client .
```

### 3. Deploy to Kubernetes

Apply the Kubernetes configuration:

```bash
# Apply Kubernetes configuration
kubectl apply -f kubernetes.yaml

# Verify pods are running
kubectl get pods
```

### 4. View Application Logs

Monitor logs from all components:

```bash
# Display logs from all components with prefix
kubectl logs -f -l "app in (server, client1, client2)" --prefix=true
```

### 5. Access Server Pod

To inspect the server pod and view the message log:

```bash
# Get server pod name
kubectl get pods

# Access server pod shell
kubectl exec -it <server-pod-name> -- /bin/bash

# Inside the pod, view message log continuously
tail -f messages.txt
```

