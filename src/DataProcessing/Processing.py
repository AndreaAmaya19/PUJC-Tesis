import pandas as pd
import numpy as np

# Luego de unificar los archivos por año proporcionados por la SDS
# y de agregar la UPZ correspondiente a las coordenadas, el procesamiento es:

file_path = '/content/drive/MyDrive/Proyecto de grado/Datos_sds/Plantilla_72_V3_Ajus.txt'

# Leer el archivo
all_dbs_combined = pd.read_csv(file_path, delimiter='|')

# Quitar duplicados, el codigo de incidente debe ser unico
all_dbs_combined = all_dbs_combined.drop_duplicates(subset=['cod_incidente', 'hora_fecha_inicial'])

# Remover registros sin coordenadas, aprox 13% del total. 
all_dbs_combined = all_dbs_combined.dropna(subset=['X_COORD'])

# ========================================================= #
# Incluir datos de fuentes secundarias
# ========================================================= #

# ----- Población por UPZ
pop = '/content/drive/MyDrive/Proyecto de grado/Datos_sds/Poblacion_UPZs.csv'
pop_df = pd.read_csv(pop, delimiter=',', encoding='UTF-8')

# Extraer año
all_dbs_combined['year'] = all_dbs_combined['hora_fecha_inicial'].dt.year

# Convertir 'Cod_UPZ' a tipo de cadena (string)
all_dbs_combined['Cod_UPZ'] = all_dbs_combined['Cod_UPZ'].astype(str)
pop_df['UPZ'] = pop_df['UPZ'].astype(str)

# Merge
all_dbs_combined = pd.merge(all_dbs_combined, pop_df,
    left_on=['year', 'Cod_UPZ'],
    right_on=['AÑO', 'UPZ'],
    how='left'
)

# ----- Eventos especiales
eventos_esp = f"/content/drive/MyDrive/Proyecto de grado/Datos_sds/eventos_final_V3.csv"
eventos_esp_df = pd.read_csv(eventos_esp, delimiter=';')

# Columna fecha en el formato datetime
all_dbs_combined['hora_fecha_inicial'] = pd.to_datetime(all_dbs_combined['hora_fecha_inicial'])
eventos_esp_df['FECHA_INICIO'] = pd.to_datetime(eventos_esp_df['FECHA_INICIO'])

# Crear las columnas 'year_month_day' en ambas bases de datos
all_dbs_combined['year_month_day'] = all_dbs_combined['hora_fecha_inicial'].dt.strftime('%Y-%m-%d')
eventos_esp_df['year_month_day'] = eventos_esp_df['FECHA_INICIO'].dt.strftime('%Y-%m-%d')

# Convertir Cod_UPZ y COD_UPZ a str
all_dbs_combined['Cod_UPZ'] = all_dbs_combined['Cod_UPZ'].astype(str)
eventos_esp_df['COD_UPZ'] = eventos_esp_df['COD_UPZ'].astype(str)

# Crear las columnas llave en ambas bases de datos
all_dbs_combined['merge_key'] = all_dbs_combined['year_month_day'] + '_' + all_dbs_combined['Cod_UPZ']
eventos_esp_df['merge_key'] = eventos_esp_df['year_month_day'] + '_' + eventos_esp_df['COD_UPZ']

# Merge usando la columna llave
df_merged2 = pd.merge(all_dbs_combined, eventos_esp_df, how='left', on='merge_key')

# ----- Datos Clima
clima = '/content/drive/MyDrive/Proyecto de grado/Datos_sds/precipitacion_ajus2.csv'
clima_df = pd.read_csv(clima, delimiter=',', encoding='UTF-8')

# Convertir a formato datetime
clima_df['FechaObservacion'] = pd.to_datetime(clima_df['FechaObservacion'])
all_dbs_combined['hora_fecha_inicial'] = pd.to_datetime(all_dbs_combined['hora_fecha_inicial'], errors='coerce')

# Redondear las coordenadas a una sola posición decimal antes de concatenar
all_dbs_combined['Latitud_X'] = all_dbs_combined['Latitud_X'].round(1)
all_dbs_combined['Longitud_Y'] = all_dbs_combined['Longitud_Y'].round(1)
clima_df['Latitud'] = clima_df['Latitud'].round(1)
clima_df['Longitud'] = clima_df['Longitud'].round(1)

# Crear columnas de coordenadas como cadenas concatenadas usando operaciones vectorizadas
all_dbs_combined['coords'] = all_dbs_combined['Latitud_X'].astype(str) + ',' + all_dbs_combined['Longitud_Y'].astype(str)
clima_df['coords'] = clima_df['Latitud'].astype(str) + ',' + clima_df['Longitud'].astype(str)

# Crear las columnas llave en ambas bases de datos
all_dbs_combined['merge_key'] = all_dbs_combined['hora_fecha_inicial'].dt.strftime('%Y-%m-%d') + '_' + all_dbs_combined_v5['coords']
clima_df['merge_key'] = clima_df['FechaObservacion'].dt.strftime('%Y-%m-%d') + '_' + clima_df['coords']

# Merge usando la columna llave
final_df = pd.merge(all_dbs_combined, clima_df, how='left', on='merge_key')


# ========================================================= #
# Guardar DF Final
# ========================================================= #

# Filtrar y guardar bd de incidentes con despacho 
bd_inc_con_desp = all_dbs_combined[all_dbs_combined['Inc_con_Desp'] == 'SI']
bd_inc_con_desp.to_csv('/content/drive/MyDrive/Proyecto de grado/Datos_sds/bd_inc_con_desp.csv', index=False)

# Luego de esto, se incluye manualmente desde excel el código de UPL para el 
# entrenamiento de los modelos. 