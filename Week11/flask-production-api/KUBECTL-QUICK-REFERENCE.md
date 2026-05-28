# Kubectl Quick Reference

## 🚀 Deployment Commands

```bash
# Deploy everything
kubectl apply -f k8s/

# Deploy individual manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Delete deployment
kubectl delete -f k8s/
kubectl delete namespace flask-api

# Dry run (see what would happen)
kubectl apply -f k8s/ --dry-run=client -o yaml
```

## 📊 Status & Monitoring

```bash
# Check cluster status
kubectl cluster-info
kubectl get nodes
kubectl get node-features

# View namespaces
kubectl get namespaces

# Get all resources in namespace
kubectl get all -n flask-api

# View specific resources
kubectl get pods -n flask-api
kubectl get svc -n flask-api
kubectl get configmap -n flask-api
kubectl get secrets -n flask-api
kubectl get hpa -n flask-api
kubectl get ingress -n flask-api
```

## 🔍 Debugging

```bash
# Check pod status (verbose)
kubectl describe pod <pod-name> -n flask-api

# View pod logs
kubectl logs <pod-name> -n flask-api
kubectl logs <pod-name> -n flask-api -f  # follow
kubectl logs <pod-name> -n flask-api --tail=50  # last 50 lines
kubectl logs <pod-name> -n flask-api --previous  # previous logs

# View logs from all pods matching label
kubectl logs -n flask-api -l app=flask-api -f

# Execute command in pod
kubectl exec -it <pod-name> -n flask-api -- /bin/sh
kubectl exec <pod-name> -n flask-api -- ls -la /app

# Get pod details (YAML)
kubectl get pod <pod-name> -n flask-api -o yaml

# Watch pod events
kubectl get events -n flask-api --sort-by='.lastTimestamp'
kubectl get events -n flask-api -w  # watch
```

## 🔄 Deployment Management

```bash
# Check rollout status
kubectl rollout status deployment/flask-api -n flask-api

# Rollout history
kubectl rollout history deployment/flask-api -n flask-api

# Rollback to previous version
kubectl rollout undo deployment/flask-api -n flask-api

# Rollback to specific revision
kubectl rollout undo deployment/flask-api -n flask-api --to-revision=1

# Restart deployment
kubectl rollout restart deployment/flask-api -n flask-api

# Update image
kubectl set image deployment/flask-api flask-api=flask-production-api:v2 -n flask-api
```

## 🎯 Scaling

```bash
# Manual scaling
kubectl scale deployment flask-api -n flask-api --replicas=5

# Get HPA status
kubectl get hpa -n flask-api
kubectl describe hpa flask-api-hpa -n flask-api

# Edit HPA
kubectl edit hpa flask-api-hpa -n flask-api
```

## 🔌 Network & Access

```bash
# Port forward to service
kubectl port-forward -n flask-api svc/flask-api-service 8000:80

# Port forward to pod
kubectl port-forward -n flask-api <pod-name> 8000:3000

# Get service details
kubectl get svc -n flask-api
kubectl describe svc flask-api-service -n flask-api
kubectl get endpoints flask-api-service -n flask-api

# Get service IP
kubectl get svc flask-api-service -n flask-api -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## 📝 Configuration Management

```bash
# View ConfigMap
kubectl get configmap flask-api-config -n flask-api
kubectl describe configmap flask-api-config -n flask-api

# Edit ConfigMap
kubectl edit configmap flask-api-config -n flask-api

# Update ConfigMap from file
kubectl create configmap flask-api-config --from-file=config/ --dry-run=client -o yaml | kubectl apply -f -

# View Secrets
kubectl get secrets -n flask-api
kubectl describe secret flask-api-secret -n flask-api

# Edit Secret
kubectl edit secret flask-api-secret -n flask-api
```

## 📊 Resource Metrics

```bash
# View resource usage
kubectl top nodes
kubectl top pods -n flask-api
kubectl top pods -n flask-api --sort-by=memory

# Get resource requests/limits
kubectl get pods -n flask-api -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources}{"\n"}{end}'
```

## 🔐 RBAC & Security

```bash
# View ServiceAccount
kubectl get serviceaccount -n flask-api
kubectl describe serviceaccount flask-api -n flask-api

# View Roles
kubectl get role -n flask-api
kubectl describe role flask-api -n flask-api

# View RoleBindings
kubectl get rolebinding -n flask-api
kubectl describe rolebinding flask-api -n flask-api

# Get RBAC permissions
kubectl auth can-i get configmaps --as=system:serviceaccount:flask-api:flask-api -n flask-api
```

## 🎁 Useful One-Liners

```bash
# Get all pod IPs
kubectl get pods -n flask-api -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'

# Find pod by label
kubectl get pods -n flask-api -l app=flask-api

# Get pod in specific node
kubectl get pods -n flask-api --field-selector spec.nodeName=<node-name>

# Sort pods by restart count
kubectl get pods -n flask-api --sort-by=.status.containerStatuses[0].restartCount

# Watch deployment scaling
kubectl rollout status deployment/flask-api -n flask-api -w

# Check if pod is ready
kubectl get pod <pod-name> -n flask-api -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'

# Get API server logs
kubectl logs -n kube-system -l component=kube-apiserver

# Drain node for maintenance
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Uncordon node after maintenance
kubectl uncordon <node-name>
```

## 🧹 Cleanup

```bash
# Delete pod
kubectl delete pod <pod-name> -n flask-api

# Delete all pods
kubectl delete pods --all -n flask-api

# Delete deployment
kubectl delete deployment flask-api -n flask-api

# Delete namespace (deletes all resources)
kubectl delete namespace flask-api

# Delete all failed pods
kubectl delete pods --field-selector status.phase=Failed -n flask-api
```

## 🔗 Context & Config

```bash
# View current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Switch context
kubectl config use-context <context-name>

# View kubeconfig
kubectl config view
cat ~/.kube/config

# Set default namespace
kubectl config set-context --current --namespace=flask-api
```

## 🎓 Learning & Help

```bash
# Get resource documentation
kubectl api-resources
kubectl api-versions
kubectl explain deployment
kubectl explain deployment.spec

# Get command help
kubectl --help
kubectl apply --help
kubectl get --help

# Get API resource details
kubectl get pod <pod-name> -n flask-api -o json | jq .
```

## 🌐 Common Workflows

### Deploy New Version

```bash
# Build image
docker build -t flask-production-api:v2 .

# Load into cluster (if local)
docker image push flask-production-api:v2  # for registry
# or: kind load docker-image flask-production-api:v2

# Update deployment
kubectl set image deployment/flask-api flask-api=flask-production-api:v2 -n flask-api

# Monitor rollout
kubectl rollout status deployment/flask-api -n flask-api -w
```

### Access API Locally

```bash
# Terminal 1: Port forward
kubectl port-forward -n flask-api svc/flask-api-service 8000:80

# Terminal 2: Test API
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/api/users
```

### Debug Pod Issues

```bash
# Check pod events
kubectl describe pod <pod-name> -n flask-api

# Check pod logs
kubectl logs <pod-name> -n flask-api

# Execute command in pod
kubectl exec -it <pod-name> -n flask-api -- /bin/sh

# Copy file from pod
kubectl cp flask-api/<pod-name>:/app/logs/app.log ./app.log

# Check resource limits
kubectl describe pod <pod-name> -n flask-api | grep -A5 "Limits\|Requests"
```

---

**Save this as a reference while working with Kubernetes! 📚**
