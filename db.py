from sqlmodel import SQLModel, create_engine, select
from models import Cliente


# Configurar la base de datos SQLite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Crear las tablas en la base de datos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Función para buscar un cliente por su DNI
def buscar_cliente_por_dni(session, cliente_dni):
    statement = select(Cliente).where(Cliente.dni == cliente_dni)
    return session.exec(statement).first()