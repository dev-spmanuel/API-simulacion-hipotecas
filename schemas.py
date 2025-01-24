from sqlmodel import SQLModel
from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime

# Esquema para crear un cliente (sin ID)
class ClienteCrear(SQLModel):
    nombre: str
    dni: str
    email: EmailStr
    capital_solicitado: float

# Esquema para devolver un cliente
class ClienteLeer(SQLModel):
    id: int
    nombre: str
    dni: str
    email: EmailStr
    capital_solicitado: float

    simulaciones: Optional[List["SimulacionHipotecaClienteLeer"]] = None


# Esquema para crear una simulación de hipoteca
class SimulacionHipotecaCrear(SQLModel):
    interes: float
    plazo: int


# Esquema para devolver una simulación de hipoteca
class SimulacionHipotecaLeer(SQLModel):
    id: int
    cliente_id: int
    cuota_mensual: float
    importe_total: float
    plazo: int
    interes: float
    fecha_simulacion: Optional[datetime] = None


# Esquema para mostrar una simulación de hipoteca junto con los datos del cliente (sin cliente_id)
class SimulacionHipotecaClienteLeer(SQLModel):
    id: int
    cuota_mensual: float
    importe_total: float
    plazo: int
    interes: float
    fecha_simulacion: Optional[datetime] = None