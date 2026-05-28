# Kubernetes Deployment Guide - Flask Production API

## Overview

This guide walks you through deploying the Flask Production API to Kubernetes. The deployment includes:

- 3 replicas with auto-scaling (min 3, max 10)
- Distributed rate limiting with Redis
- Health checks and graceful shutdown
- Prometheus metrics monitoring
- Pod disruption budget for high availability

---

## Prerequisites

### Required Tools

```bash
# Kubernetes CLI
kubectl version --client

# Docker (for building images)
docker version

# Helm (optional, for package management)
helm version
```

### Kubernetes Cluster

You need a running Kubernetes cluster:

- **Local Development**: Docker Desktop, Minikube, or Kind
- **Cloud Providers**: EKS (AWS), AKS (Azure), GKE (Google Cloud)

### Cluster Requirements

- Kubernetes 1.20+
- Metrics Server (for HPA)
- Enough resources: 
  - Min: 1 CPU, 512 MB RAM per node
  - Recommended: 2 CPU, 2GB RAM per node

---

## Quick Start

### 1. Build Docker Image

```bash
docker build -t flask-production-api:latest .
```

For registry:
```bash
docker build -t your-registry/flask-production-api:latest .
docker push your-registry/flask-production-api:latest
```

### 2. Update Image in Deployment

Edit `k8s/deployment.yaml`:

```yaml
containers:
- name: flask-api
  image: your-registry/flask-production-api:latest  # Update this line
  imagePullPolicy: IfNotPresent  # Use IfNotPresent for local, Always for registry
```

### 3. Deploy to Kubernetes

```bash
# Deploy all manifests
kubectl apply -f k8s/

# Or deploy step by step
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/pdb.yaml
```

### 4. Verify Deployment

```bash
# Check namespace
kubectl get namespace flask-api

# Check pods
kubectl get pods -n flask-api

# Check deployment status
kubectl rollout status deployment/flask-api -n flask-api

# Check services
kubectl get svc -n flask-api
```

---

## Configuration

### Environment Variables

Edit `k8s/configmap.yaml` to modify:

```yaml
PORT: "3000"                          # API port
API_VERSION: "1.0.0"                 # API version
LOG_LEVEL: "INFO"                    # Logging level
REDIS_URL: "redis://redis-service:6379/1"
RATE_LIMIT_DEFAULT: "100 per hour"   # Default rate limit
```

### Secrets

Edit `k8s/secret.yaml` for sensitive data:

```yaml
SECRET_KEY: "your-secret-key"        # Flask secret key
DEBUG: "false"                        # Debug mode
```

**Important**: In production, use a secret management solution:

```bash
# Create secret from file
kubectl create secret generic flask-api-secret \
  --from-literal=SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))') \
  -n flask-api
```

---

## Accessing the API

### Using LoadBalancer Service

```bash
# Get external IP
kubectl get svc flask-api-service -n flask-api

# Access API
curl http://<EXTERNAL-IP>/
curl http://<EXTERNAL-IP>/health
curl http://<EXTERNAL-IP>/api/users
```

### Port Forwarding (Local Testing)

```bash
kubectl port-forward svc/flask-api-service 8000:80 -n flask-api
curl http://localhost:8000/
```

### Using Ingress

```bash
# Check ingress status
kubectl get ingress -n flask-api

# Add to /etc/hosts (for local testing)
echo "127.0.0.1  flask-api.example.com" | sudo tee -a /etc/hosts

# Access
curl http://flask-api.example.com/
```

---

## Monitoring

### Prometheus Metrics

```bash
# Access metrics endpoint
kubectl port-forward svc/flask-api-service 8001:3000 -n flask-api
curl http://localhost:8001/metrics
```

### Logs

```bash
# View logs
kubectl logs -n flask-api -l app=flask-api

# Tail logs
kubectl logs -n flask-api -l app=flask-api -f

# View logs from specific pod
kubectl logs -n flask-api <pod-name>

# View logs from all containers
kubectl logs -n flask-api -l app=flask-api --all-containers=true
```

### Pod Status

```bash
# Describe pod
kubectl describe pod <pod-name> -n flask-api

# Watch pod events
kubectl get events -n flask-api --sort-by='.lastTimestamp'
```

---

## Scaling

### Manual Scaling

```bash
# Scale to 5 replicas
kubectl scale deployment flask-api -n flask-api --replicas=5

# Scale back to 3
kubectl scale deployment flask-api -n flask-api --replicas=3
```

### Auto-Scaling (HPA)

The deployment includes Horizontal Pod Autoscaler that scales based on:

- CPU usage > 70%
- Memory usage > 80%

Check HPA status:

```bash
kubectl get hpa -n flask-api
kubectl describe hpa flask-api-hpa -n flask-api
```

---

## Updating the Deployment

### Update Image

```bash
# Method 1: Update deployment directly
kubectl set image deployment/flask-api \
  flask-api=your-registry/flask-production-api:v2 \
  -n flask-api

# Method 2: Edit deployment
kubectl edit deployment flask-api -n flask-api

# Method 3: Apply updated manifest
kubectl apply -f k8s/deployment.yaml
```

### Rolling Update

The deployment uses RollingUpdate strategy with:

- maxSurge: 1 (max 1 extra pod during update)
- maxUnavailable: 0 (no pods down during update)

Monitor the update:

```bash
kubectl rollout status deployment/flask-api -n flask-api
kubectl rollout history deployment/flask-api -n flask-api
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/flask-api -n flask-api

# Rollback to specific revision
kubectl rollout undo deployment/flask-api -n flask-api --to-revision=1
```

---

## Health Checks

The deployment includes three types of health checks:

### Startup Probe (60 seconds)
- Endpoint: `/startup`
- Checks if application is initialized
- Gives 2 minutes for app to start

### Readiness Probe (30 seconds)
- Endpoint: `/ready`
- Checks if app is ready for traffic
- Excludes pod from service if failing

### Liveness Probe (90 seconds)
- Endpoint: `/health`
- Checks if app is still running
- Restarts pod if failing 3 times

---

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl get pod <pod-name> -n flask-api -o yaml

# Check pod events
kubectl describe pod <pod-name> -n flask-api

# Check logs
kubectl logs <pod-name> -n flask-api
```

### Common Issues

#### CrashLoopBackOff

```bash
# Check container logs
kubectl logs <pod-name> -n flask-api

# Common causes:
# - Missing Redis connection
# - Configuration error
# - Missing dependencies
```

#### Pending Pods

```bash
# Check events
kubectl describe pod <pod-name> -n flask-api

# Common causes:
# - Insufficient resources
# - Init container failing
# - PVC not bound
```

#### Service Not Accessible

```bash
# Check service
kubectl get svc flask-api-service -n flask-api

# Check endpoints
kubectl get endpoints flask-api-service -n flask-api

# Test connectivity
kubectl run -it --rm debug --image=busybox -- sh
# Inside: wget -O- http://flask-api-service:80/health
```

### View Detailed Events

```bash
kubectl get events -n flask-api --sort-by='.lastTimestamp'
```

---

## Production Checklist

- [ ] Update Docker image in deployment.yaml
- [ ] Set SECRET_KEY in k8s/secret.yaml
- [ ] Configure Redis for persistence (StatefulSet)
- [ ] Setup Prometheus for monitoring
- [ ] Configure Ingress with TLS certificates
- [ ] Setup log aggregation (ELK, Splunk, etc.)
- [ ] Configure backup strategy
- [ ] Setup alerting rules
- [ ] Document runbooks
- [ ] Load testing before production

---

## Cleanup

### Remove Deployment

```bash
# Delete entire namespace (removes all resources)
kubectl delete namespace flask-api

# Or delete individual resources
kubectl delete deployment flask-api -n flask-api
kubectl delete service flask-api-service -n flask-api
kubectl delete configmap flask-api-config -n flask-api
kubectl delete secret flask-api-secret -n flask-api
```

---

## Next Steps

1. **Setup Monitoring**: Install Prometheus and Grafana
2. **Add CI/CD**: Integrate with GitLab CI, GitHub Actions, or Jenkins
3. **Configure Ingress**: Setup NGINX or Istio ingress controller
4. **Enable TLS**: Configure Let's Encrypt certificates
5. **Add Logging**: Setup ELK, Splunk, or Datadog
6. **Implement GitOps**: Use ArgoCD or Flux for declarative deployments

---

## Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)

