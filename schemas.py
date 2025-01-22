from pydantic import BaseModel

class UserBase(BaseModel):
  username: str
  email: str
  password: str

  class Config:
    from_attributes = True

class CreateUser(UserBase):
  class Config:
    from_attributes = True
