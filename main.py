import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

# 1. ¡ATENCIÓN! Pon aquí la ruta exacta donde están tus 13 GB de JSONs
CARPETA_DATOS = r"D:\Universidad\TFG\IMU_App_JSON" 

@app.get("/")
def ruta_principal():
    return {"mensaje": "Servidor IMU TFG funcionando correctamente."}

# 2. Creamos la ruta dinámica para pedir pacientes
@app.get("/paciente/{nombre_archivo}")
def obtener_paciente(nombre_archivo: str):
    
    # Por si a la app se le olvida poner el ".json" al final, se lo ponemos nosotros
    if not nombre_archivo.endswith('.json'):
        nombre_archivo += '.json'
        
    # Unimos la ruta de la carpeta con el nombre del archivo
    ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
    
    # Comprobamos si el archivo existe en tu disco duro
    if not os.path.exists(ruta_completa):
        # Si alguien pide un paciente que no existe, damos error 404
        raise HTTPException(status_code=404, detail="Datos del paciente no encontrados")
    
    # 3. La magia: Enviamos el archivo directamente sin cargarlo en RAM
    return FileResponse(ruta_completa, media_type="application/json")