from sqlmodel import SQLModel
from pydantic import EmailStr

# Esquema para crear un cliente (sin ID)
class ClienteCrear(SQLModel):
    nombre: str
    dni: str
    email: EmailStr
    capital_solicitado: float

# Esquema para devolver un cliente (con ID)
class ClienteLeer(SQLModel):
    id: int
    nombre: str
    dni: str
    email: EmailStr
    capital_solicitado: float