from pydantic import BaseModel, computed_field, Field
from pydantic import EmailStr

class BaseUser(BaseModel):
    id : int
    name: str
    surname: str
    email: EmailStr

    @computed_field
    def full_name(self) -> str:
        return f'{self.name} {self.surname}'
    
class RegistrationUser(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str