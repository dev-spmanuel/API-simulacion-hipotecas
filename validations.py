from schemas import ClienteCrear
from fastapi import HTTPException
from sqlmodel import select
from models import Cliente


def validar_dni(dni: str) -> bool:
    """
    Valida un DNI español siguiendo el algoritmo oficial.
    Args:
        dni (str): DNI en formato '12345678A'.
    Returns:
        bool: True si es válido, False en caso contrario.
    """
    # Tabla de letras oficiales
    letras_dni = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    # Comprobar que el formato sea correcto (8 dígitos + 1 letra)
    if len(dni) != 9 or not dni[:-1].isdigit() or not dni[-1].isalpha():
        return False
    
    # Separar los números y la letra
    numeros = int(dni[:-1])
    letra = dni[-1].upper()  # Convertir la letra a mayúsculas
    
    # Calcular la letra correspondiente
    letra_calculada = letras_dni[numeros % 23]
    
    # Verificar si la letra es correcta
    return letra == letra_calculada


def validar_cliente(session, cliente: ClienteCrear):
    # Verificar si el email ya está en uso
    email_exists = select(Cliente).where(Cliente.email == cliente.email)
    existing_email = session.exec(email_exists).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="El email ya está en uso")

    # Verificar si el DNI ya está en uso
    dni_exists = select(Cliente).where(Cliente.dni == cliente.dni)
    existing_dni = session.exec(dni_exists).first()
    if existing_dni:
        raise HTTPException(status_code=400, detail="El DNI ya está en uso")

    if not validar_dni(cliente.dni):
        raise HTTPException(status_code=400, detail="DNI no válido")