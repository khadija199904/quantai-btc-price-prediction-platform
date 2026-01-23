from pydantic import BaseModel ,Field
from datetime import datetime

class UserRegister(BaseModel):
    username :str
    password : str


class UserLogin(BaseModel):
    username :str
    password : str
