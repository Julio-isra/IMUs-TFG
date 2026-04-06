import pandas as pd
import numpy as np
import json
import os
from tqdm import tqdm  
# ==========================================
# CONFIGURACIÓN DE RUTAS
# ==========================================
RUTA_CSV = r'D:\TFG\CSV\run_data_meta.csv'
CARPETA_JSONS = r'D:\TFG\IMU_App_JSON/'

print("1. Leyendo el diccionario clínico (CSV) y calculando pies...")
df = pd.read_csv(RUTA_CSV)

# ==========================================
# PASO 1: LÓGICA INTELIGENTE DE EXTRACCIÓN
# ==========================================
diccionario_pacientes = {}

for index, fila in df.iterrows():
    filename = str(fila['filename']).strip()
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Comprobamos si está sano
    es_sano = str(fila['InjDefn']).strip().lower() == 'no injury'
    
    pies_a_extraer = {} # Guardaremos qué pie sacar y qué etiqueta ponerle
    
    if es_sano:
        # Si está sano, AMBOS pies nos sirven como datos perfectos (0)
        pies_a_extraer['L_foot'] = 0
        pies_a_extraer['R_foot'] = 0
    else:
        # Si está lesionado, leemos los lados de las lesiones
        lado1 = str(fila['InjSide']).strip().lower()
        # Usamos .get() por si la columna InjSide2 no existe en tu CSV, que no dé error
        lado2 = str(fila.get('InjSide2', '')).strip().lower() 
        
        # Lógica para el Pie Izquierdo
        if 'left' in lado1 or 'left' in lado2 or 'bilateral' in lado1 or 'bilateral' in lado2:
            pies_a_extraer['L_foot'] = 1
            
        # Lógica para el Pie Derecho
        if 'right' in lado1 or 'right' in lado2 or 'bilateral' in lado1 or 'bilateral' in lado2:
            pies_a_extraer['R_foot'] = 1

    diccionario_pacientes[filename] = pies_a_extraer

print(f"-> Reglas de extracción creadas para {len(diccionario_pacientes)} pacientes.")

# ==========================================
# PASO 2: EXTRACCIÓN CON BARRA DE PROGRESO
# ==========================================
print("\n2. Extrayendo los ciclos de marcha de los 141 GB de archivos JSON...")
X_lista = []
Y_lista = []

# Listamos solo los archivos .json
archivos_en_carpeta = [f for f in os.listdir(CARPETA_JSONS) if f.endswith('.json')]

# Aquí está la magia: envolvemos la lista con tqdm()
for archivo in tqdm(archivos_en_carpeta, desc="Procesando pacientes", unit="archivos"):
    if archivo in diccionario_pacientes:
        reglas_pies = diccionario_pacientes[archivo] # Ej: {'L_foot': 1, 'R_foot': 1}
        
        # Si no hay pies que extraer (un caso raro), pasamos al siguiente
        if not reglas_pies: 
            continue
            
        ruta_completa = os.path.join(CARPETA_JSONS, archivo)
        
        try:
            with open(ruta_completa, 'r') as f:
                datos = json.load(f)
                
                # Buscamos cada pie que nos haya dicho el diccionario
                for nombre_pie, etiqueta in reglas_pies.items():
                    try:
                        pasos_validos = datos['acc_interp_nooutliers'][nombre_pie]
                        for paso in pasos_validos:
                            X_lista.append(paso)
                            Y_lista.append(etiqueta)
                    except KeyError:
                        # Si justo a este paciente le falta ese pie en el JSON, lo ignoramos
                        pass
        except Exception as e:
            # Si un archivo JSON está corrupto o no se puede leer
            pass

# ==========================================
# PASO 3: CREAR LOS TENSORES
# ==========================================
print("\n3. Convirtiendo a tensores matemáticos y guardando...")
X_tensor = np.array(X_lista)
Y_tensor = np.array(Y_lista)

print("\n==========================================")
print(f"FORMA DE X (Datos): {X_tensor.shape}")
print(f"FORMA DE Y (Etiquetas): {Y_tensor.shape}")
print("==========================================")

np.save('X_entrenamiento.npy', X_tensor)
np.save('Y_entrenamiento.npy', Y_tensor)

print("\n¡Proceso completado! Archivos .npy generados con éxito.")