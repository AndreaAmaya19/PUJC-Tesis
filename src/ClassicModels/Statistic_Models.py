# Librerias
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller



Datos = pd.read_csv(f"/content/drive/MyDrive/Proyecto de grado/Datos_sds/bd_inc_con_desp_2.csv", delimiter=';', encoding='latin-1')

# ------- Modelo ARIMA

# Supuestos
### Serie
# Fecha en formato de fecha
Datos_ss= Datos[['Fecha', 'Total_Incidentes']]

# Establecer 'Fecha' como índice
Datos_ss.set_index('Fecha', inplace=True)

# Total_Incidentes como una serie temporal
serie_temporal = Datos_ss['Total_Incidentes']

result = adfuller(serie_temporal)
print('ADF Statistic:', result[0])
print('p-value:', result[1])

