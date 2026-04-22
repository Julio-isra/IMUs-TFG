import numpy as np
import matplotlib.pyplot as plt

# 1. Cargar el tensor de etiquetas
print("Cargando datos...")
Y = np.load('Y_entrenamiento_2.npy')

# 2. Contar cuántos hay de cada clase
total_zancadas = len(Y)
sanos = np.sum(Y == 0)
lesionados = np.sum(Y == 1)

# 3. Calcular porcentajes matemáticos
porcentaje_sanos = (sanos / total_zancadas) * 100
porcentaje_lesionados = (lesionados / total_zancadas) * 100

# 4. Imprimir el boletín en la terminal
print("\n=================================")
print("📊 ANÁLISIS DEL DATASET")
print("=================================")
print(f"Total de zancadas procesadas: {total_zancadas}")
print(f"✅ Sanos (Etiqueta 0):     {sanos} zancadas ({porcentaje_sanos:.2f}%)")
print(f"⚠️ Lesionados (Etiqueta 1): {lesionados} zancadas ({porcentaje_lesionados:.2f}%)")
print("=================================\n")
