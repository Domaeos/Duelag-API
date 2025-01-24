from pydantic import BaseModel

class UserBase(BaseModel):
  email: str
  password: str

  class Config:
    from_attributes = True

class CreateUser(UserBase):
  username: str

class LoginUser(UserBase):
  class Config:
    from_attributes = True

class TokenSchema(BaseModel):
  access_token: str
  refresh_token: str

  class Config:
    from_attributes = True

class changepassword(UserBase):
  new_password:str

  class Config:
    from_attributes = True

class RefreshRequest(BaseModel):
    refresh_token: str