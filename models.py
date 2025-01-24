from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from typing import List, Optional
from datetime import datetime


class Cliente(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, nullable=False)
    dni: str = Field(unique=True, max_length=9, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    capital_solicitado: float = Field(default=0.0, nullable=False)

    simulaciones: List["SimulacionHipoteca"] = Relationship(back_populates="cliente", cascade_delete=True)


class SimulacionHipoteca(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    cuota_mensual: float = Field(default=0.0, nullable=False)
    importe_total: float = Field(default=0.0, nullable=False)
    plazo: int = Field(default=0, nullable=False)
    interes: float = Field(default=0.0, nullable=False)
    fecha_simulacion: datetime = Field(default=datetime.now(), nullable=False)

    cliente: Optional[Cliente] = Relationship(back_populates="simulaciones")