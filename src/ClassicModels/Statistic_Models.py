# Librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm
import scipy.stats as stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

# Carga de Datos
Datos = pd.read_csv(f"/content/drive/MyDrive/Proyecto de grado/Datos_sds/Datos_modelo_upl.csv", delimiter=',', encoding='UTF-8')

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

# Dividir en entrenamiento y prueba (80% entrenamiento, 20% prueba)
train_size = int(len(serie_temporal) * 0.8)
train, test = serie_temporal[:train_size], serie_temporal[train_size:]

# Entrenar el modelo ARIMA
model = ARIMA(train, order=(2, 0, 2))
model_fit = model.fit()

# Realizar predicciones
predictions = model_fit.forecast(steps=len(test))

# Graficar las predicciones vs el valor real
plt.figure(figsize=(14, 7))
plt.plot(train.index, train, label='Entrenamiento')
plt.plot(test.index, test, label='Test Real')
plt.plot(test.index, predictions, label='Predicciones', color='red')
plt.title('Predicción de Servicios de Emergencias')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de Servicios')
plt.legend()
plt.show()

# Evaluación
# AIC y BIC
print(f"AIC: {model_fit.aic}")
print(f"BIC: {model_fit.bic}")

# RMSE y MAE en los datos de prueba
rmse = np.sqrt(mean_squared_error(test, predictions))
mae = mean_absolute_error(test, predictions)
print(f"RMSE: {rmse}")
print(f"MAE: {mae}")

# ------- Modelo SARIMA
# Ajustar el modelo SARIMA con los mejores parámetros encontrados
#Mejores parámetros: (0, 0, 2) estacional: (2, 0, 1, 12), AIC: 12.0

best_params=(0, 0, 2)
best_seasonal_params=(2, 0, 1, 12)

model_sarima = SARIMAX(train, order=best_params, seasonal_order=best_seasonal_params)
model_sarima_fit = model_sarima.fit(disp=False)

# Resumen del modelo
print(model_sarima_fit.summary())

# ------- BINOMIAL NEGATIVA
# Definir la variable dependiente
y = Datos['Total_Incidentes']

# Seleccionar variables independientes
X = Datos[['Cod_UPL', 'Dia_semana','Total_Incidentes', 'Rango_Hora_9am-9pm','Dia_del_anio', 'Moda_PI_CRITICA', 'Adultos_mayores_60',
           'Festivo', 'Cantidad_Eventos','Infantes_0_4','Incidentes_dia_anterior' ]]

# Agregar una constante para el intercepto
X = sm.add_constant(X)

# Evaluación
mean_y = y.mean()
var_y = y.var()
print('Media:', mean_y)
print('Varianza:', var_y)

# Histograma de Incidentes
plt.figure(figsize=(10, 6))
plt.hist(y, bins=30, color='skyblue', edgecolor='black')
plt.title('Histograma de Total de Incidentes')
plt.xlabel('Total de Incidentes')
plt.ylabel('Frecuencia')
plt.show()

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Añadir una constante a los datos de entrenamiento y prueba
X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)

# Ajustar el modelo de Regresión Binomial Negativa
neg_binom_model = sm.GLM(y_train, X_train, family=sm.families.NegativeBinomial()).fit()

# Resumen del modelo
print(neg_binom_model.summary())

# Obtener residuos
residuos = neg_binom_model.resid_pearson

# Graficar residuos
plt.figure(figsize=(10, 6))
plt.hist(residuos, bins=30, edgecolor='k')
plt.title('Histograma de Residuos')
plt.xlabel('Residuos')
plt.ylabel('Frecuencia')
plt.show()

# Q-Q plot (Se prueba normalidad de los residuos)
stats.probplot(residuos, dist="norm", plot=plt)
plt.title('Q-Q Plot de Residuos')
plt.show()

# Evaluar el modelo
y_pred = neg_binom_model.predict(X_test)
mae = np.mean(np.abs(y - y_pred))
print(f'MAE: {mae}')
rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
print(f'RMSE: {rmse}')
#AIC
aic = neg_binom_model.aic

# BIC
bic = neg_binom_model.bic

print(f"AIC del modelo: {aic}")
print(f"BIC del modelo: {bic}")