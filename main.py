import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 1. Datos JSON
CARPETA_DATOS = r"D:\Universidad\TFG\IMU_App_JSON" 

# 2. Le decimos a FastAPI que sirva la página web desde la carpeta "static"
app.mount("/web", StaticFiles(directory="static", html=True), name="static")

# 3. Pagina principal
@app.get("/")
def ruta_principal():
    return RedirectResponse(url="/web/")

# 4. Tu tubería de datos intacta (El almacén de JSONs)
@app.get("/paciente/{nombre_archivo}")
def obtener_paciente(nombre_archivo: str):
    if not nombre_archivo.endswith('.json'):
        nombre_archivo += '.json'
        
    ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
    
    if not os.path.exists(ruta_completa):
        raise HTTPException(status_code=404, detail="Datos del paciente no encontrados")
    
    return FileResponse(ruta_completa, media_type="application/json")