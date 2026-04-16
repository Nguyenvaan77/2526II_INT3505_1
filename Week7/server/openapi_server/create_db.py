from sqlalchemy import create_engine, text
from openapi_server.database import Base, DATABASE_URL
import openapi_server.models_db

# Tạo kết nối tới MySQL server mà không chỉ định database
server_url = DATABASE_URL.split("/")[0] + "//" + DATABASE_URL.split("//")[1].split("/")[0]
server_engine = create_engine(server_url, echo=False, pool_pre_ping=True)

# Tạo database nếu chưa tồn tại
with server_engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS mydb"))
    conn.commit()

# Kết nối tới database và tạo các bảng
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
Base.metadata.create_all(bind=engine)
print("\n✓ Database và các bảng đã được tạo thành công!")