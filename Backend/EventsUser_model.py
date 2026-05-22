from pydantic import BaseModel

class signup_user(BaseModel):
    username:str
    password:str

class login_user(BaseModel):
    username:str
    password:str