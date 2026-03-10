from pydantic import BaseModel, computed_field
from pydantic import EmailStr

class BaseUser(BaseModel):
    id : int
    name: str
    surname: str
    email: EmailStr

    @computed_field
    def full_name(self) -> str:
        return f'{self.name} {self.surname}'