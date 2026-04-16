# Pull openapi generator

## 1. npm (*)
npm install @openapitools/openapi-generator-cli -g

## 2. docker
docker pull openapitools/openapi-generator-cli

# Kiểm tra generator có hỗ trợ python-flask không

openapi-generator-cli list

# Sinh code từ .yaml và lựa chọn thư mục chứa code base

openapi-generator-cli generate \
  -i .\openapi\openapi.yaml 
  -g python-flask 
  -o .\openapi\server 

# Đổi phiên bản  python phù hơp với SQLAIchema (Lib hỗ trợ kết nối với db mysql)

Mở Dockerfile được sinh ra trong server qua FROM python:3.11-slim

# Thêm các lib để kết nối tới mysql vào trong requirement.txt

SQLAlchemy==2.0.48
PyMySQL==1.1.0
cryptography>=41.0.0

# Cấu hình Connection, Model, triển khai Controller từ khung code base
