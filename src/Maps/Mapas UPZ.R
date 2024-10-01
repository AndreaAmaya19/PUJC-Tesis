rm (list = ls()) # Limpiar el entorno 

# Librerias necesarias 

library(sf)
library(rnaturalearth)
library(ggplot2)
library(dplyr)
library(openxlsx)
library(readxl)
library(stringr)
library(readr)
library(kableExtra)
library(viridis)
library(lubridate)
library(tidyr)
library(patchwork)


# Archivo SHP de upz 
upz_data <- st_read("C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Datos\\salud\\SALUD\\data.shp") # Ruta de acceso a la informacion 

#Creacion de los poligonos por UPL
upl_polygons <- upz_data %>%
  group_by(`COD.UPL`) %>%
  summarise(geometry = st_union(geometry))


#Archivo final de incidentes 

datos_v3 <- read_csv("C:/Users/LENOVO/Documents/Proyecto aplicado/Datos/Datos_vf_UPL.csv", 
                     locale = locale(encoding = "Latin1"))


#Mapas


# Contar la cantidad de incidentes por UPZ
incidentes_por_upz <- datos_v3 %>%
  group_by(Cod_UPZ) %>%
  summarise(Cantidad_incidentes = n())


# Unir la cantidad de incidentes con los datos espaciales de UPZ
upz_con_incidentes <- upz_data %>%
  left_join(incidentes_por_upz, by = c("COD.UPZ" = "Cod_UPZ"))

# Crear el mapa

grafico <- ggplot(data = upz_con_incidentes) +
  geom_sf(aes(fill = Cantidad_incidentes), color = "white") +
  scale_fill_viridis_c(name = "Catidad de Incidentes", direction = -1) +
  theme_minimal() +
  theme(
    text = element_text(family = "Calibri", size = 12),
    plot.title = element_text(face = "bold"),
    plot.subtitle = element_text(size = 12)
  )

# Guardar el gráfico con dimensiones personalizadas
ggsave("C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Figuras\\mapa_incidentes.png", 
       plot = grafico, 
       width = 8, height = 6, units = "in", dpi = 300)

datos_con_desp = datos_v3

# Mapas de incidentes por años 

# Agrupar por UPZ y año, y contar el número de incidentes
datos_agg <- datos_con_desp %>%
  group_by(Nombre_UPZ, Anio) %>%
  summarise(Cantidad_incidentes = n())

upz_año <- upz_data %>%
  left_join(datos_agg, by = c("UPlNmbr" = "Nombre_UPZ"), relationship = "many-to-many")


# Crear el mapa (suponiendo que ya tienes un objeto sf para las UPZs)
ggplot(data = upz_año) +
  geom_sf(aes(fill = Cantidad_incidentes), color = "white") +
  scale_fill_viridis_c(name = "Cantidad de Incidentes", direction = -1) +
  theme_minimal() +
  labs(title = "Mapa de Cantidad de Incidentes por UPZ",
       subtitle = "Cantidad de incidentes en cada UPZ por año") +
  facet_wrap(~ Anio) # Crear un mapa para cada año


## dia de la semana

datos_con_desp <- datos_con_desp %>%
  mutate(hora_fecha_inicial = as.POSIXct(hora_fecha_inicial, format="%m/%d/%Y %H:%M", tz="UTC"),
         Día_semana = weekdays(hora_fecha_inicial)) 

datos_agg1 <- datos_con_desp %>%
  group_by(Nombre_UPZ, Anio, Día_semana) %>%
  summarise(Cantidad_incidentes = n(), .groups = 'drop')

upz_año_dia <- upz_data %>%
  left_join(datos_agg1, by = c("UPlNmbr" = "Nombre_UPZ"), relationship = "many-to-many")


ggplot(data = upz_año_dia) +
  geom_sf(aes(fill = Cantidad_incidentes), color = "white") +
  scale_fill_viridis_c(name = "Cantidad de Incidentes", direction = -1) +
  theme_minimal() +
  labs(title = "Mapa de Cantidad de Incidentes por UPZ",
       subtitle = "Cantidad de incidentes en cada UPZ por día de la semana y año") +
  facet_grid(~Día_semana) 



## Promedio de incidentes en cada UPZ por día de la semana

datos_con_desp <- datos_con_desp %>%
  mutate(fecha_inicial_1 = as.Date(hora_fecha_inicial, format = "%m/%d/%Y"))


datos_agg_granular <- datos_con_desp %>%
  group_by(Nombre_UPZ, Día_semana, fecha_inicial_1) %>%
  summarise(Cantidad_incidentes = n(), .groups = 'drop')

datos_promedio <- datos_agg_granular %>%
  group_by(Nombre_UPZ, Día_semana) %>%
  summarise(Promedio_incidentes = mean(Cantidad_incidentes), .groups = 'drop')


upz_promedio <- upz_data %>%
  left_join(datos_promedio, by = c("UPlNmbr" = "Nombre_UPZ"), relationship = "many-to-many")


ggplot(data = upz_promedio) +
  geom_sf(aes(fill = Promedio_incidentes), color = "white") +
  scale_fill_viridis_c(name = "Cantidad de Incidentes", direction = -1) +
  theme_minimal() +
  labs(title = "Mapa del Promedio de Incidentes por UPZ",
       subtitle = "Promedio de incidentes en cada UPZ por día de la semana") +
  facet_wrap(~ Día_semana)

## Mapa de población 

## Datos de población##

archivo_excel1 <- "C:/Users/LENOVO/Downloads/anexo-proyecciones-poblacion-bogota-desagreacion-loc-2018-2035-UPZ-2018-2024.xlsx"
hoja_datos1 <- "Hoja3"

# Lee la hoja específica del archivo Excel
pob <- read_excel(archivo_excel1, sheet = hoja_datos1)

colnames(pob)

# Seleccionamos las columnas necesarias
df_new <- pob[, c("AÑO", "UPZ", "AREA GEOGRÁFICA","LOC" ,
                  "Total_0-4", "Total_5-9", "Total_10-14", 
                  "Total_15-19", "Total_20-24", "Total_25-29", 
                  "Total_30-34", "Total_35-39", "Total_40-44", 
                  "Total_45-49", "Total_50-54", "Total_55-59", 
                  "Total_60-64", "Total_65-69", "Total_70-74", 
                  "Total_75-79", "Total_80-84", "Total_85-89", 
                  "Total_90-94", "Total_95-99", "Total_100+")]

# Sumar las columnas en las 5 categorías deseadas
df_new$Total_0_4 <- df_new[["Total_0-4"]]
df_new$Total_5_14 <- df_new[["Total_5-9"]] + df_new[["Total_10-14"]]
df_new$Total_15_19 <- df_new[["Total_15-19"]]
df_new$Total_20_59 <- df_new[["Total_20-24"]] + df_new[["Total_25-29"]] + df_new[["Total_30-34"]] + 
  df_new[["Total_35-39"]] + df_new[["Total_40-44"]] + df_new[["Total_45-49"]] + 
  df_new[["Total_50-54"]] + df_new[["Total_55-59"]]
df_new$Mayores_60 <- df_new[["Total_60-64"]] + df_new[["Total_65-69"]] + df_new[["Total_70-74"]] + 
  df_new[["Total_75-79"]] + df_new[["Total_80-84"]] + df_new[["Total_85-89"]] + 
  df_new[["Total_90-94"]] + df_new[["Total_95-99"]] + df_new[["Total_100+"]]

# Crear el nuevo DataFrame con las columnas seleccionadas
df_final <- df_new[, c("AÑO", "UPZ","AREA GEOGRÁFICA","LOC", "Total_0_4", "Total_5_14", "Total_15_19", 
                       "Total_20_59", "Mayores_60")]

df_filtered <- subset(df_final, AÑO %in% c(2022, 2023, 2024)) # Años de analisis
df_filtered <- df_filtered %>% rename(UPlNmbr = `AREA GEOGRÁFICA`)

df_mapa <- left_join(upz_data, df_filtered, by = "UPlNmbr", relationship = "many-to-many")


## mapa para cada año 
# Filtrar los datos para el año deseado 
df_2022 <- df_mapa %>% filter(AÑO == 2024)


# Crear los mapas individualmente con la paleta viridis "A"
mapa_0_4 <- ggplot(df_2022) +
  geom_sf(aes(fill = Total_0_4)) +
  labs(title = "0 a 4 años", fill = "Población") +
  scale_fill_viridis_c(option = "A", direction = -1) +  # Colores más oscuros para mayores poblaciones
  theme_minimal()

mapa_5_14 <- ggplot(df_2022) +
  geom_sf(aes(fill = Total_5_14)) +
  labs(title = "5 a 14 años", fill = "Población") +
  scale_fill_viridis_c(option = "A", direction = -1) +  # Colores más oscuros para mayores poblaciones
  theme_minimal()

mapa_15_19 <- ggplot(df_2022) +
  geom_sf(aes(fill = Total_15_19)) +
  labs(title = "15 a 19 años", fill = "Población") +
  scale_fill_viridis_c(option = "A", direction = -1) +  # Colores más oscuros para mayores poblaciones
  theme_minimal()

mapa_20_59 <- ggplot(df_2022) +
  geom_sf(aes(fill = Total_20_59)) +
  labs(title = "20 a 59 años", fill = "Población") +
  scale_fill_viridis_c(option = "A", direction = -1) +  # Colores más oscuros para mayores poblaciones
  theme_minimal()

mapa_mayores_60 <- ggplot(df_2022) +
  geom_sf(aes(fill = Mayores_60)) +
  labs(title = "Mayores de 60 años", fill = "Población") +
  scale_fill_viridis_c(option = "A", direction = -1) +  # Colores más oscuros para mayores poblaciones
  theme_minimal()

# Combinar los mapas en una sola visualización
Mapa = (mapa_0_4 | mapa_5_14) / (mapa_15_19 | mapa_20_59 | mapa_mayores_60)

ggsave("C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Figuras\\mapa_poblacion.png", 
       plot = Mapa, 
       width = 8, height = 6, units = "in", dpi = 300)


############# Mapas de UPL ########################


#Mapas

# Contar la cantidad de incidentes por UPl
incidentes_por_upl <- datos_v3 %>%
  group_by(Cod_UPL) %>%
  summarise(Cantidad_incidentes = n())


# Unir la cantidad de incidentes con los datos espaciales de UPZ
upl_con_incidentes <- upl_polygons %>%
  left_join(incidentes_por_upl, by = c("COD.UPL" = "Cod_UPL"))

grafico1 = ggplot(data = upl_con_incidentes) +
  geom_sf(aes(fill = Cantidad_incidentes), color = "white") +  # Borde blanco
  scale_fill_viridis_c(name = "Cantidad de Incidentes") +
  theme_minimal()+
  theme(
    text = element_text(family = "Calibri", size = 12),
    plot.title = element_text(face = "bold"),
    plot.subtitle = element_text(size = 12)
  )

# Guardar el gráfico con dimensiones personalizadas
ggsave("C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Figuras\\mapa_incidentes_upl.png", 
       plot = grafico1, 
       width = 8, height = 6, units = "in", dpi = 300)

### Cambiar las rutas que sea necesario y garantizar los archivos. 
