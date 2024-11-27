# Modelo espacio temporal para la predicción de la demanda de emergencias médicas en Bogotá.

Este repositorio contiene el código fuente desarrollado para la tesis "Modelo espacio-temporal para la predicción de la demanda de emergencias médicas en Bogotá". Está organizado en módulos para facilitar la exploración, procesamiento, modelado y evaluación de datos. A continuación, se describe la estructura del repositorio y las instrucciones para ejecutar el código.

## **Estructura del Repositorio**
```plaintext
src/
├── ClassicModels/        # Implementación de modelos estadísticos tradicionales (ARIMA, SARIMA, etc.)
├── DataProcessing/       # Scripts para limpieza, transformación e integración de datos.
├── EDA/                  # Análisis exploratorio de datos.
├── ML/                   # Modelos de machine learning (XGBoost, Random Forest, Redes Neuronales, etc.)
├── Maps/                 # Archivos y scripts relacionados con análisis espacial y mapas. (Código en R)
├── Model_Implementation/ # Código para implementación del modelo final en producción.
```

## **Guía de Uso**

### **1. Requisitos Previos**

1. Asegúrate de tener instalado Python 3.8 o superior.
2. Comprueba que la estructura de la base de datos en cada parte del procesamiento. 
3. Instala las dependencias necesarias ejecutando:


```bash
pip install -r requirements.txt
```

### **2. Flujo General**

El flujo general del código sigue estos pasos:

1. **Procesamiento de Datos:**
   - Valida que los datos tengan la estructura descrita en `data_structure/Estructura de base de datos procesamiento.txt`
   - Navega a `src/DataProcessing/` y ejecuta el script para limpieza e integración de datos:
     - `Processing.py`

   ```bash
   python src/DataProcessing/Processing.py
   ```
   

2. **Análisis Exploratorio de Datos (EDA):**
   - Usa el script en `src/EDA/` para analizar y visualizar los datos procesados.
   - Archivo principal:
     - `Eda.py`\

   ```bash
   python src/EDA/eda_summary.py
   ```
   
## Modelos Tradicionales

## Modelos de Machine Learning
