# 📋 K8s Migration Action Plan - Flask Production API

**Date**: May 15, 2026  
**Project**: Flask Production API K8s Deployment  
**Timeline**: 4 weeks  
**Priority**: High

---

## 🎯 Objective

Migrate Flask Production API to Kubernetes with proper configuration, distributed rate limiting, and production-grade monitoring.

---

## 📊 Current State vs Target State

### Current State
```
✅ Working Flask app with metrics
✅ Local Docker Compose setup
⚠️  In-memory rate limiting
⚠️  Hard-coded configuration
❌ Not suitable for multiple replicas
```

### Target State
```
✅ Flask app in Kubernetes cluster
✅ 3+ replicas with automatic scaling
✅ Distributed rate limiting (Redis)
✅ Environment-based configuration
✅ Graceful shutdown & startup probes
✅ Production monitoring & alerting
✅ Persistent logging
```

---

## 🗂️ Phase Breakdown

## 📌 PHASE 1: Code Modifications (Week 1-2)

### Task 1.1: Redis-Based Rate Limiting
**Priority**: 🔴 CRITICAL  
**Effort**: 3-4 hours  
**Owner**: Backend Developer

#### Problem
Current in-memory rate limiting won't work across multiple K8s replicas.

#### Solution
Replace in-memory storage with Redis backend.

#### Implementation Steps

1. **Update requirements.txt**
   ```
   Add: redis==5.0.0
   ```

2. **Modify app/app.py**
   ```python
   # Before:
   limiter = Limiter(
       app=app,
       key_func=get_remote_address,
       default_limits=["100 per hour"],
       storage_uri="memory://"
   )
   
   # After:
   import os
   
   REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
   
   limiter = Limiter(
       app=app,
       key_func=get_remote_address,
       default_limits=["100 per hour"],
       storage_uri=REDIS_URL
   )
   ```

3. **Add fallback for local development**
   ```python
   # Graceful fallback if Redis unavailable
   try:
       limiter.init_app(app)
   except Exception as e:
       logger.warning(f"Rate limiting disabled: {e}")
       # Continue without rate limiting
   ```

4. **Testing**
   ```bash
   # Test locally with Redis
   docker run -d -p 6379:6379 redis:latest
   export REDIS_URL=redis://localhost:6379/1
   python -m app.app
   ```

#### Acceptance Criteria
- [ ] Rate limiting works with Redis
- [ ] Fallback works without Redis
- [ ] K8s deployment can scale to 3 replicas
- [ ] Rate limits enforced across all replicas

---

### Task 1.2: Environment Variable Configuration
**Priority**: 🔴 CRITICAL  
**Effort**: 1-2 hours  
**Owner**: Backend Developer

#### Problem
Hard-coded values make K8s deployment difficult.

#### Solution
Move all configuration to environment variables.

#### Implementation Steps

1. **Create config module** (`app/config.py`)
   ```python
   import os
   from datetime import timedelta
   
   class Config:
       # Flask
       DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
       SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
       
       # Server
       PORT = int(os.getenv('PORT', 3000))
       HOST = os.getenv('HOST', '0.0.0.0')
       WORKERS = int(os.getenv('WORKERS', 4))
       
       # Redis
       REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
       
       # Logging
       LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
       LOG_DIR = os.getenv('LOG_DIR', 'logs')
       
       # API
       API_VERSION = os.getenv('API_VERSION', '1.0.0')
       API_NAME = os.getenv('API_NAME', 'Flask Production API')
       
       # Limits
       RATE_LIMIT_USERS = os.getenv('RATE_LIMIT_USERS', '10/minute')
       RATE_LIMIT_USER_ID = os.getenv('RATE_LIMIT_USER_ID', '15/minute')
   ```

2. **Update app.py to use config**
   ```python
   from app.config import Config
   
   app.config.from_object(Config)
   
   # Use config values
   PORT = Config.PORT
   WORKERS = Config.WORKERS
   ```

3. **Create .env.example**
   ```env
   # Server
   PORT=3000
   HOST=0.0.0.0
   WORKERS=4
   
   # Redis
   REDIS_URL=redis://localhost:6379/1
   
   # Logging
   LOG_LEVEL=INFO
   LOG_DIR=logs
   
   # API
   API_VERSION=1.0.0
   ```

4. **Testing**
   ```bash
   # Test with different config
   export PORT=8000
   export LOG_LEVEL=DEBUG
   python -m app.app
   ```

#### Acceptance Criteria
- [ ] All configuration from env variables
- [ ] .env.example updated
- [ ] Default values work for local dev
- [ ] K8s can set config via ConfigMap

---

### Task 1.3: Graceful Shutdown Handling
**Priority**: 🔴 CRITICAL  
**Effort**: 1-2 hours  
**Owner**: Backend Developer

#### Problem
App doesn't handle SIGTERM signal properly for K8s graceful shutdowns.

#### Solution
Implement signal handlers for graceful shutdown.

#### Implementation Steps

1. **Add signal handling** (`app/app.py`)
   ```python
   import signal
   import sys
   from threading import Event
   
   # Shutdown event
   shutdown_event = Event()
   
   def handle_sigterm(signum, frame):
       logger.info("SIGTERM received - initiating graceful shutdown")
       shutdown_event.set()
   
   signal.signal(signal.SIGTERM, handle_sigterm)
   signal.signal(signal.SIGINT, handle_sigterm)
   
   # Shutdown context manager
   @app.before_request
   def check_shutdown():
       if shutdown_event.is_set():
           return jsonify({"error": "Server shutting down"}), 503
   ```

2. **Update gunicorn startup** (in Dockerfile)
   ```dockerfile
   # Set timeout for graceful shutdown
   CMD ["gunicorn", \
        "--timeout", "30", \
        "--graceful-timeout", "30", \
        "-w", "4", \
        "-b", "0.0.0.0:3000", \
        "app.app:app"]
   ```

3. **Add preload app**
   ```dockerfile
   CMD ["gunicorn", \
        "--preload-app", \
        "--workers", "4", \
        "--bind", "0.0.0.0:3000", \
        "app.app:app"]
   ```

4. **Testing**
   ```bash
   # Start app
   python -m app.app
   
   # In another terminal
   kill -TERM <PID>
   
   # Should log graceful shutdown message
   ```

#### Acceptance Criteria
- [ ] App handles SIGTERM gracefully
- [ ] Existing requests complete before shutdown
- [ ] New requests rejected during shutdown
- [ ] Shutdown completes within 30 seconds

---

### Task 1.4: Startup/Readiness Probes
**Priority**: 🟠 HIGH  
**Effort**: 1 hour  
**Owner**: Backend Developer

#### Problem
K8s needs to verify app is ready to receive traffic.

#### Solution
Add startup and readiness probe endpoints.

#### Implementation Steps

1. **Add probe endpoints** (`app/app.py`)
   ```python
   from app.config import Config
   
   STARTUP_COMPLETE = False
   DEPENDENCIES_OK = {'redis': False, 'database': False}
   
   @app.before_first_request
   def startup():
       global STARTUP_COMPLETE
       try:
           # Check Redis connection
           import redis
           r = redis.Redis.from_url(Config.REDIS_URL)
           r.ping()
           DEPENDENCIES_OK['redis'] = True
           logger.info("Redis connection verified")
       except Exception as e:
           logger.warning(f"Redis unavailable: {e}")
           DEPENDENCIES_OK['redis'] = False
       
       STARTUP_COMPLETE = True
       logger.info("Application startup complete")
   
   @app.route('/startup')
   def startup_probe():
       """K8s startup probe - checks if app is initialized"""
       if STARTUP_COMPLETE:
           return jsonify({"status": "ready"}), 200
       else:
           return jsonify({"status": "initializing"}), 503
   
   @app.route('/ready')
   def readiness_probe():
       """K8s readiness probe - checks if ready for traffic"""
       if not STARTUP_COMPLETE:
           return jsonify({"status": "not_ready"}), 503
       
       # Check critical dependencies
       if not DEPENDENCIES_OK['redis']:
           return jsonify({"status": "dependencies_unavailable"}), 503
       
       return jsonify({"status": "ready"}), 200
   ```

2. **Update health endpoint**
   ```python
   @app.route('/health')
   def health():
       """Health check endpoint (existing)"""
       return jsonify({
           "status": "healthy",
           "message": "API is running",
           "dependencies": DEPENDENCIES_OK
       }), 200
   ```

3. **Testing**
   ```bash
   # Test before app ready
   curl http://localhost:3000/startup  # Should return 503
   
   # Wait for app initialization
   # Then test again
   curl http://localhost:3000/startup  # Should return 200
   curl http://localhost:3000/ready     # Should return 200
   ```

#### Acceptance Criteria
- [ ] /startup endpoint works
- [ ] /ready endpoint checks dependencies
- [ ] Proper HTTP status codes (200/503)
- [ ] JSON response format consistent

---

### Task 1.5: Structured Logging for K8s
**Priority**: 🟠 HIGH  
**Effort**: 1-2 hours  
**Owner**: Backend Developer

#### Problem
K8s prefers JSON-formatted logs for aggregation.

#### Solution
Add optional structured (JSON) logging.

#### Implementation Steps

1. **Update logger.py**
   ```python
   import json
   from datetime import datetime
   
   class JSONFormatter(logging.Formatter):
       def format(self, record):
           log_entry = {
               "timestamp": datetime.utcnow().isoformat(),
               "level": record.levelname,
               "logger": record.name,
               "message": record.getMessage(),
               "function": record.funcName,
               "line": record.lineno,
           }
           
           # Add request_id if available
           if hasattr(request, 'request_id'):
               log_entry['request_id'] = request.request_id
           
           return json.dumps(log_entry)
   
   # Check if structured logging enabled
   USE_JSON_LOGS = os.getenv('JSON_LOGS', 'False').lower() == 'true'
   
   if USE_JSON_LOGS:
       json_formatter = JSONFormatter()
       file_handler.setFormatter(json_formatter)
       console_handler.setFormatter(json_formatter)
   ```

2. **Add request ID tracking**
   ```python
   from uuid import uuid4
   from flask import g
   
   @app.before_request
   def add_request_id():
       request.request_id = str(uuid4())
       g.request_id = request.request_id
   ```

3. **Configuration**
   ```yaml
   # In K8s ConfigMap or .env
   JSON_LOGS=true  # Enable JSON logging
   ```

#### Acceptance Criteria
- [ ] JSON logging optional (via env var)
- [ ] All logs include timestamp & level
- [ ] Request ID included when available
- [ ] Works with log aggregation tools

---

## 📌 PHASE 2: Docker & Registry (Week 2)

### Task 2.1: Update Dockerfile
**Priority**: 🟠 HIGH  
**Effort**: 1 hour  
**Owner**: DevOps Engineer

#### Current Issues
- Running as root
- No health check
- Suboptimal layer caching

#### Improved Dockerfile
```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY config/ ./config/

# Create logs directory
RUN mkdir -p logs && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 3000

# Healthcheck (for local Docker)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:3000/health')"

# Run gunicorn with proper settings
CMD ["gunicorn", \
     "--bind", "0.0.0.0:3000", \
     "--workers", "4", \
     "--timeout", "30", \
     "--graceful-timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app.app:app"]
```

### Task 2.2: Build & Push Image
**Priority**: 🟠 HIGH  
**Effort**: 1 hour  
**Owner**: DevOps Engineer

#### Steps

1. **Create build script** (`build.sh`)
   ```bash
   #!/bin/bash
   set -e
   
   REGISTRY="${REGISTRY:-docker.io}"
   USERNAME="${USERNAME:-yourusername}"
   VERSION="${1:-latest}"
   
   echo "Building image..."
   docker build -t $REGISTRY/$USERNAME/flask-api:$VERSION \
                -t $REGISTRY/$USERNAME/flask-api:latest .
   
   echo "Pushing image..."
   docker push $REGISTRY/$USERNAME/flask-api:$VERSION
   docker push $REGISTRY/$USERNAME/flask-api:latest
   
   echo "Done! Image: $REGISTRY/$USERNAME/flask-api:$VERSION"
   ```

2. **Update docker-compose.yml for testing**
   ```yaml
   version: '3.8'
   services:
     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"
     
     api:
       build: .
       ports:
         - "3000:3000"
       environment:
         - REDIS_URL=redis://redis:6379/1
         - LOG_LEVEL=INFO
         - JSON_LOGS=false
       depends_on:
         - redis
       volumes:
         - ./logs:/app/logs
   
     prometheus:
       image: prom/prometheus:latest
       ports:
         - "9090:9090"
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml
   
     grafana:
       image: grafana/grafana:latest
       ports:
         - "3001:3000"
   ```

#### Acceptance Criteria
- [ ] Docker image builds successfully
- [ ] Image runs without errors
- [ ] Image pushed to registry
- [ ] Image tag includes version

---

## 📌 PHASE 3: Kubernetes Setup (Week 3)

### Task 3.1: Setup Redis for Rate Limiting
**Priority**: 🔴 CRITICAL  
**Effort**: 2 hours  
**Owner**: DevOps Engineer

#### File: `k8s/redis-deployment.yaml`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-storage
  namespace: flask-api
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: flask-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 100m
            memory: 256Mi
        volumeMounts:
        - name: storage
          mountPath: /data
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: redis-storage
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: flask-api
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
  clusterIP: None
```

### Task 3.2: Update Flask K8s Deployment
**Priority**: 🟠 HIGH  
**Effort**: 1-2 hours  
**Owner**: DevOps Engineer

#### Updates to `k8s/02-flask-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  namespace: flask-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      containers:
      - name: flask-api
        image: docker.io/yourusername/flask-api:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
        env:
        # Configuration from ConfigMap
        - name: REDIS_URL
          value: "redis://redis:6379/1"
        - name: LOG_LEVEL
          value: "INFO"
        - name: JSON_LOGS
          value: "true"
        - name: WORKERS
          value: "4"
        - name: RATE_LIMIT_USERS
          value: "10/minute"
        
        # Probes
        startupProbe:
          httpGet:
            path: /startup
            port: 3000
          failureThreshold: 30
          periodSeconds: 1
        
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 30
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 2
        
        # Resources
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        
        # Security
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
        
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: logs
          mountPath: /app/logs
      
      # Pod security
      securityContext:
        fsGroup: 1000
      
      volumes:
      - name: tmp
        emptyDir: {}
      - name: logs
        emptyDir: {}
```

### Task 3.3: Create ConfigMap for Application Config
**Priority**: 🟠 HIGH  
**Effort**: 30 minutes  
**Owner**: DevOps Engineer

#### File: `k8s/configmap-app.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: flask-api-config
  namespace: flask-api
data:
  .env: |
    FLASK_ENV=production
    PORT=3000
    WORKERS=4
    LOG_LEVEL=INFO
    JSON_LOGS=true
    REDIS_URL=redis://redis:6379/1
    RATE_LIMIT_USERS=10/minute
    RATE_LIMIT_USER_ID=15/minute
    API_VERSION=1.0.0
```

---

## 📌 PHASE 4: Testing & Deployment (Week 4)

### Task 4.1: Local Testing
**Priority**: 🟠 HIGH  
**Effort**: 2-3 hours  
**Owner**: QA Engineer

#### Test Plan

```bash
# 1. Unit tests
python -m pytest tests/

# 2. Integration tests
docker-compose up -d
pytest tests/integration/

# 3. Load testing
ab -n 1000 -c 10 http://localhost:3000/

# 4. Rate limit testing
for i in {1..15}; do curl http://localhost:3000/api/users; done
# Should see rate limit exceeded after 10 requests
```

### Task 4.2: K8s Deployment Testing
**Priority**: 🟠 HIGH  
**Effort**: 4-6 hours  
**Owner**: DevOps Engineer

#### Test Environment
- Minikube or similar K8s cluster
- Redis deployment
- Flask API deployment (3 replicas)
- Prometheus & Grafana

#### Tests

```bash
# 1. Deploy to K8s
kubectl apply -f k8s/

# 2. Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=flask-api -n flask-api --timeout=300s

# 3. Port forward & test
kubectl port-forward svc/flask-api 3000:3000 -n flask-api &
curl http://localhost:3000/health

# 4. Test rate limiting across replicas
for i in {1..20}; do 
  curl http://localhost:3000/api/users
done

# 5. Test pod restart
kubectl delete pod -l app=flask-api -n flask-api
# Should recover automatically

# 6. Test scaling
kubectl scale deployment flask-api --replicas=5 -n flask-api
# Monitor metrics in Prometheus/Grafana

# 7. Test graceful shutdown
kubectl delete pod <pod-name> -n flask-api
# Should complete existing requests

# 8. Verify metrics
kubectl port-forward svc/prometheus 9090:9090 -n flask-api &
# Open http://localhost:9090
# Check flask_* metrics
```

#### Acceptance Criteria
- [ ] All pods start successfully
- [ ] Health check passes
- [ ] API responds to requests
- [ ] Rate limiting works across replicas
- [ ] Metrics collected by Prometheus
- [ ] Pods recover from crashes
- [ ] Graceful shutdown works
- [ ] Scaling works (up & down)

---

## 📊 Risk Assessment & Mitigation

### Risk 1: Redis Dependency
**Risk Level**: 🔴 HIGH  
**Impact**: Rate limiting fails if Redis unavailable

**Mitigation**:
- [ ] Redis in K8s cluster (replicated)
- [ ] Fallback to in-memory for non-critical limits
- [ ] Monitor Redis health
- [ ] Alert on Redis failures

### Risk 2: Breaking Changes
**Risk Level**: 🟠 MEDIUM  
**Impact**: Existing clients might break

**Mitigation**:
- [ ] Backward compatibility tests
- [ ] API versioning (/api/v1/)
- [ ] Change log documentation
- [ ] Rollback plan

### Risk 3: Performance Degradation
**Risk Level**: 🟠 MEDIUM  
**Impact**: K8s overhead might slow down requests

**Mitigation**:
- [ ] Load testing before/after
- [ ] Monitor p95/p99 latencies
- [ ] Tune resource limits
- [ ] Use HPA for auto-scaling

### Risk 4: Data Loss
**Risk Level**: 🟡 LOW  
**Impact**: Metrics or logs lost in crash

**Mitigation**:
- [ ] PersistentVolumes for Prometheus
- [ ] Log aggregation to central store
- [ ] Backup & restore procedures

---

## ✅ Checklist

### Phase 1: Code Changes
- [ ] Redis integration implemented
- [ ] Environment variables configured
- [ ] Graceful shutdown added
- [ ] Startup/readiness probes added
- [ ] Structured logging option added
- [ ] Code reviewed & tested
- [ ] All tests passing

### Phase 2: Docker
- [ ] Dockerfile updated & security hardened
- [ ] Image builds successfully
- [ ] Image pushed to registry
- [ ] Docker Compose updated with Redis
- [ ] Local testing passes

### Phase 3: Kubernetes
- [ ] Redis K8s deployment created
- [ ] Flask K8s deployment updated
- [ ] ConfigMap created
- [ ] Services configured
- [ ] RBAC updated
- [ ] Monitoring configured

### Phase 4: Deployment
- [ ] Local testing completed
- [ ] K8s staging deployment successful
- [ ] Performance testing passed
- [ ] Smoke tests passed
- [ ] Monitoring & alerts working
- [ ] Documentation updated
- [ ] Production deployment plan approved

---

## 📞 Support & Escalation

### Technical Issues
- Contact: Backend Team Lead
- Response time: < 2 hours
- Escalation: Engineering Manager

### Deployment Issues
- Contact: DevOps Team Lead
- Response time: < 1 hour
- Escalation: Infrastructure Manager

### Performance Issues
- Contact: Performance Engineer
- Response time: < 2 hours
- Escalation: Technical Director

---

## 📚 Reference Documents

- **PROJECT-ANALYSIS.md** - Detailed analysis
- **K8S-DEPLOYMENT-GUIDE.md** - Deployment procedures
- **QUICK-START.md** - Quick reference
- **Kubernetes Docs**: https://kubernetes.io/docs/
- **Flask Docs**: https://flask.palletsprojects.com/

---

**Plan Status**: ✅ Ready for Implementation  
**Last Updated**: May 15, 2026  
**Next Milestone**: Phase 1 Completion (Week 1-2)

