from pydantic import BaseModel, computed_field, Field
from pydantic import EmailStr

class BaseUser(BaseModel):
    user_id : int
    user_name: str
    user_surname: str
    user_email: EmailStr

    @computed_field
    def full_name(self) -> str:
        return f'{self.user_name} {self.user_surname}'
    
class RegistrationUser(BaseModel):
    user_name: str
    user_surname: str
    user_email: EmailStr
    user_password: str = Field(min_length=8, max_length=32)

class LoginUser(BaseModel):
    user_email: EmailStr
    user_password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str