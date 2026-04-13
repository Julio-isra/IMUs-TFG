import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. CARGAR LOS DATOS
print("Cargando tensores, los archibos npy")
X = np.load('X_entrenamiento.npy')
Y = np.load('Y_entrenamiento.npy')

# 2. SEPARAR EN ENTRENAMIENTO Y EXAMEN (80% / 20%)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print(f"Datos para estudiar: {X_train.shape[0]} zancadas.")
print(f"Datos para el examen final: {X_test.shape[0]} zancadas.")

# 3. CONSTRUIR LA ARQUITECTURA LSTM
print("\nConstruyendo la Red Neuronal...")
modelo = Sequential()

# Capa LSTM: 64 celdas de memoria. Le decimos la forma exacta de un paso (180, 3)
modelo.add(LSTM(16, input_shape=(X.shape[1], X.shape[2])))

# Capa Dropout (Apaga el 50% de las neuronas al azar para evitar que memoricen / over-fitting)
# modelo.add(Dropout(0.5))

# Capa de Decisión: 1 sola neurona con activación 'sigmoid' (escanea el resumen y da un % de lesión)
modelo.add(Dense(1, activation='sigmoid'))

# Compilar el modelo (Le enseñamos cómo medir sus propios errores)
modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
modelo.summary()

# 4. ENTRENAR LA RED 
print("\nIniciando entrenamiento...")
# Epochs = Cuántas veces se va a leer el libro entero.
historial = modelo.fit(X_train, Y_train, epochs=15, batch_size=64, validation_data=(X_test, Y_test))

# 5. GUARDAR EL CEREBRO ENTRENADO
modelo.save('modelo_lesiones_lstm.h5')
print("\n¡Modelo guardado con éxito como 'modelo_lesiones_lstm.h5'!")

# 6. DIBUJAR LA GRÁFICA DE APRENDIZAJE (Para la memoria de tu TFG)
plt.figure(figsize=(10, 5))
plt.plot(historial.history['accuracy'], label='Precisión Entrenando')
plt.plot(historial.history['val_accuracy'], label='Precisión Examen (Validación)')
plt.title('Curva de Aprendizaje de la Red LSTM')
plt.xlabel('Época (Iteración)')
plt.ylabel('Precisión (Accuracy)')
plt.legend()
plt.grid(True)
plt.savefig('curva_aprendizaje.png')
print("Gráfica guardada como 'curva_aprendizaje.png'.")