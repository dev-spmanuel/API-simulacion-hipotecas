from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import Cliente, SimulacionHipoteca
from db import engine, create_db_and_tables, buscar_cliente_por_dni
from schemas import ClienteCrear, ClienteLeer, SimulacionHipotecaCrear, SimulacionHipotecaLeer
from validations import validar_cliente
from datetime import datetime
from typing import Annotated


# Crear la base de datos y las tablas
create_db_and_tables()

# Dependencia para la sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


# Ruta para obtener todos los clientes
@app.get("/clientes/", response_model=list[ClienteLeer], response_model_exclude_unset=True)
async def get_clients(session: SessionDep):
    clientes = session.exec(select(Cliente)).all()
    return clientes


# Ruta para obtener un cliente por su DNI
@app.get("/clientes/{cliente_dni}", response_model=ClienteLeer, response_model_exclude_unset=True)
def read_client(cliente_dni: str, session: SessionDep):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


# Ruta para crear un nuevo cliente
@app.post("/clientes/", response_model=ClienteLeer)
async def create_client(cliente: ClienteCrear, session: SessionDep):
    validar_cliente(session, cliente)
    
    db_cliente = Cliente(**cliente.model_dump())
    
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


# Ruta para actualizar un cliente
@app.put("/clientes/{cliente_dni}", response_model=ClienteLeer)
def update_client(cliente_dni: str, cliente: ClienteCrear, session: SessionDep):
    db_client = buscar_cliente_por_dni(session, cliente_dni)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    validar_cliente(session, cliente, db_client.id)

    update_data = cliente.model_dump()
    for key, value in update_data.items():
        setattr(db_client, key, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


# Ruta para eliminar un cliente por su DNI
@app.delete("/clientes/{cliente_dni}")
def delete_client(cliente_dni: str, session: SessionDep):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(cliente)
    session.commit()
    return {"message": "Cliente eliminado correctamente"}


def calcular_hipoteca(capital, tae, plazo_años):
    # Calcular el interés mensual
    i = tae / 100 / 12
    # Calcular el número total de meses
    n = plazo_años * 12
    # Calcular la cuota mensual
    cuota = capital * i / (1 - (1 + i) ** -n)

    # Calcular el importe total a devolver
    importe_total = cuota * n

    # Devolver la cuota y el importe total redondeados a 2 decimales
    return round(cuota, 2), round(importe_total, 2)


def crear_simulacion(session: Session, cliente, plazo: int, interes: float):

    # Calcular los valores de la simulación
    cuota_mensual, importe_total = calcular_hipoteca(cliente.capital_solicitado, interes, plazo)

    # Crear una nueva simulación
    simulacion = SimulacionHipoteca(
        cliente_id=cliente.id,
        cuota_mensual=cuota_mensual,
        importe_total=importe_total,
        plazo=plazo,
        interes=interes,
        fecha_simulacion=datetime.now()
    )

    # return simulacion

    # Guardar la simulación en la base de datos
    session.add(simulacion)
    session.commit()
    # session.refresh(simulacion)
    return simulacion


# Ruta para solicitar una simulación de hipoteca para un cliente
@app.post("/clientes/{cliente_dni}/simulacion", response_model=SimulacionHipotecaLeer)
async def simulate_mortgage(cliente_dni: str, datos: SimulacionHipotecaCrear, session: SessionDep):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if datos.interes is None or datos.plazo is None:
        raise HTTPException(status_code=400, detail="Interes anual y plazo en años son requeridos")

    simulacion = crear_simulacion(session, cliente, datos.plazo, datos.interes)

    return simulacion


    