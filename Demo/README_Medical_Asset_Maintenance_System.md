# Medical Asset & Maintenance Management System

Hệ thống Quản lý Thiết bị Y tế và Bảo trì Bệnh viện, hỗ trợ quản lý thiết bị, lịch bảo trì, yêu cầu sửa chữa, nhật ký sửa chữa, linh kiện thay thế, tồn kho và phân quyền người dùng theo vai trò.

---

## 1. Giới thiệu đề tài

Trong bệnh viện, số lượng thiết bị y tế thường rất lớn và thuộc nhiều nhóm khác nhau như máy siêu âm, máy thở, máy xét nghiệm, máy MRI, máy đo huyết áp, monitor, bơm tiêm điện,...  
Mỗi thiết bị đều cần được theo dõi thông tin sử dụng, trạng thái hoạt động, lịch bảo trì định kỳ, lịch sử sửa chữa, chi phí phát sinh và linh kiện thay thế.

Đề tài này không chỉ dừng ở việc lưu danh sách thiết bị, mà tập trung vào **xử lý nghiệp vụ thực tế**, bao gồm:

- Báo hỏng thiết bị
- Tự động tạo và quản lý yêu cầu sửa chữa
- Gán kỹ thuật viên xử lý
- Ghi nhận nhật ký sửa chữa
- Quản lý linh kiện thay thế và tự động trừ kho
- Sinh lịch bảo trì định kỳ
- Phân quyền theo vai trò người dùng
- Báo cáo, thống kê tình trạng thiết bị và chi phí bảo trì

Đây là một đề tài phù hợp với môn học vì thể hiện được:

- **Data model nhiều thực thể, quan hệ đa dạng**
- **API xử lý logic nghiệp vụ, không chỉ CRUD**
- **Phân quyền user theo role**
- **Triển khai backend service với Spring Boot**
- **Thiết kế API có cấu trúc rõ ràng**

---

## 2. Mục tiêu hệ thống

Hệ thống được xây dựng nhằm:

- Quản lý tập trung toàn bộ thiết bị y tế trong bệnh viện
- Theo dõi trạng thái hoạt động của từng thiết bị
- Hỗ trợ nhân viên y tế báo hỏng nhanh chóng
- Hỗ trợ kỹ thuật viên xử lý, ghi log sửa chữa và dùng linh kiện
- Tự động theo dõi bảo trì định kỳ
- Hỗ trợ quản lý và kế toán theo dõi chi phí sửa chữa, bảo trì
- Hỗ trợ ban quản lý thống kê rủi ro và hiệu quả vận hành thiết bị

---

## 3. Phạm vi chức năng chính

### 3.1. Quản lý người dùng và phân quyền

- Đăng nhập hệ thống bằng JWT
- Quản lý tài khoản người dùng
- Gán vai trò cho người dùng
- Gán người dùng vào khoa/phòng ban
- Kiểm soát quyền truy cập theo role

### 3.2. Quản lý thiết bị y tế

- Thêm mới thiết bị
- Cập nhật thông tin thiết bị
- Xem danh sách thiết bị
- Xem chi tiết thiết bị
- Quản lý trạng thái thiết bị
- Gán thiết bị cho khoa/phòng ban

### 3.3. Quản lý loại thiết bị và nhà sản xuất

- Quản lý loại thiết bị
- Quản lý hãng sản xuất
- Quản lý model, serial number
- Thiết lập chu kỳ bảo trì mặc định theo từng loại

### 3.4. Báo hỏng thiết bị

- Bác sĩ/y tá báo hỏng thiết bị
- Nhập mô tả lỗi
- Hệ thống tạo yêu cầu sửa chữa
- Thiết bị được cập nhật trạng thái hỏng

### 3.5. Quản lý yêu cầu sửa chữa

- Tạo yêu cầu sửa chữa
- Phân công kỹ thuật viên
- Theo dõi tiến độ xử lý
- Hoàn thành hoặc hủy yêu cầu

### 3.6. Nhật ký sửa chữa

- Kỹ thuật viên ghi nhận quá trình sửa chữa
- Ghi nguyên nhân lỗi
- Ghi cách xử lý
- Ghi chi phí
- Ghi thời gian bắt đầu/kết thúc
- Ghi nhận linh kiện đã thay

### 3.7. Quản lý lịch bảo trì định kỳ

- Tạo lịch bảo trì
- Sinh lịch bảo trì tự động
- Đánh dấu hoàn thành bảo trì
- Theo dõi các lịch bảo trì quá hạn

### 3.8. Quản lý linh kiện và tồn kho

- Quản lý danh sách linh kiện
- Theo dõi số lượng tồn
- Cảnh báo sắp hết hàng
- Tự động trừ kho khi kỹ thuật viên sử dụng linh kiện

### 3.9. Báo cáo và thống kê

- Thống kê thiết bị theo trạng thái
- Thống kê yêu cầu sửa chữa
- Thống kê chi phí sửa chữa
- Thống kê thiết bị quá hạn bảo trì
- Thống kê linh kiện sắp hết

---

## 4. Vai trò người dùng

Hệ thống sử dụng mô hình phân quyền theo vai trò.

### 4.1. ADMIN

- Quản lý user
- Quản lý role
- Quản lý thiết bị
- Quản lý loại thiết bị
- Quản lý hãng sản xuất
- Quản lý khoa/phòng ban
- Xem toàn bộ dữ liệu hệ thống

### 4.2. DOCTOR / NURSE

- Xem thiết bị thuộc khoa mình
- Báo hỏng thiết bị
- Theo dõi tình trạng sửa chữa

### 4.3. ENGINEER

- Xem yêu cầu sửa chữa được giao
- Cập nhật trạng thái xử lý
- Tạo nhật ký sửa chữa
- Ghi nhận linh kiện sử dụng
- Hoàn thành yêu cầu sửa chữa

### 4.4. ACCOUNTANT

- Xem chi phí sửa chữa
- Theo dõi chi phí bảo trì
- Xem báo cáo chi phí

### 4.5. MANAGER

- Xem báo cáo tổng quan
- Xem thiết bị rủi ro cao
- Xem thống kê hoạt động và bảo trì

---

## 5. Công nghệ sử dụng

### Backend
- Spring Boot
- Spring Web
- Spring Data JPA
- Spring Security
- JWT Authentication
- Hibernate Validator

### Database
- MySQL hoặc PostgreSQL

### API Documentation
- OpenAPI / Swagger

### Build Tool
- Maven

### Frontend (nếu có)
- ReactJS hoặc Thymeleaf

---

## 6. Thiết kế dữ liệu (Data Model)

Hệ thống có nhiều thực thể và quan hệ nhằm đáp ứng yêu cầu của môn học.

### 6.1. Danh sách thực thể chính

- User
- Role
- Department
- Asset
- AssetType
- Manufacturer
- MaintenanceSchedule
- ServiceRequest
- ServiceLog
- TechnicalStaff
- ReplacementPart
- Inventory
- UsedPart
- Contract
- DepreciationRecord

### 6.2. Mối quan hệ chính

- Department **1 - N** Asset
- AssetType **1 - N** Asset
- Manufacturer **1 - N** Asset
- Asset **1 - N** MaintenanceSchedule
- Asset **1 - N** ServiceRequest
- ServiceRequest **1 - N** ServiceLog
- TechnicalStaff **1 - N** ServiceLog
- ServiceLog **1 - N** UsedPart
- ReplacementPart **1 - N** UsedPart
- ReplacementPart **1 - 1** Inventory
- User **N - N** Role
- Manufacturer **1 - N** Contract
- Asset **1 - N** DepreciationRecord

### 6.3. Ý nghĩa dữ liệu

#### User
Lưu thông tin tài khoản đăng nhập.

#### Role
Lưu vai trò để phân quyền.

#### Department
Lưu thông tin khoa/phòng ban sử dụng thiết bị.

#### Asset
Lưu thiết bị y tế cụ thể.

#### AssetType
Lưu nhóm loại thiết bị như MRI, Ultrasound, Ventilator,...

#### Manufacturer
Lưu hãng sản xuất thiết bị.

#### MaintenanceSchedule
Lưu lịch bảo trì định kỳ hoặc bảo trì phát sinh.

#### ServiceRequest
Lưu yêu cầu sửa chữa khi thiết bị bị hỏng.

#### ServiceLog
Lưu nhật ký xử lý và sửa chữa thiết bị.

#### ReplacementPart
Lưu thông tin linh kiện thay thế.

#### Inventory
Lưu số lượng tồn kho của linh kiện.

#### UsedPart
Bảng trung gian thể hiện linh kiện đã dùng trong một lần sửa chữa.

#### Contract
Lưu hợp đồng bảo hành / bảo trì với nhà cung cấp.

#### DepreciationRecord
Lưu dữ liệu khấu hao nếu mở rộng hệ thống.

---

## 7. Trạng thái nghiệp vụ

### 7.1. Trạng thái thiết bị

- AVAILABLE
- IN_USE
- UNDER_MAINTENANCE
- BROKEN
- RETIRED

### 7.2. Trạng thái yêu cầu sửa chữa

- PENDING
- ASSIGNED
- IN_PROGRESS
- COMPLETED
- CANCELLED

### 7.3. Trạng thái lịch bảo trì

- SCHEDULED
- IN_PROGRESS
- DONE
- OVERDUE
- CANCELLED

---

## 8. Luồng nghiệp vụ chính

### 8.1. Luồng báo hỏng thiết bị

1. Bác sĩ/y tá chọn thiết bị cần báo hỏng
2. Nhập mô tả lỗi
3. Hệ thống tạo `ServiceRequest`
4. Hệ thống cập nhật trạng thái `Asset = BROKEN`
5. Quản lý hoặc admin phân công kỹ thuật viên xử lý

### 8.2. Luồng sửa chữa thiết bị

1. Kỹ thuật viên nhận yêu cầu sửa chữa
2. Kỹ thuật viên kiểm tra thiết bị
3. Tạo `ServiceLog`
4. Nhập nguyên nhân lỗi, hướng xử lý, chi phí
5. Nếu có thay linh kiện, tạo `UsedPart`
6. Hệ thống tự động trừ tồn kho trong `Inventory`
7. Sau khi sửa xong, cập nhật trạng thái yêu cầu thành `COMPLETED`
8. Hệ thống cập nhật lại trạng thái thiết bị thành `AVAILABLE` hoặc `UNDER_MAINTENANCE`

### 8.3. Luồng sinh lịch bảo trì

1. Hệ thống quét toàn bộ thiết bị
2. Kiểm tra ngày bảo trì gần nhất
3. Dựa trên chu kỳ bảo trì của loại thiết bị
4. Sinh lịch bảo trì tiếp theo nếu đến hạn
5. Gửi dữ liệu cho quản lý/kỹ thuật viên theo dõi

---

## 9. Thiết kế API

Ngoài các API CRUD cơ bản, hệ thống cần có API xử lý nghiệp vụ.

### 9.1. Authentication API

#### POST `/api/auth/login`
Đăng nhập và nhận JWT token.

#### POST `/api/auth/register`
Tạo tài khoản mới (chỉ admin hoặc theo cấu hình hệ thống).

---

### 9.2. User API

#### GET `/api/users`
Lấy danh sách người dùng.

#### GET `/api/users/{id}`
Lấy chi tiết người dùng.

#### POST `/api/users`
Tạo người dùng mới.

#### PUT `/api/users/{id}`
Cập nhật người dùng.

#### DELETE `/api/users/{id}`
Xóa người dùng.

---

### 9.3. Department API

#### GET `/api/departments`
Lấy danh sách khoa/phòng ban.

#### POST `/api/departments`
Tạo khoa/phòng ban mới.

#### GET `/api/departments/{id}/assets`
Lấy danh sách thiết bị thuộc khoa.

---

### 9.4. Asset API

#### GET `/api/assets`
Lấy danh sách thiết bị.

#### GET `/api/assets/{id}`
Lấy chi tiết thiết bị.

#### POST `/api/assets`
Tạo thiết bị mới.

#### PUT `/api/assets/{id}`
Cập nhật thông tin thiết bị.

#### DELETE `/api/assets/{id}`
Xóa thiết bị.

#### POST `/api/assets/{id}/report-failure`
Báo hỏng thiết bị.

#### GET `/api/assets/{id}/maintenance-history`
Xem lịch sử bảo trì.

#### GET `/api/assets/{id}/service-history`
Xem lịch sử sửa chữa.

---

### 9.5. AssetType API

#### GET `/api/asset-types`
Lấy danh sách loại thiết bị.

#### POST `/api/asset-types`
Tạo loại thiết bị mới.

#### PUT `/api/asset-types/{id}`
Cập nhật loại thiết bị.

---

### 9.6. Manufacturer API

#### GET `/api/manufacturers`
Lấy danh sách hãng sản xuất.

#### POST `/api/manufacturers`
Tạo hãng sản xuất.

---

### 9.7. Service Request API

#### GET `/api/service-requests`
Lấy danh sách yêu cầu sửa chữa.

#### GET `/api/service-requests/{id}`
Lấy chi tiết yêu cầu sửa chữa.

#### POST `/api/service-requests`
Tạo yêu cầu sửa chữa.

#### POST `/api/service-requests/{id}/assign-engineer`
Phân công kỹ thuật viên.

#### POST `/api/service-requests/{id}/start`
Bắt đầu xử lý.

#### POST `/api/service-requests/{id}/complete`
Hoàn thành sửa chữa.

#### POST `/api/service-requests/{id}/cancel`
Hủy yêu cầu sửa chữa.

---

### 9.8. Service Log API

#### GET `/api/service-logs`
Lấy danh sách log sửa chữa.

#### POST `/api/service-logs`
Tạo log sửa chữa.

#### GET `/api/service-logs/{id}`
Lấy chi tiết log sửa chữa.

#### POST `/api/service-logs/{id}/used-parts`
Ghi nhận linh kiện đã sử dụng.

---

### 9.9. Maintenance Schedule API

#### GET `/api/maintenance-schedules`
Lấy danh sách lịch bảo trì.

#### POST `/api/maintenance-schedules`
Tạo lịch bảo trì thủ công.

#### POST `/api/maintenance-schedules/generate`
Tự động sinh lịch bảo trì.

#### POST `/api/maintenance-schedules/{id}/start`
Bắt đầu bảo trì.

#### POST `/api/maintenance-schedules/{id}/complete`
Hoàn thành bảo trì.

---

### 9.10. Replacement Part & Inventory API

#### GET `/api/replacement-parts`
Lấy danh sách linh kiện.

#### POST `/api/replacement-parts`
Tạo linh kiện mới.

#### GET `/api/inventories`
Lấy danh sách tồn kho.

#### PUT `/api/inventories/{id}`
Cập nhật tồn kho.

#### GET `/api/inventories/low-stock`
Lấy danh sách linh kiện sắp hết.

---

### 9.11. Report API

#### GET `/api/reports/assets-by-status`
Thống kê thiết bị theo trạng thái.

#### GET `/api/reports/service-costs`
Thống kê chi phí sửa chữa.

#### GET `/api/reports/overdue-maintenance`
Danh sách thiết bị quá hạn bảo trì.

#### GET `/api/reports/low-stock-parts`
Danh sách linh kiện sắp hết.

---

## 10. Các API thể hiện xử lý logic nghiệp vụ

Đây là phần quan trọng để chứng minh hệ thống không chỉ CRUD.

### 10.1. API báo hỏng thiết bị

**POST** `/api/assets/{id}/report-failure`

Xử lý:
- Kiểm tra thiết bị có tồn tại không
- Kiểm tra user có quyền báo hỏng không
- Tạo `ServiceRequest`
- Cập nhật trạng thái thiết bị sang `BROKEN`
- Ghi nhận thời điểm phát sinh lỗi

### 10.2. API phân công kỹ thuật viên

**POST** `/api/service-requests/{id}/assign-engineer`

Xử lý:
- Kiểm tra yêu cầu sửa chữa còn khả dụng không
- Kiểm tra kỹ thuật viên có tồn tại không
- Kiểm tra kỹ thuật viên có đúng vai trò không
- Gán người xử lý
- Cập nhật trạng thái `ASSIGNED`

### 10.3. API hoàn thành sửa chữa

**POST** `/api/service-requests/{id}/complete`

Xử lý:
- Kiểm tra yêu cầu đang ở trạng thái phù hợp
- Kiểm tra đã có log sửa chữa chưa
- Kiểm tra kỹ thuật viên có quyền thao tác không
- Cập nhật trạng thái yêu cầu thành `COMPLETED`
- Cập nhật trạng thái thiết bị phù hợp

### 10.4. API dùng linh kiện trong sửa chữa

**POST** `/api/service-logs/{id}/used-parts`

Xử lý:
- Kiểm tra linh kiện có tồn tại không
- Kiểm tra số lượng tồn kho
- Nếu đủ hàng thì tạo `UsedPart`
- Tự động trừ tồn trong `Inventory`
- Nếu tồn kho xuống thấp hơn ngưỡng thì đánh dấu cảnh báo

### 10.5. API sinh lịch bảo trì

**POST** `/api/maintenance-schedules/generate`

Xử lý:
- Quét toàn bộ thiết bị
- Tính toán ngày bảo trì tiếp theo
- Tạo lịch bảo trì mới nếu đến hạn
- Tránh tạo trùng lịch cho cùng một thiết bị

---

## 11. Gợi ý cấu trúc project Spring Boot

```text
medical-asset-maintenance/
├── src/main/java/com/example/medicalasset
│   ├── config
│   ├── controller
│   ├── dto
│   ├── entity
│   ├── enum
│   ├── exception
│   ├── mapper
│   ├── repository
│   ├── security
│   ├── service
│   └── MedicalAssetApplication.java
├── src/main/resources
│   ├── application.yml
│   └── data.sql
├── pom.xml
└── README.md
```

### Giải thích

- `controller`: xử lý request/response
- `service`: xử lý nghiệp vụ
- `repository`: truy vấn database
- `entity`: ánh xạ bảng dữ liệu
- `dto`: dữ liệu trao đổi giữa client và server
- `security`: JWT, filter, cấu hình Spring Security
- `exception`: xử lý lỗi tập trung
- `mapper`: chuyển đổi entity <-> dto

---

## 12. Gợi ý một số entity cốt lõi

### Asset
- id
- code
- name
- serialNumber
- purchaseDate
- purchasePrice
- status
- departmentId
- assetTypeId
- manufacturerId

### ServiceRequest
- id
- assetId
- reportedBy
- assignedEngineerId
- description
- status
- priority
- createdAt
- updatedAt

### ServiceLog
- id
- serviceRequestId
- engineerId
- problemCause
- resolution
- repairCost
- startedAt
- finishedAt

### ReplacementPart
- id
- partCode
- name
- unitPrice

### Inventory
- id
- partId
- quantity
- minThreshold

### MaintenanceSchedule
- id
- assetId
- scheduledDate
- completedDate
- status
- note

---

## 13. Bảo mật và phân quyền

Hệ thống sử dụng Spring Security + JWT.

### Cơ chế
- User đăng nhập bằng username/password
- Hệ thống sinh JWT token
- Client gửi token trong header Authorization
- Server kiểm tra token và role để cho phép truy cập API

### Ví dụ phân quyền
- `/api/auth/**`: public
- `/api/assets/**`: ADMIN, MANAGER, ENGINEER
- `/api/assets/{id}/report-failure`: DOCTOR, NURSE, ADMIN
- `/api/service-requests/{id}/assign-engineer`: ADMIN, MANAGER
- `/api/service-requests/{id}/complete`: ENGINEER
- `/api/reports/**`: ADMIN, MANAGER, ACCOUNTANT

---

## 14. Các điểm nổi bật của đề tài theo yêu cầu môn học

### 14.1. Data model tốt
- Nhiều thực thể
- Có quan hệ 1-N, 1-1, N-N
- Có bảng trung gian `UsedPart`
- Có dữ liệu nghiệp vụ thay vì chỉ danh sách đơn giản

### 14.2. API xử lý logic
- Báo hỏng thiết bị
- Phân công kỹ thuật viên
- Hoàn thành sửa chữa
- Dùng linh kiện và trừ kho
- Sinh lịch bảo trì tự động

### 14.3. Có phân quyền users
- Nhiều vai trò người dùng
- Mỗi vai trò có quyền khác nhau
- Kiểm soát truy cập bằng JWT + RBAC

### 14.4. Thể hiện triển khai backend service
- Spring Boot REST API
- JPA/Hibernate
- Swagger/OpenAPI
- Security
- Validation
- Exception handling

---

## 15. MVP đề xuất

Nếu thời gian làm có hạn, nên ưu tiên phiên bản MVP gồm:

- Đăng nhập + JWT
- Quản lý user + role
- Quản lý khoa/phòng ban
- Quản lý thiết bị
- Báo hỏng thiết bị
- Quản lý yêu cầu sửa chữa
- Nhật ký sửa chữa
- Quản lý linh kiện và tồn kho
- Sinh lịch bảo trì
- Báo cáo cơ bản

---

## 16. Hướng mở rộng

Nếu còn thời gian có thể mở rộng thêm:

- Quản lý hợp đồng bảo hành
- Tính khấu hao thiết bị
- Gửi email thông báo lịch bảo trì
- Dashboard trực quan
- Upload file biên bản sửa chữa
- Tích hợp barcode/QR cho thiết bị
- Thống kê nâng cao theo khoa/phòng ban/tháng/quý

---

## 17. Kết luận

**Medical Asset & Maintenance Management System** là một đề tài phù hợp cho bài tập lớn vì có:

- Nghiệp vụ rõ ràng
- Dữ liệu đủ sâu
- Nhiều thực thể và quan hệ
- API xử lý logic thay vì chỉ CRUD
- Có phân quyền người dùng
- Dễ triển khai bằng Spring Boot

Đây là một đề tài vừa đủ thực tế, vừa đủ phức tạp để thể hiện tốt các kỹ năng về phân tích hệ thống, thiết kế data model, thiết kế API và triển khai backend service.
