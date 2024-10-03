# Librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

# ========================================================= #
# Análisis Exploratorio de Datos
# ========================================================= #

Datos = pd.read_csv(f"/content/drive/MyDrive/Proyecto de grado/Datos_sds/bd_inc_con_desp.csv", delimiter=';', encoding='latin-1')

# --------- Eventos por día de la semana
# Formato datetime
Datos['hora_fecha_inicial'] = pd.to_datetime(Datos['hora_fecha_inicial'])

# Nombre del día en español
dias_semana_esp = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

Datos['dia_semana'] = Datos['hora_fecha_inicial'].dt.day_name().map(dias_semana_esp)

# Contar eventos por día de la semana
conteo_dias = Datos['dia_semana'].value_counts().reset_index()
conteo_dias.columns = ['dia_semana', 'cantidad_eventos']

# Ordenar los días de la semana
dias_semana_order_esp = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
conteo_dias['dia_semana'] = pd.Categorical(conteo_dias['dia_semana'], categories=dias_semana_order_esp, ordered=True)
conteo_dias = conteo_dias.sort_values('dia_semana')

# Gráfico de barras
sns.set(style="darkgrid")
plt.figure(figsize=(12, 5))
bar_plot = sns.barplot(x='dia_semana', y='cantidad_eventos', hue='dia_semana', legend=False, data=conteo_dias, palette='GnBu')

bar_plot.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

# Añadir los valores encima de las barras
for p in bar_plot.patches:
    height = p.get_height()
    bar_plot.text(p.get_x() + p.get_width() / 2., height, f'{int(height):,}',
                  ha='center', va='bottom', fontweight='bold', color='gray', size=11)

# Configurar el título y las etiquetas
plt.title('Cantidad de Eventos por Día de la Semana')
plt.xlabel('Día de la Semana')
plt.ylabel('Cantidad de Eventos')
plt.xticks(rotation=0)
plt.show()

# --------- Promedio de Eventos por dia
# Contar eventos por día de la semana y luego calcular el promedio por cada día (Para los 2.5 años del analisis)
promedio_dias = Datos.groupby('dia_semana')['cod_incidente'].count().reset_index()
promedio_dias['promedio_eventos'] = promedio_dias['cod_incidente'] / Datos['dia_semana'].nunique()

# Ordenar los días de la semana
dias_semana_order_esp = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
promedio_dias['dia_semana'] = pd.Categorical(promedio_dias['dia_semana'], categories=dias_semana_order_esp, ordered=True)
promedio_dias = promedio_dias.sort_values('dia_semana')

# Gráfico de barras
sns.set(style="darkgrid")
plt.figure(figsize=(12, 5))
bar_plot = sns.barplot(x='dia_semana', y='promedio_eventos', hue='dia_semana', legend=False, data=promedio_dias, palette='GnBu')

# Formato del eje y para mostrar números enteros
bar_plot.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

# Añadir los valores encima de las barras
for p in bar_plot.patches:
    height = p.get_height()
    bar_plot.text(p.get_x() + p.get_width() / 2., height, f'{height:.0f}',
                  ha='center', va='bottom', fontweight='bold', color='gray', size=11)

# Configurar el título y las etiquetas
plt.title('Promedio de Incidentes por Día de la Semana')
plt.xlabel('Día de la Semana')
plt.ylabel('Promedio de Incidentes')
plt.xticks(rotation=0)
plt.show()

# --------- Eventos por día del mes
# Extraer el día del mes
Datos['dia_mes'] = Datos['hora_fecha_inicial'].dt.day

# Contar eventos por día del mes
conteo_dias_mes = Datos['dia_mes'].value_counts().reset_index()
conteo_dias_mes.columns = ['dia_mes', 'cantidad_eventos']

# Ordenar los días del mes
conteo_dias_mes = conteo_dias_mes.sort_values('dia_mes')

# Gráfico de barras
plt.figure(figsize=(12, 6))
gradient_palette = sns.color_palette("crest", as_cmap=True)
bar_plot = sns.barplot(x='dia_mes', y='cantidad_eventos', hue='dia_mes', legend=False, data=conteo_dias_mes, palette=gradient_palette)

bar_plot.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

# Configurar el título y las etiquetas
plt.title('Cantidad de Eventos por Día del Mes')
plt.xlabel('Día del Mes')
plt.ylabel('Cantidad de Eventos')
plt.xticks(rotation=0)
plt.show()

# --------- Promedio por día del mes
# Contar la cantidad de veces que cada día del mes aparece en los datos
dias_conteo = Datos['dia_mes'].value_counts().sort_index()

# Contar eventos por día del mes
conteo_dias_mes = Datos['dia_mes'].value_counts().reset_index()
conteo_dias_mes.columns = ['dia_mes', 'cantidad_eventos']

# Calcular el promedio de eventos por día del mes
conteo_dias_mes['promedio_eventos'] = conteo_dias_mes.apply(lambda row: row['cantidad_eventos']/30 , axis=1)

# Ordenar los días del mes
conteo_dias_mes = conteo_dias_mes.sort_values('dia_mes')

# Crear una paleta de colores categórica basada en la paleta continua "crest"
gradient_palette = sns.color_palette("crest", n_colors=len(conteo_dias_mes))

# Gráfico de barras
plt.figure(figsize=(12, 6))
bar_plot = sns.barplot(x='dia_mes', y='promedio_eventos', data=conteo_dias_mes, palette=gradient_palette)

# Formato del eje Y para mostrar números enteros con coma
bar_plot.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.2f}'))

# Configurar el título y las etiquetas
plt.title('Promedio de Eventos por Día del Mes')
plt.xlabel('Día del Mes')
plt.ylabel('Promedio de Eventos')
plt.xticks(rotation=0)
plt.show()

# --------- Eventos por año y mes
# Extraer año y mes
Datos['year'] = Datos['hora_fecha_inicial'].dt.year
Datos['month'] = Datos['hora_fecha_inicial'].dt.month

# incidentes por año y month
conteo_incidentes = Datos.groupby(['year', 'month']).size().reset_index(name='cantidad_incidentes')

# Crear una columna de fecha para el gráfico
conteo_incidentes['fecha'] = pd.to_datetime(conteo_incidentes[['year', 'month']].assign(day=1))

# Crear el gráfico
plt.figure(figsize=(12, 4))
ax = sns.lineplot(x='fecha', y='cantidad_incidentes', data=conteo_incidentes, marker='o', color='lightseagreen')

ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Ajustar formato del gráfico
plt.title('')
plt.xlabel('Fecha')
plt.ylabel('Cantidad de Incidentes')
plt.xticks(rotation=90)
plt.grid(True)

plt.show()

# --------- Promedio por año y mes
# Extraer año y mes
Datos['year'] = Datos['hora_fecha_inicial'].dt.year
Datos['month'] = Datos['hora_fecha_inicial'].dt.month

# incidentes por año y month
conteo_incidentes = Datos.groupby(['year', 'month']).size().reset_index(name='cantidad_incidentes')
# Crear una columna de fecha para el gráfico
conteo_incidentes['fecha'] = pd.to_datetime(conteo_incidentes[['year', 'month']].assign(day=1))

# Sumar la cantidad de incidentes por año
suma_incidentes_por_anyo = conteo_incidentes.groupby('year')['cantidad_incidentes'].transform('sum')

# Agregar la suma anual como una nueva columna en el DataFrame original
conteo_incidentes['suma_anual'] = suma_incidentes_por_anyo

# Promedio mensual por año
conteo_incidentes ["Promedio_incidentes"] = conteo_incidentes["cantidad_incidentes"]/30

# Crear una columna de fecha para el gráfico
# Crear el gráfico
plt.figure(figsize=(13, 4.3))
ax = sns.lineplot(x='fecha', y='Promedio_incidentes', data=conteo_incidentes, marker='o', color='lightseagreen')

ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Ajustar formato del gráfico
plt.xlabel('Fecha')
plt.ylabel('Promedio de Incidentes')
plt.xticks(rotation=90, fontsize=13)
plt.yticks(fontsize=13)
plt.grid(True)

plt.show()

# --------- Porcentaje de evento por localidad
# Calcular la cantidad de incidentes por localidad
incidentes_por_localidad = Datos.groupby('Localidad_V2').agg({'cod_incidente': 'count'}).reset_index()

# Calcular el porcentaje de incidentes por localidad
total_incidentes = incidentes_por_localidad['cod_incidente'].sum()
incidentes_por_localidad['porcentaje_incidentes'] = (incidentes_por_localidad['cod_incidente'] / total_incidentes) * 100

# Ordenar por porcentaje de incidentes
incidentes_por_localidad = incidentes_por_localidad.sort_values(by='porcentaje_incidentes', ascending=False)

# Configurar el estilo de la gráfica
sns.set(style="darkgrid")
plt.figure(figsize=(8, 5))
gradient_palette = sns.color_palette("crest", as_cmap=True)

# Crear el gráfico de barras
bar_plot = sns.barplot(
    x='porcentaje_incidentes',
    y='Localidad_V2',
    data=incidentes_por_localidad,
    palette='viridis'
)

# Formatear el eje X para mostrar porcentajes
bar_plot.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}%'))


# Títulos y etiquetas
plt.xlabel('Porcentaje de Incidentes')
plt.ylabel('Localidad')
plt.xticks(rotation=0, fontsize=13)
plt.yticks(fontsize=13)
plt.tight_layout()
plt.show()

# --------- Frecuencia de prioridades inicial y final
prioridad_inicial = Datos['prioridad.inicial'].value_counts().sort_index()
prioridad_final = Datos['prioridad.final'].value_counts().sort_index()

# Crear un DataFrame con ambas series
prioridades_df = pd.DataFrame({'Prioridad Inicial': prioridad_inicial, 'Prioridad Final': prioridad_final})

# Graficar las prioridades
sns.set(style="darkgrid")
ax = prioridades_df.plot(kind='bar', figsize=(10, 4.5), color=['lightseagreen', 'seagreen'], width=0.8)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
# Configurar título y etiquetas

plt.xlabel('Prioridad')
plt.ylabel('Frecuencia')
plt.xticks(rotation=0, fontsize=13)
plt.yticks(fontsize=13)
plt.legend(title='Tipo de Prioridad', fontsize=13)

# Agregar labels sobre las barras
for container in ax.containers:
    ax.bar_label(container, label_type='edge', padding=1, color='gray', fontsize = 11 )

plt.show()

# --------- Frecuencia por tipo de incidentes 
tipo_incidente_counts = Datos['Incidente'].value_counts().sort_values(ascending=True)

plt.figure(figsize=(8, 5.5))

ax = tipo_incidente_counts.plot(kind='barh', color='lightseagreen')
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

plt.xlabel('Frecuencia')
plt.ylabel('')
plt.xticks(rotation=0, fontsize=13)
plt.yticks(fontsize=14)
plt.show()

# --------- Eventos por hora del día
# Crear el histograma sin etiquetas en las barras
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(Datos['hora_del_dia'], bins=24, color='lightseagreen', edgecolor='black')

ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

# Configurar título y etiquetas
plt.title('Distribución de Servicios de Emergencias por Hora')
plt.xlabel('Hora del Día')
plt.ylabel('Cantidad de Servicios')
plt.xticks(range(0, 24))
plt.grid(True)

plt.show()

# --------- Eventos por hora y día de la semana
# Definir los días de la semana en orden
dias_semana_order_esp = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

# Seleccionar la paleta de colores
colors = sns.color_palette('crest', 7)

# Crear una figura con 7 subplots
fig, axes = plt.subplots(7, 1, figsize=(10, 15), sharex=True)

for i, dia in enumerate(dias_semana_order_esp):
    # Filtrar los datos para el día de la semana actual
    df_dia = Datos[Datos['dia_semana'] == dia]

    # Crear el histograma para el día específico
    axes[i].hist(df_dia['hora_del_dia'], bins=24, color=colors[i], edgecolor='black')
    axes[i].set_title(f'{dia}', fontsize=14)
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')
    axes[i].set_xticks(range(0, 24))
    axes[i].grid(True)

# Ajustar el layout para que los subplots no se superpongan
plt.tight_layout()
plt.show()