from pydantic import BaseModel,Field

class CreateUser(BaseModel):
    username:str = Field(..., min_length=3)
    password:str = Field(..., min_length=6)

class Event(BaseModel):
    title:str = Field(..., min_length=1)
    category:str
    due_date:str
    priority:str
    status:str
    notes:str