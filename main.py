from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import Cliente
from db import engine, create_db_and_tables, buscar_cliente_por_dni
from schemas import ClienteCrear, ClienteLeer, SimulacionHipotecaCrear, SimulacionHipotecaLeer
from validations import validar_cliente
from typing import Annotated
from simulacion_hipoteca import CalculadorSimulacionHipoteca


# Crear la base de datos y las tablas
create_db_and_tables()

# Dependencia para la sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


# Ruta para obtener todos los clientes
@app.get("/clientes/", response_model=list[ClienteLeer])
async def get_clients(session: SessionDep):
    clientes = session.exec(select(Cliente)).all()
    return clientes


# Ruta para obtener un cliente por su DNI
@app.get("/clientes/{cliente_dni}", response_model=ClienteLeer)
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

    client_data = cliente.model_dump()
    db_client.sqlmodel_update(client_data)

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


# Ruta para solicitar una simulación de hipoteca para un cliente
@app.post("/clientes/{cliente_dni}/simulacion", response_model=SimulacionHipotecaLeer)
async def simulate_mortgage(cliente_dni: str, datos: SimulacionHipotecaCrear, session: SessionDep):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if datos.interes is None or datos.plazo is None:
        raise HTTPException(status_code=400, detail="Interes anual y plazo en años son requeridos")

    calculador_hipoteca = CalculadorSimulacionHipoteca(cliente.capital_solicitado, datos.interes, datos.plazo)
    simulacion = calculador_hipoteca.crear_simulacion(session, cliente.id)
    
    return simulacion
