# Informe de estado

1\. Arquitectura del Sistema
Has abandonado la rigidez de las apps móviles tradicionales para construir una arquitectura moderna Cliente-Servidor (Web App):
&#x20;   Backend (Servidor): Programado en Python con FastAPI. Es un servidor ultrarrápido que se encarga de buscar en tu disco duro (entre los 13 GB de base de datos) el archivo JSON del paciente solicitado y enviarlo a la web.
&#x20;   Frontend (Cliente): Una interfaz web construida con HTML5, JavaScript y Bootstrap 5. Es totalmente responsiva, por lo que el médico puede verla en el monitor del ordenador o en la pantalla de su teléfono móvil conectado al mismo Wi-Fi.
&#x20;   Control de Versiones: El código está correctamente estructurado y subido a GitHub, manteniendo el .gitignore configurado para proteger la nube de los archivos pesados (JSON) y temporales (\_\_pycache\_\_).
2\. Interfaz y Experiencia de Usuario (Dashboard)
&#x20;   Buscador Inteligente: Una barra de búsqueda donde el clínico introduce el ID del paciente (ej: 20090527T000000). El sistema tiene prevención de errores: avisa si la caja está vacía o si el paciente no existe en la base de datos.
&#x20;   Tabla de Metadatos Clínicos: Un panel superior que lee el archivo JSON y extrae parámetros clave del experimento de forma automática:
&#x20;       Frecuencia de Muestreo (Hz): Ej. 200 Hz.
&#x20;       Pasos Anómalos (Outliers): La cantidad de pasos erróneos que el script de MATLAB detectó y purgó.

&#x20;       Pasos Válidos Analizados: El recuento de las zancadas perfectas que se van a dibujar.



3\. Motor de Visualización (Dashboard Dual)



Has implementado Chart.js para renderizar un cuadro de mando con dos tarjetas gráficas independientes y sincronizadas con los datos:



&#x20;   Gráfica 1 (Acelerómetro): Mide impactos y fuerza lineal en m/s².



&#x20;   Gráfica 2 (Giroscopio): Mide rotación articular en deg/s (grados por segundo).



&#x20;   Menús Desplegables Inteligentes: La web lee dinámicamente el JSON para saber qué partes del cuerpo están disponibles. Protege al usuario de errores sabiendo que la aceleración solo tiene 7 segmentos (ej: pies, tibias, muslos, pelvis) mientras que el giroscopio tiene 13 (añadiendo rodillas, tobillos y caderas).



4\. Modos de Análisis Biomecánico (El núcleo de tu TFG)



Cada gráfica tiene un selector para alternar entre dos visiones matemáticas diferentes de los mismos datos:



&#x20;   Modo 1: Continuo (Dominio Temporal)



&#x20;       Muestra la prueba completa paso tras paso.



&#x20;       Diseño con Scroll Horizontal dinámico: la gráfica crece de tamaño según la cantidad de pasos para que el usuario pueda deslizar con el dedo.



&#x20;       Técnicamente, representa pasos interpolados por MATLAB a 180 muestras (lo que equivale a 0.9 segundos por paso físico). Útil para ver asimetrías temporales o desgaste/fatiga a lo largo de la prueba.



&#x20;   Modo 2: Media + Sombra (Dominio del Ciclo de Marcha)



&#x20;       Normaliza todos los pasos temporalmente del 0% al 100% del ciclo de marcha.



&#x20;       Línea central (Media): Calcula y dibuja el promedio matemático en cada instante, obteniendo el "Paso Patrón" o huella biomecánica del paciente.



&#x20;       Envolvente / Sombra (Variabilidad): Calcula los Percentiles 10 y 90 de todos los pasos para dibujar una franja de color semitransparente. Representa el margen de error o la inestabilidad del paciente (si la sombra es ancha, el paciente tiene un control motor pobre; si es estrecha, su pisada es estable y repetitiva).

