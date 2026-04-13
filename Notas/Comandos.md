Servidor:

* Activar entorno: entorno_tfg\Scripts\activate
* Desactivar entorno: deactivate
* Arrancar servidor: uvicorn main:app --reload
                     uvicorn main:app --host 0.0.0.0 --port 8000 --reload

APP:

* Activar app: flutter run
* Actualiazar app: r
* Reiniciar: R
* Cerrar: q

pasar de pagina a pagina a scroll --------------------- Hecho
desviacion estandar, envolvente, paso mediano, los percentiles (10,90 o 25,75) para que se vea sombra ------- hecho
    hacemos los percentiles con la media, El 0% es el instante exacto en el que el talón izquierdo choca contra el suelo (TouchDown).
    El 100% es el instante en el que ese mismo talón izquierdo vuelve a chocar contra el suelo tras haber dado la zancada.
    
estudiar si seguimos con app o vamos a web movil --------------- hecho web movil 

estudiar clasificador para el estilo de carrera ------- 

añadir los datos para giroscopio igual que la aceleracion ----------- Hecho


en el scroll no esta de sincronizado por el filtro de pasos falsos
hay que representar todos por separado: L_foot y R_foot: Pies izquierdo y derecho.
    L_shank y R_shank: Espinillas/Tibias izquierda y derecha.
    L_thigh y R_thigh: Muslos/Fémures izquierdo y derecho.
    Pelvis: El centro de gravedad, en la baja espalda.

DATOS DEL script de matlab:
------------------
    - Acelerómetro: Mide fuerzas lineales, impactos contra el suelo y la gravedad en m/s2. Lo que ddibujamos ahora
    - Giroscopio: Mide la velocidad angular (cuántos grados por segundo está girando ese hueso). Es vital para ver si el paciente tuerce el tobillo al aterrizar (pronación/supinación) o si gira demasiado la cadera.
------------------
    -Segementos corporales
------------------
    - Cinematica: joint_angles (no lo encuentro)
------------------
    - Frecuencia de muestreo 
    - Outliers: : La lista negra de los pasos que el paciente dio mal y que MATLAB borró de la matriz de "pasos perfectos".

    20090527T000000


---------------------------------------------------------------------------
continuo los datos en bruto, sin outliers, pero el paso mediano(media) y medio con outliers, desviacion estar afura-----------------hecho
25-75 primer segundo y tercer cuartil

en python aparte en un fichero aparte generar redes neuronales, 
entrenar el modelo en local y cargar a la wevb y solo dar respuesta a la web 
hay que subir el modelo ya entrenado con los datos de ferber. 
el modelo que solo diga si esta lesionado o no lesionado/ o si se puede para estilo de carrerar

lstm ----> porque tenemos que tener en cuenta el tiempo, ya que en las redes neuronales tipicas no lo tiene en cuenta. Aunque estan las RNN que tienen memoria pero tienen mala memoria a largo plazo
auto encoder

https://ieeexplore.ieee.org/document/7837994 abrir desde myapps

https://bitbucket.org/bookcold/pretraining_lstm/src/master/


preguntar si el modelo se tiene que hacer con los pasos sin outliers o con, sin pasos invalidos o con los invalidos tambien
Posibles mejoras:

    Añadir más capas LSTM (apiladas) con return_sequences=True para aprender jerarquías temporales.

    Añadir batch normalization.

    Ajustar la tasa de dropout (0.5 es alta; a veces 0.2-0.3 funciona mejor).

    Probar con GRU (menos parámetros, igual rendimiento a veces).

    Usar early stopping para no sobreentrenar.



-------------------------------------------------------------------------------------

mirar los test y entrenamiento no coger solo izq y hacer el examen solo con derecha, también no entrenar con 90% enferomos y examen 10% sanos

Matlab estraficada stratify 

meter aceleromet4ro y giroscopio y seguramente me salgra mas ejes 

bajar celdas en el modelo 8, 16 etc 64 es mucho

dependiente de lados o por paciente el dataset. respuesta final para el sujeto

esquema de cada script explicando todo, entradas, que hago con eso, para que donde lo uso, y conexiones con otros script