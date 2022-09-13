from typing import List, Optional

from pydantic import BaseModel


class PreprocessingData(BaseModel):
    sessionId: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "sessionId": "123456",
            }
        }

class ExotelPost(BaseModel):
    CallSid: Optional[str] = None
    Status: Optional[str] = None
    DateUpdated: Optional[str] = None

    class Config:
        
        schema_extra = {
            "example": {
                'CallSid': '9fa644151797d8978f62dc0158f01698', 
                'Status': 'busy', 
                'DateUpdated': '2022-09-08 18:26:06'
                }
        }

