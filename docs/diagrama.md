graph TD
    subgraph Fase 1: Preprocesamiento
        A((Corredor + IMU)) --> B[Scripts de MATLAB]
        B --> C{141 GB JSONs + CSV}
    end

    subgraph Fase 2: Ingeniería de Datos
        C --> D[dataset.py <br> Fusión a 6 Canales]
        D --> E[(Tensores .npy <br> X, Y, IDs)]
    end

    subgraph Fase 3: Inteligencia Artificial
        E --> F[entrenamiento.py <br> Stratified K-Fold]
        F --> G[[modelo_mejor.h5]]
    end

    subgraph Fase 4: Servidor y Web
        G -. Carga en RAM .-> H[main.py <br> Servidor FastAPI]
        H <--> I[/Interfaz Web del Médico/]
    end