# 🏠 API de Simulación de Hipotecas
### Creada para la prueba técnica de *Roams*.

Esta API permite gestionar clientes y realizar simulaciones de hipotecas con los siguientes endpoints:
- Crear un cliente.
- Consultar los datos de un cliente por su DNI.
- Solicitar una simulación de hipoteca para un cliente dado un TAE y un plazo de amortización.
- Modificar un cliente.
- Eliminar un cliente.


## **Instalación**

1. Clona el repositorio:
   ```bash
   git clone git@github.com:dev-spmanuel/API-simulacion-hipotecas.git
   cd API-simulacion-hipotecas/

2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt

4. Para levantar la API, ejecuta:
   ```bash
   fastapi run

La API estará disponible en http://127.0.0.1:8000 por defecto.

>[!NOTE]
>  #### Puedes importar la colección de Postman con los endpoints de la API desde el archivo [SimulacionHipotecas.postman_collection.json](utils/SimulacionHipotecas.postman_collection.json), incluido en este repositorio.
