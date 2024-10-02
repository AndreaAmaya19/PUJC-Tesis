# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization, LSTM, Concatenate, Reshape, Flatten
from tensorflow.keras import regularizers

# Carga de datos
Datos = pd.read_csv(f"/content/drive/MyDrive/Proyecto de grado/Datos_sds/Datos_rnn.csv", delimiter=',', encoding='UTF-8')

# Agrupar Datos por Fecha, Cod_UPL y Rango_Hora:
df_agrupado = Datos.groupby(['Fecha', 'Cod_UPL', 'Rango_Hora']).agg(
    Total_Incidentes=('cod_incidente', lambda x: x.nunique()),
    Anio = ('Anio', 'max'),
    Mes = ('Mes', 'max'),
    Dia_mes = ('Dia_mes', 'max'),
    Dia_del_anio = ('dia_del_anio', 'max'),
    Dia_semana = ('dia_semana', 'max'),
    Festivo = ('Festivo', 'max'),
    Cantidad_Eventos = ('Cantidad Eventos', 'max'),
    Aforo_Total_Eventos = ('Aforo_total', 'max'),
    Precipitacion_mm = ('ValorPrecip', 'max'),
    Infantes_0_4 = ('Infantes_0_4', 'max'),
    Niños_5_14 = ('Niños_5_14', 'max'),
    Adolecentes_15_19 = ('Adolecentes_15_19', 'max'),
    Adultos_20_59 = ('Adultos_20_59', 'max'),
    Adultos_mayores_60 = ('Adultos_mayores_60', 'max'),
    Total_Mujeres = ('Total_Mujeres', 'max'),
    Total_Hombres = ('Total_Hombres', 'max'),
    Total_Pob = ('Total_pob_UPL', 'max'),
    Densidad_poblacional = ('Densidad_poblacional', 'max'),

    Broma=('Broma', 'sum'),
    Falsa_alarma =('Falsa_alarma', 'sum'),
    Atendido=('Atendido', 'sum'),
    Inc_Herido=('Inc_Herido', 'sum'),
    Inc_TrstM=('Inc_TrstM', 'sum'),
    Inc_Enfermo=('Inc_Enfermo', 'sum'),
    Inc_Convulsion=('Inc_Convulsion', 'sum'),
    Inc_Dif_Resp=('Inc_Dif_Resp', 'sum'),
    Inc_Paro = ('Inc_Paro', 'sum'),

    PI_Critica = ('prioridad.inicial_CRITICA', 'sum'),
    PI_Alta = ('prioridad.inicial_ALTA', 'sum'),
    PI_Media = ('prioridad.inicial_MEDIA', 'sum'),
    PI_Baja = ('prioridad.inicial_BAJA', 'sum')

).reset_index()

# Crear columna de Incidentes del Día Anterior
df_agrupado['Fecha'] = pd.to_datetime(df_agrupado['Fecha'])
df = df_agrupado.sort_values(by=['Fecha', 'Cod_UPL', 'Rango_Hora'])
df['Inc_dia_anterior'] = df.groupby(['Cod_UPL', 'Rango_Hora'])['Total_Incidentes'].shift(1)
df = df.dropna(subset=['Inc_dia_anterior'])

# Rango de hora a formato binario
df['Rango_Hora'] = np.where(df['Rango_Hora'] == '9am-9pm', 1, 0)

# Análisis de correlación 
Datos_corr = df.drop(['Fecha', 'Anio', 'Total_Mujeres', 'Total_Hombres', 'Broma', 'Falsa_alarma', 'Atendido', 'Total_Pob', 'Inc_Enfermo'], axis=1)
corr_matrix = Datos_corr.corr()

plt.figure(figsize=(12, 7.5))
sns.heatmap(corr_matrix, annot=True, cmap='crest', linewidth=.5, fmt='.1f')
plt.xticks(fontsize=12, color='gray')
plt.yticks(fontsize=12, color='gray')
plt.title('')
plt.show()

# Selección de variables
X = df[['Cod_UPL', 'Dia_semana', 'Dia_del_anio', 'Rango_Hora', 'Densidad_poblacional', 'Adultos_mayores_60', 'Infantes_0_4', 'Festivo', 'Cantidad_Eventos',
         'Inc_Herido', 'Inc_dia_anterior', 'PI_Critica']]
y = df['Total_Incidentes']

# Separación de los datos, 80% entrenamiento - 20% prueba.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ========================================================= #
#                   Modelo XGBoost
# ========================================================= #
modelo_xgb = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.05, random_state=123)
modelo_xgb.fit(X_train, y_train)

# Predicciones
y_pred = modelo_xgb.predict(X_test)

# Metricas de evaluación
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'RMSE: {rmse}')
print(f'MAE: {mae}')
print(f'R²: {r2}')

# Base de datos de resultados
df_resultados = X_test.copy()
df_resultados['Total_Inc_Real'] = y_test
df_resultados['Total_Inc_Pred'] = y_pred

# Grafico de valores reales Vs predicciones
plt.figure(figsize=(15, 5))
g1 = sns.lineplot(df_resultados, x='Dia_del_anio', y='Total_Inc_Real', label='Datos Reales', color='dodgerblue', alpha=1)
g2 = sns.lineplot(df_resultados, x='Dia_del_anio', y='Total_Inc_Pred', label='Predicción', color='orange', alpha=1)

# Importancia de Variables
importance_xgb = modelo_xgb.get_booster().get_score(importance_type='gain')
importance_df_xgb = pd.DataFrame(importance_xgb.items(), columns=['Feature', 'Importance'])
importance_df_xgb = importance_df_xgb.sort_values(by='Importance', ascending=False).head(10)

plt.figure(figsize=(8, 4))
sns.barplot(x='Importance', y='Feature', data=importance_df_xgb, color='lightseagreen' )
plt.title("")
plt.xlabel("Importancia", fontsize=12, color='gray')
plt.ylabel("Variable", fontsize=12, color='gray')
plt.xticks(fontsize=12 )
plt.yticks(fontsize=12)
plt.show()

# ========================================================= #
#                   Modelo MLP
# ========================================================= #
# Hiperparámetros ajustados
dropout_rate = 0.5
l2_factor = 0.001
learning_rate = 0.01

# Construcción del modelo con Batch Normalization, Dropout, y L2
model_mlp = Sequential([
  Dense(64, activation='relu', kernel_regularizer=regularizers.l2(l2_factor), input_shape=(X_train.shape[1],)),
  BatchNormalization(),
  Dropout(dropout_rate),

  Dense(32, activation='relu', kernel_regularizer=regularizers.l2(l2_factor)),
  Dropout(dropout_rate),

  Dense(16, activation='relu', kernel_regularizer=regularizers.l2(l2_factor)),
  Dropout(dropout_rate),

  Dense(1, activation='linear')
])

# Compilación del modelo con optimizador Adam ajustado
model_mlp.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='mean_squared_error',
                  metrics=['mae'])

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model_mlp.fit(X_train, y_train,
                        epochs=50,
                        batch_size=32,
                        validation_split=0.1,
                        callbacks=[early_stopping],
                        verbose=1)

# Función para evaluar los resultados del modelo
def evaluate_model(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f'{model_name} - MAE: {mae:.4f}, MSE: {mse:.4f}, R2: {r2:.4f}')
    return mae, mse, r2

mlp_predictions = model_mlp.predict(X_test).flatten()
results = evaluate_model(y_test, mlp_predictions, 'MLP')

# ========================================================= #
#                   Modelo RNN
# ========================================================= #
df['Cod_UPL'] = df['Cod_UPL'].astype('int64')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
y_train = y_train.astype('float32')
y_test = y_test.astype('float32')

# Entradas del modelo
input_upl = Input(shape=(1,), name='upl_input')  # Cod_UPL
input_time = Input(shape=(3,), name='time_input')  # Mes, Dia_mes, Dia_semana, Dia_del_anio, Rango_Hora
input_context = Input(shape=(8,), name='context_input')

# Reshape para que sea compatible con la LSTM
reshaped_time = Reshape((3, 1))(input_time)

# Procesar las variables temporales con una LSTM
lstm_out = LSTM(128, return_sequences=False, kernel_regularizer=tf.keras.regularizers.l2(0.001))(reshaped_time)
lstm_out = Dropout(0.5)(lstm_out)

# Capa densa para Cod_UPL
upl_dense = Dense(16, activation='relu')(input_upl)

# Capa densa para las variables de contexto con regularización L2
context_dense = Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001))(input_context)
context_dense = Dropout(0.5)(context_dense)

combined = Concatenate()([upl_dense, lstm_out, context_dense])

# Capa final
output = Dense(1, activation='linear')(combined)

# Crear modelo
model = Model(inputs=[input_upl, input_time, input_context], outputs=output)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
              loss='mean_squared_error',
              metrics=['mae'])

model.summary()

X_train_time = np.array(X_train[['Dia_semana', 'Dia_del_anio', 'Rango_Hora']]).astype('float32')
X_train_upl = np.array(X_train['Cod_UPL']).astype('float32')
X_train_context = np.array(X_train[['Densidad_poblacional', 'Adultos_mayores_60', 'Infantes_0_4', 'Festivo', 'Cantidad_Eventos', 'Inc_Herido', 'Inc_dia_anterior', 'PI_Critica']]).astype('float32')

X_test_time = np.array(X_test[['Dia_semana', 'Dia_del_anio', 'Rango_Hora']]).astype('float32')
X_test_upl = np.array(X_test['Cod_UPL']).astype('float32')
X_test_context = np.array(X_test[['Densidad_poblacional', 'Adultos_mayores_60', 'Infantes_0_4', 'Festivo', 'Cantidad_Eventos', 'Inc_Herido', 'Inc_dia_anterior', 'PI_Critica']]).astype('float32')

# Entrenar el modelo
history = model.fit([X_train_upl, X_train_time, X_train_context], y_train,
                    epochs=50, batch_size=64, validation_split=0.2)

# Evaluar el modelo
test_loss, test_mae = model.evaluate([X_test_upl, X_test_time, X_test_context], y_test)
print(f'Test Loss: {test_loss}, Test MAE: {test_mae}')

# predicciones
y_pred = model.predict([X_test_upl, X_test_time, X_test_context])

rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'RMSE: {rmse}')
print(f'MAE: {mae}')
print(f'R²: {r2}')