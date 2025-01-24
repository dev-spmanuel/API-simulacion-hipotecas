from fastapi import FastAPI

from db.db import create_db_and_tables

from routes import clients


# Crear la base de datos y las tablas
create_db_and_tables()


app = FastAPI()

# Incluir las rutas de clientes
app.include_router(clients.router)


@app.get("/")
async def root():
    return {"message": "API de generación de simulaciones de hipotecas"}