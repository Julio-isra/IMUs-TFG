import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. CARGAR LOS NUEVOS DATOS (Paciente Global + 6 Canales)
print("Cargando tensores de 6 canales...")
X = np.load('X_entrenamiento_6canales.npy')
Y = np.load('Y_entrenamiento_6canales.npy')

# 2. SEPARAR EN ENTRENAMIENTO Y EXAMEN (80% / 20%)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify =Y)

print(f"Datos para estudiar: {X_train.shape[0]} zancadas (Acc + Gyro).")
print(f"Datos para el examen final: {X_test.shape[0]} zancadas (Acc + Gyro).")

# 3. LA NUEVA ARQUITECTURA (Más ligera y eficiente)
print("\nConstruyendo la Red Neuronal Optimizada...")
modelo = Sequential()

# Capa LSTM: Reducida a 16 celdas (Evita memorización). 
# Lee los 180 puntos y los 6 canales (X.shape[2] ahora vale 6)
modelo.add(LSTM(16, input_shape=(X.shape[1], X.shape[2])))

# ¡Dropout eliminado por recomendación clínica/técnica!

# Capa de Decisión: 1 sola neurona (0 = Sano, 1 = Lesionado)
modelo.add(Dense(1, activation='sigmoid'))

modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
modelo.summary()

# 4. ENTRENAR LA RED
print("\nIniciando entrenamiento...")
historial = modelo.fit(X_train, Y_train, epochs=15, batch_size=64, validation_data=(X_test, Y_test))

# 5. GUARDAR EL NUEVO CEREBRO
# Le cambiamos el nombre para no machacar el que ya tenías
modelo.save('modelo_paciente_6canales.h5')
print("\n¡Modelo guardado con éxito como 'modelo_paciente_6canales.h5'!")

# 6. GRÁFICA DE APRENDIZAJE
plt.figure(figsize=(10, 5))
plt.plot(historial.history['accuracy'], label='Precisión Entrenando')
plt.plot(historial.history['val_accuracy'], label='Precisión Examen (Validación)')
plt.title('Curva de Aprendizaje - Modelo Global (6 Canales)')
plt.xlabel('Época (Iteración)')
plt.ylabel('Precisión (Accuracy)')
plt.legend()
plt.grid(True)
plt.savefig('curva_aprendizaje_v2.png')
print("Gráfica guardada como 'curva_aprendizaje_v2.png'.")