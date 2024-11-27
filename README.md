# Modelo espacio temporal para la predicción de la demanda de emergencias médicas en Bogotá.

Este repositorio contiene el código fuente desarrollado para la tesis "Modelo espacio-temporal para la predicción de la demanda de emergencias médicas en Bogotá". Está organizado en módulos para facilitar la exploración, procesamiento, modelado y evaluación de datos. A continuación, se describe la estructura del repositorio y las instrucciones para ejecutar el código.

## **Estructura del Repositorio**
```plaintext
data_structure/
├── estructura de base de datos procesamiento.txt/          # Descripción de las bases de datos para procesamiento inicial.
├── estructura de datos para implementación del modelo.txt/ # Detalles de la estructura de datos necesaria para implementar el modelo.
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
     - `processing.py`

   ```bash
   python src/DataProcessing/processing.py
   ``` 

2. **Análisis Exploratorio de Datos (EDA):**
   - Usa el script en `src/EDA/` para analizar y visualizar los datos procesados.
   - Archivo principal:
     - `eda.py` 

   ```bash
   python src/EDA/eda.py
   ```

3. **Modelado Estadístico:**
   - Implementa y evalúa los modelos tradicionales en `src/ClassicModels/`.
   - Archivo:
     - `statistic_models.py`

   ```bash
   python src/ClassicModels/statistic_models.py
   ```

4. **Modelos de Machine Learning:**
   - Entrena y evalúa modelos avanzados en `src/ML/`.
   - Archivo:
     - `ml_final_model.py`

   ```bash
   python src/ML/ml_final_model.py
   ```

5. **Análisis Espacial y Mapas:**
   - Visualiza los patrones espacio-temporales en `src/Maps/` utilizando R.
   - Archivos principales:
     - `Analisis espacial.R`
     - `Mapas UPZ.R`
     - `variable UPZ.R`

6. **Implementación del Modelo Final:**
   - Valida la estructura de la base de datos antes de ejecutar el modelo, esta se encuentra en `data_structure/estructura de datos para implementación del modelo.txt`
   - Usa el script en `src/Model_Implementation/` para implementar el modelo final y realizar predicciones. El modelo ya esta entrenado, solo sigue los pasos que están en el notebook para llamarlo y ejecutarlo.
   - Archivos principales:
     - Modelo: `src/Model_Implementation/modelo_xgb.pkl`
     - Notebook: `src/Model_Implementation/Implementación_Modelo_CRUE.ipynb`

   ```bash
   python src/Model_Implementation/Implementación_Modelo_CRUE.ipynb
   ```

---

## **Notas Adicionales**

- Asegúrate de que los datos estén en el formato adecuado antes de ejecutar los scripts.
- El archivo `requirements.txt` incluye todas las dependencias necesarias para ejecutar el código, pero puede ser necesario actualizar la versión de las librerías.
- Si necesitas ayuda adicional, revisa los comentarios dentro de cada script para más detalles.
