# models.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(Text, nullable=False, index=True)
    user_name = Column(Text, nullable=False)
    product_name = Column(Text, nullable=False)
    product_review = Column(Text, nullable=False)
    # store created_at in UTC (Postgres now() at timezone UTC recommended)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
