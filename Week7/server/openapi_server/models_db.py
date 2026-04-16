
from sqlalchemy.orm import relationship, scoped_session, Session
from openapi_server.database import Base, engine, SessionLocal

from sqlalchemy import Column, Integer, String, Float, ForeignKey

# Create scoped session for legacy query API
session = scoped_session(SessionLocal)
Base.query = session.query_property()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    products = relationship("ProductDB", back_populates="owner", cascade="all, delete")

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserDB", back_populates="products")

# Alias cho compatibility
UserModel = UserDB
ProductModel = ProductDB

# Simple db object decorator cho compatibility
class DBProxy:
    def __init__(self, scoped_session_obj):
        self._session = scoped_session_obj
    
    @property
    def session(self):
        return self._session()
    
    def add(self, obj):
        return self.session.add(obj)
    
    def delete(self, obj):
        return self.session.delete(obj)
    
    def commit(self):
        return self.session.commit()

db = DBProxy(session)