rm (list = ls())

# Carga de las librerías
library(gstat)
library(sp)
library(sf)
library(raster)
library(automap)
library(geoR)
library(readxl)
library (ggplot2)
library(dplyr)
library(viridis)
library(corrplot)
library(ggcorrplot)
library(spatstat)
library(spatstat.geom)
library(spatstat.utils)


#Archivo final de incidentes 

datos1 <- read_csv("C:/Users/LENOVO/Documents/Proyecto aplicado/Datos/Datos_vf_UPL.csv", 
                     locale = locale(encoding = "Latin1"))

# Convertir la columna de fechas en un objeto de fecha y hora

datos1$hora_fecha_inicial <- as.POSIXct(datos1$hora_fecha_inicial, format = "%m/%d/%Y %H:%M")

# Crear una columna con el día de la semana
datos1$dia_semana <- weekdays(datos1$hora_fecha_inicial)

# Crear una columna con la hora del día
datos1$hora <- format(datos1$hora_fecha_inicial, "%H")

# Analisis por periodo del dia

# Crear una columna categórica para el período del día
datos1$periodo_dia <- cut(as.numeric(datos1$hora), 
                          breaks = c(0, 6, 12, 18, 24), 
                          labels = c("Madrugada", "Mañana", "Tarde", "Noche"), 
                          include.lowest = TRUE, right = FALSE)

# Agrupar por UPZ, día de la semana y período del día
incidentes_agrupados <- datos1 %>%
  group_by(Nombre_UPZ, dia_semana, periodo_dia) %>%
  summarise(total_incidentes = n()) %>%
  ungroup()

       
# Gráfico de barras Total de Incidentes por Día de la Semana y Período del Día
G.Peridodia = ggplot(incidentes_agrupados, aes(x = dia_semana, y = total_incidentes, fill = periodo_dia)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_viridis_d(option = "D", name = "Período del Día") +
  theme_minimal() +
  labs(x = "Día de la Semana", 
       y = "Total de Incidentes") +
  theme(
    text = element_text(family = "Calibri", size = 12),
    plot.title = element_text(face = "bold"),
    plot.subtitle = element_text(size = 12)
  )

# Guardar el gráfico con dimensiones personalizadas
ggsave("C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Figuras\\G.Peridodia.png", 
       plot = G.Peridodia, 
       width = 6, height = 4, units = "in", dpi = 300)

## Analisis temporal 

# Extraer año y mes para análisis temporal
datos1$anio <- format(datos1$hora_fecha_inicial, "%Y")
datos1$mes <- format(datos1$hora_fecha_inicial, "%m")

incidentes_por_mes <- datos1 %>%
  group_by(anio, mes) %>%
  summarize(total_incidentes = n(), .groups = 'drop')

# Convertir mes a factor para orden correcto
incidentes_por_mes$mes <- factor(incidentes_por_mes$mes, levels = sprintf("%02d", 1:12), labels = month.abb)


# Tendencia de Incidentes por Mes (2022-2024
G.Tende.anio = ggplot(incidentes_por_mes, aes(x = mes, y = total_incidentes, color = anio, group = anio)) +
  geom_line(size = 1) +      # Añadir líneas de tendencia
  geom_point(size = 2) +    # Añadir puntos
  labs(x = "Mes",
       y = "Total de Incidentes",
       color = "Año") +
  theme_minimal() +
  scale_color_viridis_d() +  # Usar paleta de colores viridis para distinguir años
  scale_x_discrete(limits = month.abb)+
  theme(
    text = element_text(family = "Calibri", size = 12),
    plot.title = element_text(face = "bold"),
    plot.subtitle = element_text(size = 12)
  )

# Guardar el gráfico con dimensiones personalizadas
ggsave("C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Figuras\\G.Tende.anio.png", 
       plot = G.Tende.anio, 
       width = 6, height = 4, units = "in", dpi = 300)



## Modelo

## 1. Tranformacion de las variables 


# Asegúrate de que las coordenadas están en formato numérico
datos1$Latitud_X <- as.numeric(datos1$Latitud_X)
datos1$Longitud_Y <- as.numeric(datos1$Longitud_Y)

# Convertir la columna de fecha y hora en formato POSIXct
datos1$hora_fecha_inicial <- as.POSIXct(datos1$hora_fecha_inicial, format="%Y-%m-%d %H:%M:%S")

# Agregar una columna temporal en formato numérico para simplificar el análisis
datos1$time_num <- as.numeric(difftime(datos1$hora_fecha_inicial, min(datos1$hora_fecha_inicial), units = "days"))

# Filtrar registros donde latitud y longitud no sean 0
datos1 <- datos1[!(datos1$Latitud_X == 0 & datos1$Longitud_Y == 0), ]


# 2. Crear el Objeto Espacial limites de Bogotá
# Definir los límites espaciales de Bogotá 
bbox_bogota <- owin(xrange = c(-74.22, -74.01), yrange = c(4.4, 4.9))

# Crear un objeto espacial
pattern_spatial <- ppp(x = datos1$Longitud_Y, y = datos1$Latitud_X, window = bbox_bogota)

# Verificar el objeto
plot(pattern_spatial)

# Calcular la densidad de los incidentes
density_pattern <- density(pattern_spatial)

# Graficar la densidad
plot(density_pattern)


# Usar la función stpp de spatstat para crear un objeto espaciotemporal
# Aquí se crea un objeto de proceso puntual espaciotemporal
pattern_st <- stppp(x = datos1$Longitud_Y, 
                    y = datos1$Latitud_X, 
                    t = datos1$time_num, 
                    window = bbox_bogota, 
                    T = range(datos1$time_num))

# Verificar el objeto
plot(pattern_st)




# Crear un objeto de proceso puntual espaciotemporal usando ppp para los datos espaciales
# y luego realiza análisis sobre la variable temporal separadamente

pattern_st <- ppp(x = datos1$Longitud_Y, 
                  y = datos1$Latitud_X, 
                  window = bbox_bogota)

# calcular la intensidad temporal
time_range <- range(datos1$time_num)
time_hist <- hist(datos1$time_num, breaks=50, main="Distribución Temporal de Incidentes", xlab="Días desde el inicio")

K_function <- Kest(pattern_spatial)

# Graficar la función K
plot(K_function)


# Instalar y cargar el paquete spatstat.extra
if (!require(spatstat.extra)) install.packages("spatstat.extra")
library(spatstat.extra)

# Crear una representación espaciotemporal con datos simulados
pattern_st <- pps(x = datos1$Longitud_Y, 
                  y = datos1$Latitud_X, 
                  t = datos1$time_num, 
                  window = bbox_bogota, 
                  T = range(datos1$time_num))


######

