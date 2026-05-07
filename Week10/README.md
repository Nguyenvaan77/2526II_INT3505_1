# Chạy test hiệu năng (peformance)
1. Pull docker k6 (Container chỉ chạy được khi có script load test đầu vào)
2. Viết kịch bản test bằng file load_test.js
3. Chạy lệnh chạy test  `docker run -i -v ${PWD}:/scripts grafana/k6 run /scripts/load_test.js`
4. Lấy và đọc kết quả ở terminal

# Chạy test với pytest
1. ra thư mục gốc .\Week9 chạy lệnh pytest

# Tạo test suite 5 endpoint trong Postman và Chạy test với newman 
1. Tạo collection dựa trên các endpoint
2. Export 
    1. Vào 3 chấm '...' ở collection muốn tạo
    2. Vào More
    3. Vào Export
    4. Đưa vào folder project 
    5. Chạy lệnh terminal `newman run .\postman_collection.json` và đọc kết quả

