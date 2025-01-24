from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from db.db import get_session
from db.models import Cliente
from db.schemas import ClienteCrear, ClienteLeer, SimulacionHipotecaCrear, SimulacionHipotecaLeer

from validations.validations import validar_cliente

from services.simulacion_hipoteca import CalculadorSimulacionHipoteca



router = APIRouter(prefix="/clientes", tags=["Clientes"])


# Función para buscar un cliente por su DNI
def buscar_cliente_por_dni(session, cliente_dni):
    statement = select(Cliente).where(Cliente.dni == cliente_dni)
    return session.exec(statement).first()


# Ruta para obtener todos los clientes
@router.get("/", response_model=list[ClienteLeer])
async def get_clients(session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente)).all()
    return clientes


# Ruta para obtener un cliente por su DNI
@router.get("/{cliente_dni}", response_model=ClienteLeer)
def read_client(cliente_dni: str, session: Session = Depends(get_session)):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


# Ruta para crear un nuevo cliente
@router.post("/", response_model=ClienteLeer)
async def create_client(cliente: ClienteCrear, session: Session = Depends(get_session)):
    validar_cliente(session, cliente)
    
    db_cliente = Cliente(**cliente.model_dump())
    
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


# Ruta para actualizar un cliente
@router.put("/{cliente_dni}", response_model=ClienteLeer)
def update_client(cliente_dni: str, cliente: ClienteCrear, session: Session = Depends(get_session)):
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
@router.delete("/{cliente_dni}")
def delete_client(cliente_dni: str, session: Session = Depends(get_session)):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(cliente)
    session.commit()
    return {"message": "Cliente eliminado correctamente"}


# Ruta para solicitar una simulación de hipoteca para un cliente
@router.post("/{cliente_dni}/simulacion", response_model=SimulacionHipotecaLeer)
async def simulate_mortgage(cliente_dni: str, datos: SimulacionHipotecaCrear, session: Session = Depends(get_session)):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if datos.interes is None or datos.plazo is None:
        raise HTTPException(status_code=400, detail="Interes anual y plazo en años son requeridos")

    calculador_hipoteca = CalculadorSimulacionHipoteca(cliente.capital_solicitado, datos.interes, datos.plazo)
    simulacion = calculador_hipoteca.crear_simulacion(session, cliente.id)
    
    return simulacion