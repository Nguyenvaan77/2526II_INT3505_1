# 📋 Luồng Hoạt Động Chi Tiết - Bank Webhook Demo

## 🎯 Tổng Quan Hệ Thống

Hệ thống sử dụng **Event-Driven Architecture** với gửi email bất đồng bộ:
- **Main App (Flask)**: Port 5000 - Xử lý API requests
- **Redis**: Port 6379 - Message Broker
- **Celery Worker**: Xử lý async tasks
- **Email Service**: Port 7000 - Webhook receiver

---

## 📊 So Sánh Các Endpoint

| **Endpoint** | **Method** | **Tham số** | **Quy trình** | **Response** | **Status Code** |
|---|---|---|---|---|---|
| **/users** | POST | `{name, email}` | 1. Generate UUID → 2. Lưu vào users dict → 3. Trả về user mới | `{user_id, name, email}` | **201** |
| **/tasks** | POST | `{user_id, title}` | 1. Verify user exists → 2. Generate UUID → 3. **Lưu task vào DB (sync)** → 4. **Create event** → 5. **Queue email task (async)** → 6. Trả về ngay | `{task_id, title, status, user_id}` | **201** |
| **/tasks/{id}** | PUT | `{title?, status?}` | 1. Verify task exists → 2. **Cập nhật task (sync)** → 3. **Create event** → 4. **Queue email task (async)** → 5. Trả về ngay | Task object cập nhật | **200** |
| **/tasks/{id}** | DELETE | - | 1. Verify task exists → 2. **Lấy task info** → 3. **Xoá task (sync)** → 4. **Create event** → 5. **Queue email task (async)** → 6. Trả về ngay | `{message: "Task deleted"}` | **200** |

---

## 🔷 Endpoint 1: Tạo User - `POST /users`

### Chi Tiết Luồng

```
Client (HTTP)
    ↓
POST /users {name, email}
    ↓
create_user()
    ├─ Lấy data từ request.json
    ├─ Generate UUID → user_id
    ├─ Tạo user object:
    │  {
    │    user_id: string,
    │    name: string,
    │    email: string
    │  }
    ├─ Lưu vào users dict: users[user_id] = user
    └─ Trả về Response 201
         {
           user_id, name, email
         }
```

### Code Implementation

```python
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user_id = str(uuid.uuid4())
    
    user = {
        "user_id": user_id,
        "name": data["name"],
        "email": data["email"]
    }
    
    users[user_id] = user  # Lưu vào in-memory DB
    return jsonify(user), 201
```

### Ví Dụ Request/Response

**Request:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Nguyễn Văn A", "email": "a@example.com"}'
```

**Response (201):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Nguyễn Văn A",
  "email": "a@example.com"
}
```

---

## 📝 Endpoint 2: Tạo Task - `POST /tasks`

### Chi Tiết Luồng (BẤT ĐỒNG BỘ)

```
Client (HTTP)
    ↓
POST /tasks {user_id, title}
    ↓
create_task()
    ├─ Kiểm tra user_id có tồn tại?
    │  ├─ KHÔNG → Return 404 "User not found"
    │  └─ CÓ → Tiếp tục
    │
    ├─ Generate UUID → task_id
    │
    ├─ Tạo task object:
    │  {
    │    task_id: string,
    │    title: string,
    │    status: "TODO",
    │    user_id: string
    │  }
    │
    ├─ 💾 LƯU VÀO DATABASE (ĐỒNG BỘ):
    │  tasks_db[task_id] = task
    │  Print: "Created New Task Successfully"
    │
    ├─ ✅ TẠO EVENT OBJECT:
    │  {
    │    event_id: string (UUID),
    │    event_type: "task_created",
    │    timestamp: ISO 8601,
    │    user: {...},
    │    task: {...}
    │  }
    │
    ├─ 📤 QUEUE ASYNC TASK:
    │  send_email_webhook_task.delay(event)
    │  → Task được đưa vào Redis Queue
    │
    └─ ⚡ TRẢ VỀ RESPONSE 201 NGAY (Không đợi email)
         {
           task_id, title, status, user_id
         }

================================ (BẤT ĐỒNG BỘ) ================================

ĐỒNG THỜI - Celery Worker xử lý:

Celery Worker
    ↓
Bắt task từ Redis Queue
    ↓
send_email_webhook_task()
    ├─ Serialize event thành JSON payload
    │
    ├─ 🔐 GENERATE HMAC SIGNATURE:
    │  signature = HMAC-SHA256(
    │    key=WEBHOOK_SECRET,
    │    message=payload
    │  )
    │
    ├─ 📧 SEND WEBHOOK:
    │  POST http://localhost:7000/webhooks/email
    │  Headers:
    │    - Content-Type: application/json
    │    - X-Webhook-Signature: {signature}
    │  Body: {event_data}
    │  Timeout: 5s
    │
    └─ Nếu lỗi → Retry (max 5 lần)
       - Exponential backoff

================== EMAIL SERVICE (Port 7000) ==================

Email Service
    ↓
receive_email_webhook()
    ├─ Lấy payload từ request.data
    │
    ├─ 🔐 VERIFY SIGNATURE:
    │  expected_sig = HMAC-SHA256(
    │    key=WEBHOOK_SECRET,
    │    message=payload
    │  )
    │  
    │  if signature != expected_sig:
    │    → Return 401 "Invalid signature"
    │
    ├─ Lấy event từ request.json
    │
    ├─ 🔍 CHECK DUPLICATE:
    │  if event_id in processed_events:
    │    → Return 200 "Duplicate ignored"
    │  else:
    │    processed_events.add(event_id)
    │
    ├─ ⏳ PROCESS EMAIL:
    │  time.sleep(10)  # Simulate processing
    │
    ├─ ✉️ SEND EMAIL:
    │  TO: user["email"]
    │  SUBJECT: Task Created
    │  BODY: Task {title} has been created
    │  Print: "EMAIL: Task created -> {title}"
    │
    └─ Return 200 "email processed"
```

### Code Implementation

**app.py:**
```python
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    user_id = data["user_id"]
    
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    task_id = str(uuid.uuid4())
    
    task = {
        "task_id": task_id,
        "title": data["title"],
        "status": "TODO",
        "user_id": user_id
    }
    
    tasks_db[task_id] = task  # 💾 SYNC: Lưu vào DB
    print("Created New Task Successfully")
    
    # ✅ Create Event
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "task_created",
        "timestamp": datetime.utcnow().isoformat(),
        "user": users[user_id],
        "task": task
    }
    
    # 📤 Queue Async Task
    send_email_webhook_task.delay(event)
    
    # ⚡ Trả về ngay (không đợi email)
    return jsonify(task), 201
```

**tasks.py:**
```python
@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=5
)
def send_email_webhook_task(self, event):
    payload = json.dumps(event)
    signature = generate_signature(payload)
    
    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Signature": signature
    }
    
    response = requests.post(
        WEBHOOK_URL,
        data=payload,
        headers=headers,
        timeout=5
    )
    
    print("\nWebhook Email Sent")
    print(response.status_code)
    
    return response.status_code
```

**email_service.py:**
```python
@app.route("/webhooks/email", methods=["POST"])
def receive_email_webhook():
    payload = request.data
    signature = request.headers.get("X-Webhook-Signature")
    
    # 🔐 Verify Signature
    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401
    
    event = request.json
    event_id = event["event_id"]
    
    # 🔍 Check Duplicate
    if event_id in processed_events:
        return jsonify({"message": "Duplicate ignored"}), 200
    
    processed_events.add(event_id)
    
    event_type = event["event_type"]
    user = event["user"]
    task = event["task"]
    
    # ⏳ Process
    time.sleep(10)
    
    # ✉️ Send Email
    print("\n========================")
    print("EMAIL SERVICE")
    print("========================")
    print("TO:", user["email"])
    
    if event_type == "task_created":
        print(f"EMAIL: Task created -> {task['title']}")
    
    return jsonify({"status": "email processed"}), 200
```

### Ví Dụ Request/Response

**Request:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Hoàn thành project"
  }'
```

**Response (201) - Trả về NGAY:**
```json
{
  "task_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "title": "Hoàn thành project",
  "status": "TODO",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Email được gửi bất đồng bộ (vài giây sau):**
```
========================
EMAIL SERVICE
========================
TO: a@example.com
EMAIL: Task created -> Hoàn thành project
```

---

## ✏️ Endpoint 3: Cập Nhật Task - `PUT /tasks/{task_id}`

### Chi Tiết Luồng

```
Client (HTTP)
    ↓
PUT /tasks/{task_id} {title?, status?}
    ↓
update_task(task_id)
    ├─ Kiểm tra task_id có tồn tại?
    │  ├─ KHÔNG → Return 404 "Task not found"
    │  └─ CÓ → Tiếp tục
    │
    ├─ 📝 CẬP NHẬT TASK:
    │  tasks_db[task_id]["title"] = data.get("title", ...)
    │  tasks_db[task_id]["status"] = data.get("status", ...)
    │
    ├─ ✅ TẠO EVENT OBJECT:
    │  {
    │    event_id: string,
    │    event_type: "task_updated",
    │    timestamp: ISO 8601,
    │    user: users[task["user_id"]],
    │    task: updated_task
    │  }
    │
    ├─ 📤 QUEUE ASYNC TASK
    │
    └─ ⚡ TRẢ VỀ 200 (Không đợi email)

(Email được gửi bất đồng bộ - tương tự POST /tasks)
```

### Code Implementation

```python
@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id not in tasks_db:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.json
    
    # 📝 Update
    tasks_db[task_id]["title"] = data.get(
        "title",
        tasks_db[task_id]["title"]
    )
    tasks_db[task_id]["status"] = data.get(
        "status",
        tasks_db[task_id]["status"]
    )
    
    task = tasks_db[task_id]
    user = users[task["user_id"]]
    
    # ✅ Create Event
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "task_updated",
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "task": task
    }
    
    # 📤 Queue Async Task
    send_email_webhook_task.delay(event)
    
    # ⚡ Trả về ngay
    return jsonify(task)
```

### Ví Dụ Request/Response

**Request:**
```bash
curl -X PUT http://localhost:5000/tasks/6ba7b810-9dad-11d1-80b4-00c04fd430c8 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hoàn thành project (Cập nhật)",
    "status": "IN_PROGRESS"
  }'
```

**Response (200):**
```json
{
  "task_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "title": "Hoàn thành project (Cập nhật)",
  "status": "IN_PROGRESS",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 🗑️ Endpoint 4: Xoá Task - `DELETE /tasks/{task_id}`

### Chi Tiết Luồng

```
Client (HTTP)
    ↓
DELETE /tasks/{task_id}
    ↓
delete_task(task_id)
    ├─ Kiểm tra task_id có tồn tại?
    │  ├─ KHÔNG → Return 404 "Task not found"
    │  └─ CÓ → Tiếp tục
    │
    ├─ ✅ LẤY THÔNG TIN TASK & USER:
    │  task = tasks_db[task_id]
    │  user = users[task["user_id"]]
    │
    ├─ 🗑️ XOÁ TASK:
    │  del tasks_db[task_id]
    │
    ├─ ✅ TẠO EVENT OBJECT:
    │  {
    │    event_id: string,
    │    event_type: "task_deleted",
    │    timestamp: ISO 8601,
    │    user: user,
    │    task: task (lấy trước khi xoá)
    │  }
    │
    ├─ 📤 QUEUE ASYNC TASK
    │
    └─ ⚡ TRẢ VỀ 200 (Không đợi email)

(Email được gửi bất đồng bộ)
```

### Code Implementation

```python
@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks_db:
        return jsonify({"error": "Task not found"}), 404
    
    task = tasks_db[task_id]
    user = users[task["user_id"]]
    
    # 🗑️ Delete
    del tasks_db[task_id]
    
    # ✅ Create Event (lưu trước khi xoá)
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "task_deleted",
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "task": task
    }
    
    # 📤 Queue Async Task
    send_email_webhook_task.delay(event)
    
    # ⚡ Trả về ngay
    return jsonify({"message": "Task deleted"})
```

### Ví Dụ Request/Response

**Request:**
```bash
curl -X DELETE http://localhost:5000/tasks/6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

**Response (200):**
```json
{
  "message": "Task deleted"
}
```

---

## ⏱️ Luồng Thời Gian Chi Tiết (Timeline)

```
T=0ms:    Client gửi POST /tasks
          ↓
T=1ms:    Flask endpoint kiểm tra user_id
          ↓
T=2ms:    ✅ Lưu task vào tasks_db (ĐỒNG BỘ)
          Print: "Created New Task Successfully"
          ↓
T=3ms:    ✅ Tạo Event object + Generate event_id
          ↓
T=4ms:    ✅ Queue task vào Redis
          send_email_webhook_task.delay(event)
          ↓
T=5ms:    ⚡ API trả về 201 → Client nhận response NGAY
          ← KHÔNG CHẶN ← KHÔNG ĐỢI EMAIL

═════════════════════════════════════════════════════════════════

T=5ms+:   Celery Worker bắt task từ Redis queue
          ↓
T=10ms:   Generate HMAC signature
          ↓
T=15ms:   Gửi POST webhook → Email Service:7000
          ↓
T=20ms:   Email Service nhận webhook
          ↓
T=25ms:   Xác thực signature (HMAC verify)
          ↓
T=30ms:   Kiểm tra duplicate (event_id)
          ↓
T=35ms:   ⏳ Sleep 10 giây (simulate processing)
          ↓
T=10035ms: Gửi email (print output)
          ↓
T=10040ms: Celery task hoàn thành ✅
```

---

## 🔑 Các Điểm Quan Trọng

### 1. ✅ Non-Blocking API

**Tại sao quan trọng:**
- Task được lưu vào DB **trước** khi queue async
- API trả về ngay (**5-10ms**) không đợi email (**10+ giây**)
- Cải thiện UX: Response nhanh, không timeout
- Avoid blocking I/O operations

**Code:**
```python
tasks_db[task_id] = task      # ✅ Sync - Trước
send_email_webhook_task.delay(event)  # 📤 Async - Sau
return jsonify(task), 201     # ⚡ Return ngay
```

### 2. ✅ Event-Driven Architecture

**Tại sao quan trọng:**
- Loosely coupled: Main app không cần biết email service
- Scalable: Có thể thêm event handlers khác (SMS, push, etc.)
- Traceable: Mỗi event có unique ID & timestamp

**Event Types:**
```python
event_type = "task_created"    # POST /tasks
event_type = "task_updated"    # PUT /tasks
event_type = "task_deleted"    # DELETE /tasks
```

### 3. ✅ Retry Mechanism

**Tại sao quan trọng:**
- Network failures không làm mất task
- Tự động thử lại khi email service down
- Exponential backoff tránh spam

**Code (tasks.py):**
```python
@celery.task(
    autoretry_for=(Exception,),  # Tự động retry khi lỗi
    retry_backoff=True,          # Exponential backoff
    max_retries=5                # Thử tối đa 5 lần
)
def send_email_webhook_task(self, event):
    ...
```

**Retry Timeline:**
```
Attempt 1: T=0s - Failed
Attempt 2: T=2s - Failed (2^1 = 2s delay)
Attempt 3: T=8s - Failed (2^2 = 4s delay)
Attempt 4: T=24s - Failed (2^3 = 8s delay)
Attempt 5: T=56s - Success!
```

### 4. ✅ Security (HMAC Signature)

**Tại sao quan trọng:**
- Xác minh webhook đến từ Celery worker (không phải attacker)
- Chặn các webhook giả mạo
- HMAC-SHA256 là cryptographically secure

**Flow:**
```
Celery Worker:
  payload = json.dumps(event)
  signature = HMAC-SHA256(key=SECRET, message=payload)
  Send POST with header: X-Webhook-Signature: {signature}

Email Service:
  expected = HMAC-SHA256(key=SECRET, message=payload)
  if signature != expected:
    return 401 "Invalid signature"  # ❌ Reject
```

### 5. ✅ Idempotency (Duplicate Detection)

**Tại sao quan trọng:**
- Webhook có thể bị retry nhiều lần
- Nếu không check, email gửi trùng lặp
- `event_id` unique → có thể phát hiện duplicate

**Code (email_service.py):**
```python
processed_events = set()  # Lưu event_id đã xử lý

event_id = event["event_id"]
if event_id in processed_events:
    return {"message": "Duplicate ignored"}, 200  # ✅ Skip
else:
    processed_events.add(event_id)
    # Process email...
```

---

## 📊 So Sánh Performance

| Thành phần | Thời gian | Ảnh hưởng |
|---|---|---|
| Save to DB (sync) | **1-2ms** | ✅ Nhanh |
| API response | **5-10ms** | ✅ Không chặn |
| Redis queue | **1-5ms** | ✅ Nhanh |
| Celery worker latency | **100ms-1s** | ⚠️ Có thể delay nếu worker bận |
| Generate signature | **5-10ms** | ✅ Nhanh |
| Send webhook | **50-200ms** | ✅ Nhanh |
| Email service processing | **10+ giây** | ✅ Async, không ảnh hưởng user |

**Total latency for user:** ~10ms ✅
**Total latency for email:** ~10+ seconds (async, không ảnh hưởng)

---

## 🚀 Cách Chạy Hệ Thống

### 1. Start Redis
```bash
# Terminal 1
redis-server
# hoặc nếu dùng Docker:
docker run -d -p 6379:6379 redis:7
```

### 2. Start Main App
```bash
# Terminal 2
python app.py
# Output: Running on http://127.0.0.1:5000
```

### 3. Start Celery Worker
```bash
# Terminal 3
celery -A tasks worker --loglevel=info
```

### 4. Start Email Service
```bash
# Terminal 4
python email_service.py
# Output: Running on http://127.0.0.1:7000
```

### 5. Test API

```bash
# 1. Create User
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Nguyễn Văn A", "email": "a@example.com"}'
# Lưu user_id

# 2. Create Task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"user_id": "YOUR_USER_ID", "title": "Hoàn thành project"}'
# Xem response ngay (201)
# Email được gửi vài giây sau

# 3. Update Task
curl -X PUT http://localhost:5000/tasks/YOUR_TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "IN_PROGRESS"}'

# 4. Delete Task
curl -X DELETE http://localhost:5000/tasks/YOUR_TASK_ID
```

---

## 📝 Tóm Tắt Kiến Trúc

```
┌─────────────┐
│   CLIENT    │
└──────┬──────┘
       │ HTTP Requests
       ↓
┌─────────────────────────────────────┐
│      MAIN APP (Flask:5000)          │
│  ┌───────────────────────────────┐  │
│  │ POST /users                   │  │
│  │ POST /tasks  ──→ Sync DB      │  │
│  │ PUT  /tasks  ──→ Async Queue  │  │
│  │ DELETE /tasks                 │  │
│  └───────────────────────────────┘  │
└────────┬────────────────────────────┘
         │
         │ Event ┌──────────────────┐
         └──────→│  REDIS:6379      │
                │ (Message Broker) │
                └────────┬─────────┘
                         │
                         │ Pull Task
                         ↓
                ┌──────────────────┐
                │ CELERY WORKER    │
                │ • Generate Sig   │
                │ • Send Webhook   │
                └────────┬─────────┘
                         │ POST Webhook
                         ↓
                ┌──────────────────────┐
                │ EMAIL SERVICE:7000   │
                │ • Verify Signature   │
                │ • Check Duplicate    │
                │ • Send Email         │
                └──────────────────────┘
```

---

## 🎓 Bài Học

1. **Non-blocking operations** cải thiện UX đáng kể
2. **Event-driven architecture** dễ scale & maintain
3. **Async tasks** thích hợp cho long-running operations
4. **HMAC signatures** bảo vệ webhook security
5. **Idempotency** quan trọng cho distributed systems
6. **Retry mechanisms** giúp handle transient failures

---

**Cập nhật lần cuối:** May 21, 2026
**Tác giả:** Bank Webhook Demo
**Phiên bản:** 1.0
