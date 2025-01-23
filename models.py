from sqlmodel import Field, SQLModel
from pydantic import EmailStr

## VALIDAR DATOS, DNI... ##

class Cliente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, nullable=False)
    dni: str = Field(unique=True, max_length=9, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    capital_solicitado: float = Field(default=0.0, nullable=False)
