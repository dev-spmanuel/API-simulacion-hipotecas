from sqlmodel import Field, SQLModel, create_engine, select

## VALIDAR DATOS, DNI... ##

class Cliente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, nullable=False)
    dni: str = Field(unique=True, max_length=9, nullable=False)
    email: str = Field(unique=True, nullable=False)
    capital_solicitado: float = Field(default=0.0, nullable=False)


# Configurar la base de datos SQLite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Crear las tablas en la base de datos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)