% exportador_app.m
clear; clc;

% 1. Definimos de dónde leemos y dónde guardamos
carpeta_origen = 'D:\Universidad\TFG\IMU_segm_sync'; %  datos ya procesados
carpeta_destino = 'D:\Universidad\TFG\IMU_App_JSON'; % Carpeta nueva para App

% Crea la carpeta nueva si no existe
if ~exist(carpeta_destino, 'dir')
    mkdir(carpeta_destino);
end

% Buscamos todos los archivos .mat
files = dir([carpeta_origen '/*.mat']);

disp(['Comenzando exportación de ' num2str(length(files)) ' pacientes...']);

% 2. Bucle rápido de conversión
for i = 1:length(files)
    
    % Carga silenciosamente el paciente (variable 'Subject')
    load(fullfile(files(i).folder, files(i).name));
    
    % Estructura de MATLAB a texto JSON
    texto_json = jsonencode(Subject);
    
    % Cambiamos la extensión del nombre de .mat a .json
    nuevo_nombre = strrep(files(i).name, '.mat', '.json');
    ruta_guardado = fullfile(carpeta_destino, nuevo_nombre);
    
    % Creamos el archivo y guardamos el texto dentro
    fid = fopen(ruta_guardado, 'w');
    fprintf(fid, '%s', texto_json);
    fclose(fid);
    
    % Barra de progreso cada 100 archivos
    if mod(i, 100) == 0
        disp(['Exportados ' num2str(i) ' de ' num2str(length(files))]);
    end
end

disp('¡BINGO! Exportación completada. Ya tienes los datos listos para tu App Móvil.');