import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt

# ============================================================
# 1. CARGA DE DATOS
# ============================================================
print("Cargando tensores...")
X = np.load('X_entrenamiento_2.npy')
Y = np.load('Y_entrenamiento_2.npy')
IDs = np.load('ID_entrenamiento_6canales.npy')

# Verificación de forma y rango de valores (IMPORTANTE)
print(f"Forma de X: {X.shape}")  # Debería ser (muestras, pasos, canales)
print(f"Rango de valores en X: [{np.min(X):.2f}, {np.max(X):.2f}]")
print(f"Distribución de clases: Sanos={np.sum(Y==0)} ({np.mean(Y==0)*100:.1f}%), Lesionados={np.sum(Y==1)} ({np.mean(Y==1)*100:.1f}%)")

# ============================================================
# 2. NORMALIZACIÓN (Z-Score por canal)
# ============================================================
# Calculamos media y desviación sobre TODOS los datos de entrenamiento
# (esto se hace antes de la validación cruzada para evitar fugas)
mean = np.mean(X, axis=(0, 1), keepdims=True)
std = np.std(X, axis=(0, 1), keepdims=True)
X = (X - mean) / (std + 1e-8)  # evitamos división por cero
print("Datos normalizados (media=0, std=1 por canal).")

# ============================================================
# 3. FÁBRICA DE MODELOS (ARQUITECTURA MEJORADA)
# ============================================================
def crear_modelo():
    """
    Construye un modelo LSTM más profundo:
    - Input explícito (corrige el warning)
    - Dos capas LSTM (64 → 32)
    - Capa densa intermedia con ReLU
    - Salida sigmoide para clasificación binaria
    """
    modelo = Sequential([
        Input(shape=(X.shape[1], X.shape[2])),   # (time_steps, features)
        LSTM(64, return_sequences=True),         # Primera LSTM, devuelve secuencia
        LSTM(32),                                # Segunda LSTM, solo último estado
        Dense(16, activation='relu'),            # Capa oculta no lineal
        Dense(1, activation='sigmoid')           # Salida binaria
    ])
    modelo.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return modelo

# ============================================================
# 4. CONFIGURACIÓN DE VALIDACIÓN CRUZADA
# ============================================================
N_SPLITS = 5
sgkf = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=42)

precisiones_examenes = []
mejor_precision = 0.0

print("\n=== INICIANDO VALIDACIÓN CRUZADA (5 FOLDS) ===")

# ============================================================
# 5. BUCLE PRINCIPAL DE ENTRENAMIENTO / EVALUACIÓN
# ============================================================
for fold, (train_idx, test_idx) in enumerate(sgkf.split(X, Y, groups=IDs)):
    print(f"\n--- Entrenando Fold {fold + 1}/{N_SPLITS} ---")

    # Separar datos del fold actual
    X_train, X_test = X[train_idx], X[test_idx]
    Y_train, Y_test = Y[train_idx], Y[test_idx]

    # Calcular pesos de clase para compensar desbalanceo
    clases = np.unique(Y_train)
    pesos = compute_class_weight(class_weight='balanced', classes=clases, y=Y_train)
    class_weight_dict = dict(zip(clases, pesos))
    print(f"  Pesos de clase: {class_weight_dict}")

    # Crear modelo nuevo (pesos aleatorios)
    modelo = crear_modelo()

    # Entrenamiento
    modelo.fit(
        X_train, Y_train,
        epochs=20,                  # Un poco más de épocas
        batch_size=64,
        class_weight=class_weight_dict,
        verbose=0                   # Silencioso para no saturar la consola
    )

    # Evaluación sobre el conjunto de prueba (pacientes no vistos)
    resultados = modelo.evaluate(X_test, Y_test, verbose=0)
    precision_actual = resultados[1] * 100
    print(f"  Precisión en Fold {fold + 1}: {precision_actual:.2f}%")

    precisiones_examenes.append(precision_actual)

    # Guardar el mejor modelo encontrado hasta ahora
    if precision_actual > mejor_precision:
        mejor_precision = precision_actual
        modelo.save('modelo_paciente_mejor.keras')  # Formato nativo Keras (recomendado)
        print(f"  → Nuevo mejor modelo guardado (Fold {fold + 1}).")

# ============================================================
# 6. RESULTADOS FINALES
# ============================================================
media = np.mean(precisiones_examenes)
desviacion = np.std(precisiones_examenes)

print("\n================================================")
print("🏆 RESULTADOS FINALES DE LA VALIDACIÓN CRUZADA")
print("================================================")
print(f"Precisión Media: {media:.2f}% (± {desviacion:.2f}%)")
print("================================================")
print("Mejor modelo guardado como 'modelo_paciente_mejor.keras'")