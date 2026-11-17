from pydantic import BaseModel, Field
from typing import Optional

class Student(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    gender: str = Field(..., min_length=3, max_length=10)
    marks: int = Field(..., ge=0, le=100)
    course: str = Field(..., min_length=2, max_length=50)
    attendance: str = Field(..., min_length=3, max_length=10)
    image_url: Optional[str] = ""