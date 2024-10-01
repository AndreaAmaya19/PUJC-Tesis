import pandas as pd

# Ruta del archivo
ruta_archivo = r'C:\Users\LENOVO\Documents\Proyecto aplicado\Datos\Plantilla_72_V3.txt'

# Cargar el archivo en un DataFrame
df = pd.read_csv(ruta_archivo, delimiter='|', low_memory=False)  # Ajusta el delimitador si es necesario

# Eliminar duplicados basados en la columna 'ID_consecutivo'
df_sin_duplicados = df.drop_duplicates(subset='ID_consecutivo')

# Eliminar la columna 'ID_consecutivo'
df_sin_duplicados = df_sin_duplicados.drop(columns=['ID_consecutivo'])

# Guardar el DataFrame resultante en un nuevo archivo (opcional)
df_sin_duplicados.to_csv(r'C:\Users\LENOVO\Documents\Proyecto aplicado\Datos\Plantilla_72_V3_sin_duplicados.txt', index=False, sep='|')
