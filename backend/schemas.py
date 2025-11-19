# schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReviewOut(BaseModel):
    id: int
    contact_number: str
    user_name: str
    product_name: str
    product_review: str
    created_at: datetime

    class Config:
        orm_mode = True

class ReviewList(BaseModel):
    reviews: List[ReviewOut]
