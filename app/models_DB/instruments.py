from sqlalchemy import Column, String
from app.db_manager import Base

class Instrument_db(Base):
    __tablename__ = "instruments"
    name = Column(String(255), nullable=False)
    ticker = Column(String(10), primary_key=True)
    