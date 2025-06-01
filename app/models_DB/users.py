from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.db_manager import Base

class User_db(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)

    api_key = Column(String(255), nullable=False, unique=True)
    role = Column(Enum("USER", "ADMIN", name="user_role"), nullable=False, default="USER")
