from sqlmodel import SQLModel, create_engine, Session


# Configurar la base de datos SQLite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Crear las tablas en la base de datos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Dependencia para la sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session