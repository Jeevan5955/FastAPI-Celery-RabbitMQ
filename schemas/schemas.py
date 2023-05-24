from typing import List, Optional

from pydantic import BaseModel


class CreateUpdateUser(BaseModel):
    email: Optional[str] 
    name: Optional[str] = None
    mobileNumber: Optional[int] = None
    age: Optional[int] = None
    height: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "email": "njeevan@gmail.com",
                "name": "Jeevan",
                "mobileNumber": 8884974479,
                "age": 24,
                "height": 168
            }
        }


