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
#_______________________

#UPZ archivo de la secretaria 
upz_data <- st_read("C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Datos\\salud\\SALUD\\saludupz.shp") # Ruta de acceso a la informacion 


#Upl (archivo de UPL y localidad corregido)
archivo_excel <- "C:/Users/LENOVO/Documents/Proyecto aplicado/Datos/BARRIOS POR UPZ.xlsx"
hoja_datos <- "Hoja2"
UPL <- read_excel(archivo_excel, sheet = hoja_datos)

# Union de las bases para incorporar UPL y Localidad ajustada.
upz_data1= merge(x = upz_data, y = UPL, by = c("UPlNombre"))


#Creacion de los poligonos por UPL
upl_polygons <- upz_data1 %>%
  group_by(`UPL_Nombre`) %>%
  summarise(geometry = st_union(geometry))


# Km por UPZ

data_upl_km = read_excel("C:/Users/LENOVO/Documents/Proyecto aplicado/Datos/Datos_upl_km.xlsx")
# Cambiar el nombre de la columna
data_upl_km  = data_upl_km %>%
rename(UPlNombre = UPZ)


#Extraemos el area Km que es nuestra variable de interes 
Km_upz1 <- data_upl_km[, c("UPlNombre", "Área.urbana", "Área.urbana UPL" )]


# Union de las bases para incorporar UPL y Localidad ajustada.
upz_data1= merge(x = upz_data1, y = Km_upz1, by = c("UPlNombre"))


# Graficos



colores <- c(
  "#CDC0B0", "#8B8378", "#76EEC6", "#66CDAA", "#458B74", "#EED5B7", 
  "#A52A2A", "#EE3B3B", "#EEC591", "#CDAA7D", "#8B7355", "#5F9EA0", 
  "#8EE5EE", "#7AC5CD", "#458B00", "#D2691E", "#8B4513", "#FF7F50", 
  "#CD5B45", "#8B3E2F", "#00CDCD", "#EEAD0E", "#556B2F", "#BCEE68", 
  "#9932CC", "#BF3EFF", "#68228B", "#C1FFC1", "#FF1493", "#8B0A50", 
  "#00B2EE", "#CD8162"  ) #Paleta de colores 

## Mapa de las UPZ por Localidades. 

ggplot(data = upz_data1) +
  scale_fill_manual(values = colores) +  # Usa la paleta de 20 colores definida
  theme_minimal() +
   geom_sf(aes(fill = LOCALIDAD), color = "white", size = 0.3) +
 labs(title = "Mapa de Bogotá por UPZ y Localidades") +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.title.x = element_blank(),
    axis.title.y = element_blank()
  )

## Mapa de las UPZ por UPL.
ggplot(data = upz_data1) +
  scale_fill_manual(values = colores) +  # Usa la paleta de 20 colores definida
  theme_minimal() +
   geom_sf(aes(fill = UPL_Nombre), color = "white", size = 0.3) +
 labs(title = "Mapa de Bogotá por UPZ y UPL") +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.title.x = element_blank(),
    axis.title.y = element_blank()
  )



## Incorporar UPZ y UPL por Lat y Long 

# Cargar la base que contiene los registros con Lat y Long

archivo_path <- "C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Plantilla_72_V2.txt" #Ruta del archivo
datos_v2 <- read.table(archivo_path, header = TRUE, sep = "|", stringsAsFactors = FALSE)

#Crear nuevas variables para Lat y Long para no modificar las originales 
datos_v2$Longitud_Y = datos_v2$Longitud..Y.
datos_v2$Longitud_X = datos_v2$Latitud..X.

#Crear un consecutivo a los datos en caso de que se duplique la informacion poder identificarlo
datos_v2 <- datos_v2 %>%
mutate(ID_consecutivo = row_number())

# Convertir la base a un objeto sf para acerlo compatible con el archizo shp de UPZ y UPL

datos_v2$geometry = st_as_sfc(st_as_sf(datos_v2, coords = c("Longitud..Y.", "Latitud..X."), crs = st_crs(upz_data), remove = FALSE))
datos_v2_sf <- st_as_sf(datos_v2, coords = c("Longitud..Y.", "Latitud..X."), crs = 4326)
datos_v2_sf <- st_transform(datos_v2_sf, crs = st_crs(upz_data1))


# Realizar la intersección de las variable UPZ

#seleccion de varibles a incorporar en la base principal
upz_data_selected <- upz_data1 %>%
  dplyr::select("UPlNombre", "COD UPZ","NUM LOCALIDAD" , "LOCALIDAD", "COD UPL", "UPL_Nombre","Área.urbana", "Área.urbana UPL" ,"geometry")

# Incorporacion espacial lat y lon
datos_v2_upz1 <- st_join(datos_v2_sf, upz_data_selected, join = st_within)

#Convertir la base nuevamente a DF
datos_v2_upz1 <- st_drop_geometry(datos_v2_upz1)


#Seleccionar el Id_consecutivo unico dado que la informacion se duplica
#Datos_unicos <- datos_v2_upz1 %>%
#  distinct(ID_consecutivo, .keep_all = TRUE)

#Eliminar la columna de ID_consecutivo
#Datos_unicos = Datos_unicos %>% select(-ID_consecutivo)


## Con el ID_consecutivo eliminar los duplicados en Python.

## Exportar base 
write.table(datos_v2_upz1, "C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Datos\\Plantilla_72_V3.txt", sep = "|", row.names = FALSE, quote = FALSE) # formato TXT
write.csv(datos_v2_upz1 = "C:/Users/LENOVO/Documents/Proyecto aplicado/Datos/Plantilla_72_V3.csv", row.names = FALSE) # formato CSV


# Exportar Shp. para los mapas 
st_write(upz_data_selected, "C:\\Users\\LENOVO\\Documents\\Proyecto aplicado\\Datos\\salud\\SALUD\\data.shp")


##### Ajustar las rutas 



