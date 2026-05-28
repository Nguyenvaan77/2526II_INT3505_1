#!/bin/bash

# Flask Production API - K8s Deployment Script
# This script deploys the Flask API to Kubernetes

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCKER_REGISTRY="${DOCKER_REGISTRY:-docker.io}"
IMAGE_NAME="${IMAGE_NAME:-flask-production-api}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
NAMESPACE="flask-api"
K8S_CONTEXT="${K8S_CONTEXT:-}"

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Flask Production API - K8s Deployment   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check prerequisites
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}✗ kubectl not found. Please install kubectl.${NC}"
    exit 1
fi
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ docker not found. Please install Docker.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Step 2: Build Docker image
echo -e "${YELLOW}[2/6] Building Docker image...${NC}"
echo "Building ${IMAGE_NAME}:${IMAGE_TAG}..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
echo -e "${GREEN}✓ Docker image built successfully${NC}"
echo ""

# Step 3: Load image into K8s (for local development)
if [ "${IMAGE_REGISTRY}" == "local" ] || [ "${DOCKER_REGISTRY}" == "local" ]; then
    echo -e "${YELLOW}[3/6] Loading image into local K8s cluster...${NC}"
    # This depends on your K8s setup (Docker Desktop, Minikube, etc.)
    # Uncomment the appropriate line for your setup:
    
    # For Docker Desktop:
    # Image is automatically available
    
    # For Minikube:
    # minikube image load ${IMAGE_NAME}:${IMAGE_TAG}
    
    # For Kind:
    # kind load docker-image ${IMAGE_NAME}:${IMAGE_TAG}
    
    echo -e "${GREEN}✓ Image loaded${NC}"
else
    echo -e "${YELLOW}[3/6] Skipping image load (using registry)${NC}"
fi
echo ""

# Step 4: Set K8s context if specified
if [ -n "${K8S_CONTEXT}" ]; then
    echo -e "${YELLOW}[4/6] Setting Kubernetes context...${NC}"
    kubectl config use-context ${K8S_CONTEXT}
    echo -e "${GREEN}✓ Context set to ${K8S_CONTEXT}${NC}"
else
    echo -e "${YELLOW}[4/6] Using current Kubernetes context...${NC}"
    kubectl config current-context
fi
echo ""

# Step 5: Deploy to Kubernetes
echo -e "${YELLOW}[5/6] Deploying to Kubernetes...${NC}"
echo "Creating namespace..."
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

echo "Applying K8s manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/pdb.yaml

# Apply ingress if NGINX ingress controller is available
if kubectl get ingressclass nginx &> /dev/null; then
    echo "Applying ingress configuration..."
    kubectl apply -f k8s/ingress.yaml
else
    echo -e "${YELLOW}⚠ NGINX ingress controller not found, skipping ingress${NC}"
fi

# Apply ServiceMonitor if Prometheus is available
if kubectl api-resources | grep -q servicemonitor; then
    echo "Applying Prometheus ServiceMonitor..."
    kubectl apply -f k8s/servicemonitor.yaml
else
    echo -e "${YELLOW}⚠ Prometheus not found, skipping ServiceMonitor${NC}"
fi

echo -e "${GREEN}✓ Deployment manifests applied${NC}"
echo ""

# Step 6: Wait for deployment to be ready
echo -e "${YELLOW}[6/6] Waiting for deployment to be ready...${NC}"
echo "This may take a few minutes..."

kubectl rollout status deployment/flask-api -n ${NAMESPACE} --timeout=5m

# Check pod status
echo ""
echo -e "${BLUE}Pod Status:${NC}"
kubectl get pods -n ${NAMESPACE}

# Get service information
echo ""
echo -e "${BLUE}Service Information:${NC}"
kubectl get svc -n ${NAMESPACE}

# Display access information
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      Deployment Complete! 🎉              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""

# Get the service endpoint
SERVICE_IP=$(kubectl get svc flask-api-service -n ${NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")

if [ "${SERVICE_IP}" != "pending" ]; then
    echo -e "${BLUE}Access your API at:${NC}"
    echo "  http://${SERVICE_IP}/"
    echo "  http://${SERVICE_IP}/health"
    echo "  http://${SERVICE_IP}/api/users"
else
    echo -e "${BLUE}API Service is being provisioned. Check status with:${NC}"
    echo "  kubectl get svc -n ${NAMESPACE}"
fi

echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "  View logs:"
echo "    kubectl logs -n ${NAMESPACE} -l app=flask-api -f"
echo ""
echo "  Port forward to access locally:"
echo "    kubectl port-forward -n ${NAMESPACE} svc/flask-api-service 8000:80"
echo ""
echo "  View metrics:"
echo "    kubectl port-forward -n ${NAMESPACE} svc/flask-api-service 8001:3000"
echo "    Then visit: http://localhost:8001/metrics"
echo ""
echo "  Scale deployment:"
echo "    kubectl scale deployment flask-api -n ${NAMESPACE} --replicas=5"
echo ""
echo "  View pod events:"
echo "    kubectl describe pod -n ${NAMESPACE} <pod-name>"
echo ""

echo -e "${GREEN}✓ All done!${NC}"
