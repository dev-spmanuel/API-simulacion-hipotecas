from sqlmodel import SQLModel

# Esquema para crear un cliente (sin ID)
class ClienteCrear(SQLModel):
    nombre: str
    dni: str
    email: str
    capital_solicitado: float

# Esquema para devolver un cliente (con ID)
class ClienteLeer(SQLModel):
    id: int
    nombre: str
    dni: str
    email: str
    capital_solicitado: float