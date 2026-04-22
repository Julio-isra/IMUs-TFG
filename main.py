import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
from tensorflow.keras.models import load_model
import json
from fastapi.responses import JSONResponse

app = FastAPI()

# --- CARGAMOS EL MODELO LSTM ---
try:
    modelo_ia = load_model('LSTM/modelo_lesiones_lstm.h5')
    print("---- Modelo LSTM cargado correctamente. ----")
except Exception as e:
    print("---- Error al cargar el modelo: ", e)
    modelo_ia = None

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
    
    # 1. Leemos el contenido del JSON
    with open(ruta_completa, 'r') as f:
        datos_paciente = json.load(f)
    
    # 2. Iniciamos variables de diagnóstico por defecto
    diagnostico = "No evaluable"
    probabilidad = 0.0

    # 3. Procesamos con la IA si hay datos del pie izquierdo
    # Accedemos a la representación de la señal procesada sin outliers
    try:
        pasos = datos_paciente['acc_interp_nooutliers'].get('L_foot', [])
        
        if modelo_ia and len(pasos) > 0:
            # Convertimos los pasos a una matriz (tensor) para la red neuronal
            X_input = np.array(pasos) # Forma: (N_pasos, 180, 3)
            
            # La red predice la etiqueta usando una capa final de regresión logística [cite: 7]
            predicciones = modelo_ia.predict(X_input, verbose=0)
            
            # Calculamos la media de riesgo entre todas las zancadas detectadas
            riesgo_medio = float(np.mean(predicciones))
            probabilidad = round(riesgo_medio * 100, 2)
            
            # Clasificación binaria: 1 para lesionado, 0 para sano [cite: 5, 7]
            if riesgo_medio >= 0.5:
                diagnostico = "Lesionado"
            else:
                diagnostico = "Sano"
                
    except KeyError:
        pass # El archivo no tiene el formato esperado para la IA

    # 4. Inyectamos los resultados de la IA en los datos que enviamos a la web
    datos_paciente['ia_diagnostico'] = diagnostico
    datos_paciente['ia_probabilidad'] = probabilidad
    
    # Devolvemos el JSON completo modificado
    return datos_paciente