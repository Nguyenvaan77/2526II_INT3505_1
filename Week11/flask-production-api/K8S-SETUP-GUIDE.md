# Quick Start: Setup Local Kubernetes Cluster

Để deploy ứng dụng Flask lên Kubernetes, bạn cần một Kubernetes cluster. Dưới đây là hướng dẫn thiết lập cho các tùy chọn phổ biến:

## Option 1: Docker Desktop (Recommended for Beginners)

### Setup

1. **Install Docker Desktop**
   - Download từ: https://www.docker.com/products/docker-desktop
   - Install và restart computer

2. **Enable Kubernetes**
   - Mở Docker Desktop
   - Go to Settings → Kubernetes
   - Check "Enable Kubernetes"
   - Wait for cluster to start (~2-5 minutes)

3. **Verify Installation**
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

### Deploy

```powershell
cd "d:\IT\Code\Kiến trúc hướng dịch vụ\2526II_INT3505_1\Week11\flask-production-api"

# Deploy all manifests
kubectl apply -f k8s/

# Or use the deploy script
.\deploy.sh
```

### Monitor Deployment

```powershell
# Watch pods
kubectl get pods -n flask-api --watch

# Check status
kubectl rollout status deployment/flask-api -n flask-api

# Port forward to access
kubectl port-forward -n flask-api svc/flask-api-service 8000:80

# Access API
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/api/users
```

---

## Option 2: Minikube (Good for Development)

### Setup

1. **Install Minikube**
   ```powershell
   # Using Chocolatey
   choco install minikube

   # Or download from: https://minikube.sigs.k8s.io/
   ```

2. **Start Minikube**
   ```powershell
   minikube start --cpus=4 --memory=4096 --driver=docker
   ```

3. **Load Docker Image**
   ```powershell
   minikube image load flask-production-api:latest
   ```

4. **Verify**
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

### Deploy

```powershell
cd "d:\IT\Code\Kiến trúc hướng dịch vụ\2526II_INT3505_1\Week11\flask-production-api"

# Update deployment.yaml: imagePullPolicy: Never
kubectl apply -f k8s/

# Get service IP
minikube service flask-api-service -n flask-api
```

### Cleanup

```powershell
minikube delete
```

---

## Option 3: Kind (Kubernetes in Docker)

### Setup

1. **Install Kind**
   ```powershell
   choco install kind
   # Or: go install sigs.k8s.io/kind@latest
   ```

2. **Create Cluster**
   ```powershell
   kind create cluster --name flask-api

   # Set context
   kubectl cluster-context kind-flask-api
   ```

3. **Load Docker Image**
   ```powershell
   kind load docker-image flask-production-api:latest --name flask-api
   ```

4. **Verify**
   ```powershell
   kubectl cluster-info
   ```

### Deploy

```powershell
cd "d:\IT\Code\Kiến trúc hướng dịch vụ\2526II_INT3505_1\Week11\flask-production-api"

# Update deployment.yaml: imagePullPolicy: Never
kubectl apply -f k8s/

# Port forward (Kind doesn't provide LoadBalancer)
kubectl port-forward -n flask-api svc/flask-api-service 8000:80
```

### Cleanup

```powershell
kind delete cluster --name flask-api
```

---

## Deployment Steps (All Options)

### 1. Apply Manifests

```powershell
cd "d:\IT\Code\Kiến trúc hướng dịch vụ\2526II_INT3505_1\Week11\flask-production-api"

# Deploy namespace and configurations first
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Deploy Redis
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/redis.yaml

# Wait for Redis to be ready
kubectl wait --for=condition=ready pod -l app=redis -n flask-api --timeout=60s

# Deploy Flask API
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/pdb.yaml
```

### 2. Monitor Deployment

```powershell
# Watch pods
kubectl get pods -n flask-api --watch

# Check all resources
kubectl get all -n flask-api

# View logs
kubectl logs -n flask-api -l app=flask-api -f
```

### 3. Verify Health

```powershell
# Forward port
kubectl port-forward -n flask-api svc/flask-api-service 8000:80

# Test in another terminal
Invoke-WebRequest http://localhost:8000/
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/api/users
```

---

## Useful Commands

```powershell
# Get pod info
kubectl get pods -n flask-api -o wide

# Describe pod (for debugging)
kubectl describe pod -n flask-api <pod-name>

# View logs
kubectl logs -n flask-api <pod-name>

# Execute command in pod
kubectl exec -it -n flask-api <pod-name> -- /bin/sh

# Port forward
kubectl port-forward -n flask-api svc/flask-api-service 8000:80

# Scale deployment
kubectl scale deployment flask-api -n flask-api --replicas=5

# Delete deployment
kubectl delete namespace flask-api
```

---

## Troubleshooting

### Pods stuck in "Pending"

```powershell
# Check events
kubectl describe pod -n flask-api <pod-name>

# Check resource availability
kubectl describe node
```

### Pods in "CrashLoopBackOff"

```powershell
# Check logs
kubectl logs -n flask-api <pod-name>

# Common issues:
# - Redis not running (check redis pod)
# - Config issues (check ConfigMap)
# - Missing dependencies (check Dockerfile)
```

### Can't connect to API

```powershell
# Check service
kubectl get svc -n flask-api

# Check endpoints
kubectl get endpoints -n flask-api

# Port forward and test
kubectl port-forward -n flask-api svc/flask-api-service 8000:80
Invoke-WebRequest http://localhost:8000/health
```

---

## Next: Production Deployment

For production deployment, use:

- **AWS EKS**: Amazon Elastic Kubernetes Service
- **Azure AKS**: Azure Kubernetes Service
- **Google GKE**: Google Kubernetes Engine
- **DigitalOcean DOKS**: DigitalOcean Kubernetes

Each provides managed Kubernetes with:
- High availability
- Auto-scaling
- Integrated monitoring
- Security features
- Load balancing

---

## References

- [Docker Desktop Kubernetes](https://docs.docker.com/desktop/kubernetes/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/)
- [Kind Documentation](https://kind.sigs.k8s.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
