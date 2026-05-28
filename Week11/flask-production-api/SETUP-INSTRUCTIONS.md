# 🚀 Setup & Run Flask API on Kubernetes - Chi Tiết Từng Bước

## 📝 Tất Cả Các Bước (Dự Kiến Mất ~20 phút)

```
1. Bật Kubernetes Docker Desktop        (5 phút)
2. Build Docker image                    (2 phút)
3. Load image vào K8s                    (1 phút)
4. Deploy lên Kubernetes                 (3 phút)
5. Port forward & test API               (1 phút)
6. Monitor logs                          (tuỳ chọn)
```

---

## 🔥 **BƯỚC 1: Bật Kubernetes trong Docker Desktop** (QUAN TRỌNG!)

### ⚠️ **Bạn PHẢI làm bước này trước!**

#### **Nếu chạy trên Windows:**

**Cách 1: Thông qua GUI (Recommended)**

1. **Mở Docker Desktop**
   - Click vào icon Docker ở góc phải taskbar (phía dưới màn hình)
   - Hoặc tìm "Docker Desktop" trong Start menu

2. **Vào Settings**
   - Click icon Docker → "Settings"
   - Hoặc nhấn: Ctrl+, (Ctrl + dấu phẩy)

3. **Tìm "Kubernetes" trong sidebar trái**

4. **Check vào "Enable Kubernetes"**
   - Sẽ có dòng checkbox "Enable Kubernetes"
   - Click vào để check

5. **Click "Apply & Restart"**
   - Button ở góc phải dưới
   - Docker sẽ khởi động lại
   - Chờ **2-5 phút** cho đến khi xong

6. **Chờ cho đến khi "Docker Desktop is running"**
   - Xem status ở góc phải Docker window
   - Các components sẽ sáng xanh từng cái

---

## ✅ **Kiểm Tra Kubernetes Đã Ready**

Sau khi Docker Desktop khởi động xong, mở **PowerShell** hoặc **Command Prompt** ở thư mục project:

```powershell
cd "d:\IT\Code\Kiến trúc hướng dịch vụ\2526II_INT3505_1\Week11\flask-production-api"

# Kiểm tra K8s cluster
kubectl cluster-info
```

**Nếu thấy:**
```
Kubernetes control plane is running at https://127.0.0.1:...
CoreDNS is running at https://127.0.0.1:.../api/v1/namespaces/...
```

✅ **Kubernetes đã sẵn sàng!** Tiếp tục bước tiếp theo.

**Nếu thấy lỗi:**
```
Unable to connect to the server: dial tcp 127.0.0.1:...: connectex: ...
```

❌ **Kubernetes chưa bật.** Hãy quay lại Bước 1 và bật nó.

---

## 🐳 **BƯỚC 2: Build Docker Image**

Đảm bảo bạn ở thư mục project:

```powershell
cd "d:\IT\Code\Kiến trúc hướng dịch vụ\2526II_INT3505_1\Week11\flask-production-api"

# Build image
docker build -t flask-production-api:latest .
```

**Output sẽ trông như vầy:**
```
[+] Building 23.4s (13/13) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/7] FROM docker.io/library/python:3.12-slim
 => [2/7] WORKDIR /app
 => ... (các bước xây dựng)
 => => naming to docker.io/library/flask-production-api:latest
```

**Mất khoảng 1-2 phút.** Chờ cho đến khi thấy "FINISHED".

### ✅ Kiểm Tra Image

```powershell
docker images | findstr flask-production-api
```

Sẽ thấy:
```
flask-production-api   latest    f59350d31dbe   ...
```

---

## 📦 **BƯỚC 3: Load Image vào Docker Desktop K8s**

Docker Desktop tự động có sẵn image đã build, không cần làm gì thêm! ✓

---

## 🚀 **BƯỚC 4: Deploy lên Kubernetes**

### **Cách nhanh nhất: Deploy tất cả cùng lúc**

```powershell
cd "d:\IT\Code\Kiến trúc hướng dịch vụ\2526II_INT3505_1\Week11\flask-production-api"

# Deploy tất cả manifests
kubectl apply -f k8s/
```

**Output:**
```
namespace/flask-api created
configmap/flask-api-config created
secret/flask-api-secret created
serviceaccount/flask-api created
role.rbac.authorization.k8s.io/flask-api created
rolebinding.rbac.authorization.k8s.io/flask-api created
deployment.apps/redis created
service/flask-api-service created
service/flask-api-internal created
service/redis-service created
deployment.apps/flask-api created
horizontalpodautoscaler.autoscaling/flask-api-hpa created
poddisruptionbudget.policy/flask-api-pdb created
```

### **Kiểm Tra Deploy Trạng Thái**

```powershell
# Xem tất cả resources
kubectl get all -n flask-api
```

Sẽ thấy:
```
NAME                            READY   STATUS    RESTARTS   AGE
pod/redis-xxx                   1/1     Running   0          20s
pod/flask-api-xxx               1/1     Running   0          15s
pod/flask-api-yyy               1/1     Running   0          15s
pod/flask-api-zzz               1/1     Running   0          15s

NAME                        TYPE           CLUSTER-IP
svc/flask-api-service       LoadBalancer   10.96.x.x
svc/flask-api-internal      ClusterIP      10.96.x.x
svc/redis-service           ClusterIP      None

NAME                    READY   UP-TO-DATE   AVAILABLE
deployment.apps/redis   1/1     1            1
deployment.apps/flask-api 3/3   3            3
```

### **Chờ cho Deployment Ready**

```powershell
# Chờ cho deployment sẵn sàng (chạy đến khi thấy "successfully rolled out")
kubectl rollout status deployment/flask-api -n flask-api
```

**Output khi xong:**
```
deployment "flask-api" successfully rolled out
```

**Nếu chậm, có thể chờ tối đa 60 giây.**

---

## 🔌 **BƯỚC 5: Port Forward & Test API**

### **Mở Port Forward**

**Mở 1 cửa sổ PowerShell:**

```powershell
kubectl port-forward -n flask-api svc/flask-api-service 8000:80
```

Output:
```
Forwarding from 127.0.0.1:8000 -> 3000
Forwarding from [::1]:8000 -> 3000
```

**ĐỪng đóng cửa sổ này! Nó cần chạy liên tục để port forward hoạt động.**

### **Mở Cửa Sổ PowerShell Thứ 2 để Test API**

```powershell
# Test endpoint 1: Home
curl http://localhost:8000/

# Output:
# {
#   "message": "Flask Production API",
#   "version": "1.0.0",
#   "status": "running",
#   "redis": "connected"
# }

# Test endpoint 2: Health check
curl http://localhost:8000/health

# Test endpoint 3: Get users
curl http://localhost:8000/api/users

# Test endpoint 4: Get specific user
curl http://localhost:8000/api/users/1

# Test endpoint 5: Metrics
curl http://localhost:8000/metrics
```

**Nếu tất cả trả về response, ✅ ứng dụng đang chạy!**

---

## 📊 **BƯỚC 6: Xem Logs (Tuỳ Chọn)**

### **Xem logs từ tất cả pods**

```powershell
# Xem logs real-time
kubectl logs -n flask-api -l app=flask-api -f
```

Sẽ thấy:
```
[REQUEST] GET / from 127.0.0.1 [ID: xxx-xxx]
[RESPONSE] GET / - Status: 200 [ID: xxx-xxx]
[REQUEST] GET /api/users from 127.0.0.1 [ID: yyy-yyy]
[RESPONSE] GET /api/users - Status: 200 [ID: yyy-yyy]
```

### **Xem logs từ một pod cụ thể**

```powershell
# Lấy tên pod
kubectl get pods -n flask-api

# Xem logs của pod
kubectl logs -n flask-api flask-api-xxx -f
```

---

## 🔍 **BƯỚC 7: Kiểm Tra Chi Tiết (Tuỳ Chọn)**

### **Xem trạng thái pod**

```powershell
kubectl get pods -n flask-api -o wide
```

### **Mô tả pod (debug)**

```powershell
kubectl describe pod -n flask-api <pod-name>
```

### **Xem resource usage**

```powershell
kubectl top pods -n flask-api
```

### **Xem HPA status (auto-scaling)**

```powershell
kubectl get hpa -n flask-api
```

---

## 🧪 **Test Lần Lượt**

### **1. Test Health Check**

```powershell
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "message": "API is running",
  "version": "1.0.0",
  "dependencies": {
    "redis": true
  }
}
```

### **2. Test Get Users**

```powershell
curl http://localhost:8000/api/users
```

**Expected:**
```json
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"},
  {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]
```

### **3. Test Get Specific User**

```powershell
curl http://localhost:8000/api/users/1
```

**Expected:**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

### **4. Test Rate Limiting (Optional)**

```powershell
# Gửi requests nhanh chóng
for ($i=0; $i -lt 20; $i++) {
  curl http://localhost:8000/api/users
  Start-Sleep -Milliseconds 100
}

# Sau khi vượt 10 requests/minute, sẽ nhận:
# {
#   "error": "Rate limit exceeded",
#   "message": "10 per 1 minute"
# }
```

### **5. Test Metrics**

```powershell
curl http://localhost:8000/metrics
```

**Expected:** Prometheus metrics format (nhiều dòng)

---

## 🛑 **Dừng Deployment**

### **Xoá namespace (xoá tất cả resources)**

```powershell
kubectl delete namespace flask-api
```

### **Dừng Port Forward**

- Click vào cửa sổ port forward PowerShell
- Nhấn: **Ctrl + C**

---

## 🚨 **Troubleshooting**

### **Pods không chạy?**

```powershell
# Xem chi tiết pod
kubectl describe pod -n flask-api <pod-name>

# Xem logs
kubectl logs -n flask-api <pod-name>
```

### **Không thể kết nối đến API?**

```powershell
# Kiểm tra port forward đang chạy
# (Nên thấy "Forwarding from 127.0.0.1:8000 -> 3000")

# Kiểm tra service
kubectl get svc -n flask-api
```

### **Docker Desktop không bật Kubernetes?**

```powershell
# Kiểm tra Docker Desktop process
Get-Process docker* | Format-Table

# Nếu không thấy, hãy mở Docker Desktop lại
```

---

## ✅ **Checklist Hoàn Thành**

- [ ] Bật Kubernetes trong Docker Desktop
- [ ] Chạy `kubectl cluster-info` → Thành công
- [ ] Build Docker image → `docker build -t flask-production-api:latest .`
- [ ] Deploy → `kubectl apply -f k8s/`
- [ ] Xem pods → `kubectl get pods -n flask-api` → Thấy 4 pods (3 Flask + 1 Redis)
- [ ] Port forward → `kubectl port-forward -n flask-api svc/flask-api-service 8000:80`
- [ ] Test API → `curl http://localhost:8000/health` → Status 200
- [ ] Xem logs → `kubectl logs -n flask-api -l app=flask-api -f`

✅ **Tất cả hoàn thành = Ứng dụng đang chạy trên Kubernetes!**

---

## 📚 **Tài Liệu Thêm**

- Xem thêm: [DEPLOYMENT-CHECKLIST.md](DEPLOYMENT-CHECKLIST.md)
- Xem thêm: [KUBECTL-QUICK-REFERENCE.md](KUBECTL-QUICK-REFERENCE.md)
- Xem thêm: [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)

---

**Hãy làm từng bước một và ghi lại kết quả. Nếu gặp vấn đề, hãy kiểm tra phần Troubleshooting!**

🚀 **Happy Deploying!**
