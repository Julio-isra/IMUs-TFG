import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt

# ==========================================
# BLOQUE 1: CARGA DE DATOS
# ==========================================
print("Cargando tensores desde el disco...")
X = np.load('X_entrenamiento_2.npy')
Y = np.load('Y_entrenamiento_2.npy')
IDs = np.load('ID_entrenamiento_6canales.npy')

print(f"Forma de X (Zancadas, Muestras, Canales): {X.shape}")
print(f"Total de etiquetas Y: {Y.shape}")
print(f"Total de IDs de pacientes: {IDs.shape}\n")

# ==========================================
# BLOQUE 2: FÁBRICA DE CEREBROS (MODELO)
# ==========================================
def crear_modelo():
    modelo = Sequential()
    # Estilo moderno: Definimos la entrada por separado
    modelo.add(Input(shape=(X.shape[1], X.shape[2]))) 
    # Memoria a corto-largo plazo (ampliada a 32 neuronas)
    modelo.add(LSTM(32)) 
    # Decisión final (0 a 1)
    modelo.add(Dense(1, activation='sigmoid'))
    
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return modelo

# ==========================================
# BLOQUE 3: EL ORGANIZADOR (K-FOLD) Y ENTRENAMIENTO
# ==========================================
# Preparamos los 5 exámenes, aislando a los pacientes y manteniendo la proporción sano/lesionado
sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)

precisiones_examenes = []
mejor_precision = 0

print("=== INICIANDO VALIDACIÓN CRUZADA (5 FOLDS) ===")

for fold, (train_idx, test_idx) in enumerate(sgkf.split(X, Y, groups=IDs)):
    print(f"\n--- Entrenando Fold {fold + 1}/5 ---")
    
    # Repartimos los apuntes y los exámenes físicos
    X_train, X_test = X[train_idx], X[test_idx]
    Y_train, Y_test = Y[train_idx], Y[test_idx]
    
    # 1. Calculamos los pesos justos para que la IA no sea perezosa
    pesos = compute_class_weight('balanced', classes=np.unique(Y_train), y=Y_train)
    pesos_diccionario = {0: pesos[0], 1: pesos[1]}
    print(f"Pesos de atención -> Sanos (0): {pesos[0]:.2f}x | Lesionados (1): {pesos[1]:.2f}x")
    
    # 2. Pedimos un cerebro nuevo y reseteado
    modelo = crear_modelo()
    
    # 3. ¡A estudiar! Le pasamos los pesos y aumentamos el tiempo a 40 épocas
    modelo.fit(
        X_train, Y_train, 
        epochs=40, 
        batch_size=64, 
        class_weight=pesos_diccionario, 
        verbose=0
    )
    
    # 4. ¡El Examen!
    resultados = modelo.evaluate(X_test, Y_test, verbose=0)
    precision_actual = resultados[1] * 100
    precisiones_examenes.append(precision_actual)
    print(f"Precisión en el examen del Fold {fold + 1}: {precision_actual:.2f}%")
    
    # 5. Guardar el trofeo si es la mejor nota hasta ahora (en formato .keras)
    if precision_actual > mejor_precision:
        mejor_precision = precision_actual
        modelo.save('modelo_paciente_6C_mejor.keras')
        print("   -> ¡Nuevo récord! Modelo guardado.")

# ==========================================
# BLOQUE 4: BOLETÍN DE NOTAS FINAL
# ==========================================
media = np.mean(precisiones_examenes)
desviacion = np.std(precisiones_examenes)

print("\n================================================")
print("🏆 RESULTADOS FINALES DE LA VALIDACIÓN CRUZADA")
print("================================================")
print(f"Precisión Media: {media:.2f}% (± {desviacion:.2f}%)")
print("================================================\n")