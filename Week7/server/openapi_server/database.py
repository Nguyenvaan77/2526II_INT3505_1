import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Đọc cấu hình MySQL từ environment variables
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "160220057a")
MYSQL_HOST = os.getenv("MYSQL_HOST", "host.docker.internal")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "mydb")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(
    DATABASE_URL,
    echo=True,               # log SQL (debug)
    pool_pre_ping=True       # tránh lỗi mất kết nối
)

session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

SessionLocal = scoped_session(session_factory)

Base = declarative_base()