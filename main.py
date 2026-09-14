import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
from tensorflow.keras.models import load_model
import json

app = FastAPI()

# --- CARGA DEL MODELO LSTM AL SERVIDOR ---
try:
    modelo_ia = load_model('LSTM/modelo_lesiones_lstm.h5')
    print("---- Modelo LSTM cargado correctamente. ----")
except Exception as e:
    print("---- Error al cargar el modelo: ", e)
    modelo_ia = None

# Datos JSON (RUATA LOCAL)
CARPETA_DATOS = r"D:\Universidad\TFG\IMU_App_JSON"

# ASIGNACIOÓN DE RUTA PARA EL HTML (CARPETTA: STATIC)
app.mount("/web", StaticFiles(directory="static", html=True), name="static")

# Pagina principal (RUTA)
@app.get("/")
def ruta_principal():
    return RedirectResponse(url="/web/")

# SOLICITUD DE DATOS DEL PACIENTE SOLICITADO (JSON)
@app.get("/paciente/{nombre_archivo}")
def obtener_paciente(nombre_archivo: str):
    # VALIDACION DEL NOMBRE DEL ARCHIVO (PACIENTE)
    if not nombre_archivo.endswith('.json'):
        nombre_archivo += '.json'
    
    # RUTA LOCAL DEL JSON DEL PACIENTE
    ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
    
    if not os.path.exists(ruta_completa):
        raise HTTPException(status_code=404, detail="Datos del paciente no encontrados")
    
    # LECTURA DEL CONTENIDO DEL JSON
    with open(ruta_completa, 'r') as f:
        datos_paciente = json.load(f)
    
    # Iniciamos variables de diagnóstico por defecto
    diagnostico = "No evaluable"
    probabilidad = 0.0

#### ¡¡¡¡¡¡¡¡¡¡ REVISAR POR QUE SE USA SOLO EL PIE IZQUIERDO !!!!!!!!!!!!  
 
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

    # ENVIAMOS LOS RESULTADOS DEL MODELO AL USARIO 
    datos_paciente['ia_diagnostico'] = diagnostico
    datos_paciente['ia_probabilidad'] = probabilidad
    
    # Devolvemos el JSON completo modificado
    return datos_paciente