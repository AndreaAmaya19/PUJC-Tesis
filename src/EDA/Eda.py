# Librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter


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
