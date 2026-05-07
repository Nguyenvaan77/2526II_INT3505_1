# Thông Báo Ngừng Hỗ Trợ Payment API v1

## Tổng Quan

Chúng tôi chính thức phát hành Payment API v2 như một phần của chiến lược cải tiến vòng đời API (API Lifecycle Management).

Payment API v2 mang lại các cải tiến:

* Tăng cường bảo mật
* Cải thiện cấu trúc request và response
* Hỗ trợ currency
* Chuẩn hóa định dạng phản hồi API
* Dễ mở rộng cho các tính năng tương lai

Do đó, Payment API v1 hiện được đánh dấu là deprecated (ngừng phát triển) và sẽ bị loại bỏ trong tương lai.

---

# Các Mốc Thời Gian Quan Trọng

| Sự kiện                         | Thời gian  |
| ------------------------------- | ---------- |
| Phát hành Payment API v2        | 01/06/2026 |
| Bắt đầu deprecated API v1       | 01/09/2026 |
| Ngừng hoạt động API v1 (Sunset) | 01/12/2026 |

Sau ngày 01/12/2026, mọi request tới API v1 sẽ trả về:

```http id="me7q9w"
410 Gone
```

---

# Endpoint Bị Deprecated

```http id="pk3m0f"
POST /api/v1/payments
```

---

# Endpoint Mới

```http id="hn5k7r"
POST /api/v2/payments
```

---

# Vì Sao Cần API v2?

Phiên bản API trước đây tồn tại một số hạn chế trong thiết kế:

| Vấn đề ở v1                 | Cải tiến ở v2               |
| --------------------------- | --------------------------- |
| amount lưu dưới dạng string | amount sử dụng integer      |
| lộ toàn bộ số thẻ           | chỉ lưu 4 số cuối           |
| không hỗ trợ currency       | currency là trường bắt buộc |
| response không thống nhất   | response được chuẩn hóa     |
| khó mở rộng trong tương lai | thiết kế dễ mở rộng         |

---

# Các Breaking Changes

Các breaking changes sau đã được áp dụng trong v2.

---

## 1. Thay Đổi Kiểu Dữ Liệu amount

### v1

```json id="xj0f9t"
{
  "amount": "50000"
}
```

### v2

```json id="odv0nv"
{
  "amount": 50000
}
```

### Hành Động Cần Thực Hiện

Chuyển đổi amount từ kiểu string sang integer trước khi gửi request.

---

## 2. card_number Được Thay Bằng card_last4

### v1

```json id="2l8d6i"
{
  "card_number": "4111111111111111"
}
```

### v2

```json id="h2a8h9"
{
  "card_last4": "1111"
}
```

### Hành Động Cần Thực Hiện

Không gửi toàn bộ số thẻ nữa.
Chỉ gửi 4 số cuối của thẻ.

---

## 3. Thêm Trường currency

### v1

```json id="g9xy98"
{
  "amount": "50000"
}
```

### v2

```json id="u1l8jg"
{
  "amount": 50000,
  "currency": "VND"
}
```

### Hành Động Cần Thực Hiện

Ứng dụng bắt buộc phải gửi mã currency hợp lệ trong mọi request.

---

## 4. Thay Đổi Cấu Trúc Response

### Response v1

```json id="q0q37y"
{
  "id": 1,
  "status": "success"
}
```

### Response v2

```json id="8tx5ku"
{
  "data": {
    "payment_id": 1,
    "status": "completed"
  },
  "meta": {
    "api_version": "v2"
  }
}
```

### Hành Động Cần Thực Hiện

Ứng dụng cần đọc dữ liệu từ:

```text id="3e56dx"
response.data
```

thay vì đọc trực tiếp từ object gốc như ở v1.

---

# Kế Hoạch Migration

Chúng tôi khuyến nghị quy trình migration như sau.

---

## Giai Đoạn 1 — Triển Khai v2

* Tiếp tục duy trì hoạt động của v1
* Phát hành tài liệu cho v2
* Cho phép developers kiểm thử migration

---

## Giai Đoạn 2 — Cảnh Báo Deprecation

Response của v1 sẽ bao gồm các header:

```http id="jwxj8w"
Deprecation: true
Sunset: 2026-12-01
```

Điều này nhằm thông báo rằng v1 sẽ sớm bị loại bỏ.

---

## Giai Đoạn 3 — Migration Client

Developers cần:

* Cập nhật request payload
* Cập nhật logic xử lý response
* Thêm hỗ trợ currency
* Loại bỏ việc gửi full card number

---

## Giai Đoạn 4 — Ngừng Hoạt Động v1

Sau ngày sunset:

```http id="u7z3aa"
410 Gone
```

sẽ được trả về cho mọi endpoint thuộc v1.

---

# Hướng Dẫn Migration

Tài liệu migration chi tiết có tại:

```http id="zazk9v"
GET /api/migration-guide
```

---

# Khuyến Nghị Dành Cho Developers

* Bắt đầu migration càng sớm càng tốt
* Kiểm thử ứng dụng với v2
* Cập nhật integration trước ngày sunset
* Theo dõi deprecation warning trong HTTP headers

---

# Liên Hệ

Nếu có câu hỏi liên quan đến migration hoặc vấn đề tương thích, vui lòng liên hệ nhóm hỗ trợ API.

Xin cảm ơn vì đã sử dụng Payment API.
