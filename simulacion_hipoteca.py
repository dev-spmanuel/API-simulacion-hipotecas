from datetime import datetime
from sqlmodel import Session
from models import SimulacionHipoteca


class CalculadorSimulacionHipoteca:
    """
    Calcula la cuota mensual y el importe total de una hipoteca para un cliente.

    Args:
        capital (float): El capital solicitado.
        interes (float): El interés anual.
        plazo (int): El plazo en años.
    """

    def __init__(self, capital: float, interes: float, plazo: int):
        self.capital = capital
        self.interes = interes
        self.plazo = plazo

    def _calcular_hipoteca(self):

        # Calcular el interés mensual y el número total de meses
        i = self.interes / 100 / 12
        n = self.plazo * 12

        # Calcular la cuota mensual
        cuota_mensual = self.capital * i / (1 - (1 + i) ** -n)

        # Calcular el importe total a devolver
        importe_total = cuota_mensual * n

        # Devolver la cuota y el importe total redondeados a 2 decimales
        return round(cuota_mensual, 2), round(importe_total, 2)


    def crear_simulacion(self, session: Session, cliente_id: int):

        # Calcular los valores de la simulación
        cuota_mensual, importe_total = self._calcular_hipoteca()

        # Crear una nueva simulación
        simulacion = SimulacionHipoteca(
            cliente_id=cliente_id,
            cuota_mensual=cuota_mensual,
            importe_total=importe_total,
            plazo=self.plazo,
            interes=self.interes,
            fecha_simulacion=datetime.now()
        )

        # Guardar la simulación en la base de datos
        session.add(simulacion)
        session.commit()
        session.refresh(simulacion)
        return simulacion