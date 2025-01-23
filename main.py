from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import Cliente
from db import engine, create_db_and_tables
from schemas import ClienteCrear, ClienteLeer
from validations import validar_cliente

app = FastAPI()

# Crear la base de datos y las tablas
create_db_and_tables()

# Dependencia para la sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session

## Crear rutas para clientes ##
# - Crear cliente
# - Consultar cliente por DNI
# - Solicitar simulación de hipoteca 
#       (dado TAE y plazo de amortización, devuelve la cuota mensual y el importe total a pagar y lo guarda en la base de datos)
# - Modificar cliente
# - Elminar cliente


def buscar_cliente_por_dni(session, cliente_dni):
    statement = select(Cliente).where(Cliente.dni == cliente_dni)
    return session.exec(statement).first()


@app.get("/")
async def get():
    return {"message": "Hello World"}


# Ruta para obtener todos los clientes
@app.get("/clientes/", response_model=list[ClienteLeer])
async def get_clients(session=Depends(get_session)):
    clientes = session.exec(select(Cliente)).all()
    return clientes


# Ruta para obtener un cliente por su DNI
@app.get("/clientes/{cliente_dni}", response_model=ClienteLeer)
def read_cliente(cliente_dni: str, session: Session = Depends(get_session)):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


# Ruta para crear un nuevo cliente
@app.post("/clientes/", response_model=ClienteLeer)
async def create_client(cliente: ClienteCrear, session=Depends(get_session)):
    validar_cliente(session, cliente)
    
    db_cliente = Cliente(**cliente.model_dump())
    
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


# Ruta para actualizar un cliente
@app.put("/clientes/{cliente_dni}", response_model=ClienteLeer)
def update_cliente(cliente_dni: str, cliente: ClienteCrear, session: Session = Depends(get_session)):
    db_client = buscar_cliente_por_dni(session, cliente_dni)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    validar_cliente(session, cliente)

    update_data = cliente.model_dump()
    for key, value in update_data.items():
        setattr(db_client, key, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


# Ruta para eliminar un cliente por su DNI
@app.delete("/clientes/{cliente_dni}")
def delete_cliente(cliente_dni: str, session: Session = Depends(get_session)):
    cliente = buscar_cliente_por_dni(session, cliente_dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(cliente)
    session.commit()
    return {"message": "Cliente eliminado correctamente"}