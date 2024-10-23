# **Clasificación de Noticias por Categoría usando Naive Bayes**

## **Autor**
- **Alejandro Ignacio Ortiz Ortega**
---
## **Índice**
1. [Planteamiento del Problema](#planteamiento-del-problema)
2. [Introducción y Objetivo](#introducción-y-objetivo)
3. [Proceso de Desarrollo](#proceso-de-desarrollo)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Instrucciones de Uso](#instrucciones-de-uso)
6. [Preprocesamiento y Uso de SMOTE](#preprocesamiento-y-uso-de-smote)
7. [Informe de Clasificación](#informe-de-clasificación)
8. [Pruebas por Categoría](#pruebas-por-categoría)
9. [Posibles Razones de Errores del Modelo](#posibles-razones-de-errores-del-modelo)
10. [Conclusión](#conclusión)

---

## **Planteamiento del Problema**
**Ejercicio 4:** Clasificación de Noticias

Tienes un conjunto de datos que contiene noticias clasificadas en diferentes categorías (política, deportes, tecnología, etc.).
Utiliza el Teorema de Bayes para construir un clasificador que pueda predecir la categoría de una noticia dada su
descripción. Divide el conjunto de datos en entrenamiento y prueba, y evalúa la precisión de tu clasificador.

---

## **Introducción y Objetivo**
Este proyecto tiene como objetivo crear un modelo de **Machine Learning** que clasifique noticias en cinco categorías: **tecnología, deportes, política, entretenimiento y salud**. Utilizamos **Naive Bayes** como modelo de clasificación junto con **TF-IDF** para transformar texto en vectores numéricos. Las noticias se obtienen a través de la API de **NewsAPI**.

---

## **Proceso de Desarrollo**

### 1. **Obtención de Datos**
- Utilizamos la API **NewsAPI** para extraer noticias en cinco categorías.
- Implementamos manejo de errores para manejar el **límite de solicitudes** (código 429).
- Validamos las noticias para evitar descripciones vacías o con valor `None`.

### 2. **Preprocesamiento de Texto**
- Eliminamos **palabras vacías** con la biblioteca **NLTK**.
- Aplicamos **TF-IDF** con las siguientes configuraciones:
  - `ngram_range = (1, 2)` para capturar secuencias de palabras.
  - `max_features = 5000` para limitar a las palabras más relevantes.

### 3. **División del Dataset**
- Dividimos los datos en **70% entrenamiento** y **30% prueba** usando `train_test_split`.
- Usamos **estratificación** para mantener proporciones iguales de categorías en ambos conjuntos.

### 4. **Entrenamiento del Modelo**
- Entrenamos el modelo con **Multinomial Naive Bayes**, adecuado para clasificación de texto.
- Ajustamos el parámetro **alpha = 1.0** para un rendimiento óptimo.

### 5. **Evaluación del Modelo**
- Usamos **precisión, recall y f1-score** para evaluar el modelo.
- La precisión final del modelo fue de **66%**.

---

## **Estructura del Proyecto**

- **Código**: Implementa la obtención de datos, preprocesamiento, entrenamiento del modelo y predicciones en tiempo real.
- **Interacción con el usuario**: Permite ingresar descripciones para predecir la categoría correspondiente.

---

## **Instrucciones de Uso**

### **1. Preparación**
Asegúrate de tener las siguientes dependencias instaladas:
```bash
pip install requests pandas scikit-learn nltk
```

### **2. Configuración**
- Obtén una **API Key** válida de [NewsAPI](https://newsapi.org) y reemplázala en la variable `API_KEY` dentro del código.

### **3. Ejecución del Proyecto**
- Ejecuta el script en tu terminal o IDE.
- Ingresa descripciones de noticias cuando el programa lo solicite, o escribe 'salir' para salir del programa.
---

## **Preprocesamiento y Uso de SMOTE**

### **1. Preprocesamiento con TF-IDF**
- El proyecto utiliza **TF-IDF** (Term Frequency-Inverse Document Frequency) para transformar las descripciones de las noticias en vectores numéricos. Esta técnica pondera las palabras más relevantes de cada documento, ignorando aquellas demasiado frecuentes en todo el corpus.

### **2. Sobremuestreo con SMOTE**
- **SMOTE** (Synthetic Minority Over-sampling Technique) se aplica para **equilibrar las clases** en el dataset. 
- En datasets desbalanceados, algunas categorías tienen menos ejemplos, lo que podría llevar al modelo a tener un **sesgo** hacia las categorías más frecuentes.
- **SMOTE** genera ejemplos sintéticos para las clases minoritarias, creando un dataset más **balanceado** y mejorando la capacidad del modelo para generalizar.

**Distribución del dataset tras aplicar SMOTE:**

| Categoría      | Cantidad |
|----------------|----------|
| Tecnología     | 300      |
| Deportes       | 300      |
| Política       | 300      |
| Entretenimiento| 300      |
| Salud          | 300      |

- Esta distribución refleja el balanceo del dataset después de aplicar SMOTE.
- Cada categoría tiene 300 ejemplos, garantizando que ninguna clase esté sobre o infra-representada, reduciendo el sesgo del modelo.
---
## **Informe de Clasificación**

**Precisión del modelo**: 0.66

| **Categoría**       | **Precisión** | **Recall** | **F1-Score** | **Soporte** |
|---------------------|---------------|------------|--------------|-------------|
| **Entretenimiento** | 0.59          | 0.70       | 0.64         | 90          |
| **Salud**           | 0.72          | 0.74       | 0.73         | 90          |
| **Política**        | 0.74          | 0.60       | 0.66         | 90          |
| **Deportes**        | 0.62          | 0.61       | 0.62         | 90          |
| **Tecnología**      | 0.62          | 0.62       | 0.62         | 90          |

| **Métricas Totales**| **Precisión** | **Recall** | **F1-Score** | **Soporte** |
|---------------------|---------------|------------|--------------|-------------|
| **Exactitud**       |               |            | 0.66         | 450         |
| **Macro Avg**       | 0.66          | 0.66       | 0.66         | 450         |
| **Weighted Avg**    | 0.66          | 0.66       | 0.66         | 450         |


## **Análisis del Informe**

### **1. Métricas por Categoría:**

- **Precision:** Proporción de ejemplos correctamente clasificados entre todas las predicciones positivas para una categoría.
- **Recall:** Proporción de ejemplos correctamente clasificados entre todas las instancias reales de esa categoría.
- **F1-Score:** Media armónica entre precision y recall.
- **Support:** Número de ejemplos reales de cada categoría en el conjunto de prueba.

### **2. Interpretación de las Categorías:**

- **entertainment:** Precision de 0.59, indicando que el modelo tiene dificultades para predecir esta categoría.
- **health:** El mejor rendimiento con un f1-score de 0.73.
- **politics:** El recall bajo (0.60) sugiere que el modelo pierde algunas noticias de esta categoría.
- **sports y technology:** Tienen métricas similares, lo que indica dificultades en la diferenciación.

### **3. Métricas Generales:**

- **Accuracy:** 0.66 → El modelo predijo correctamente el 66% de las noticias del conjunto de prueba.
- **Macro Avg:** Promedio no ponderado de todas las categorías.
- **Weighted Avg:** Promedio ponderado según la cantidad de ejemplos en cada categoría.

---


## **Pruebas por Categoría**

### **Tecnología**
1. “Apple presentó su último modelo de iPhone con una cámara revolucionaria.”
2. “Google lanza una actualización de su algoritmo de búsqueda.”
3. “Tesla introduce su nuevo software para conducción autónoma.”

### **Deportes**
1. “El equipo de fútbol local ganó en penales tras un empate a cero.”
2. “El tenista número uno del mundo avanzó a la final del torneo.”
3. “El maratón de Nueva York atrajo a miles de corredores este año.”

### **Política**
1. “El presidente anunció nuevas políticas para enfrentar la recesión mundial.”
2. “Se aprobó una ley para apoyar a los pequeños empresarios.”
3. “El parlamento discute reformas en el sistema educativo.”

### **Entretenimiento**
1. “La última serie de Netflix batió récords de audiencia.”
2. “El festival de cine presentó más de 50 películas independientes.”
3. “La cantante lanzó su nuevo álbum en todas las plataformas.”

### **Salud**
1. “Los médicos recomiendan caminar 30 minutos al día.”
2. “Se aprobó una nueva vacuna para combatir el virus.”
3. “Un estudio revela los beneficios del consumo de frutas y verduras.”

---


## **Posibles Razones de Errores del Modelo**

### **1. Categorías Similares**
- Noticias de **tecnología** y **entretenimiento** pueden solaparse si se habla de productos con impacto mediático (por ejemplo, lanzamientos de Apple).

### **2. Datos Desequilibrados**
- A pesar del **sobremuestreo**, la variabilidad en las categorías puede afectar la precisión en algunas predicciones.

### **3. Limitaciones del Modelo**
- **TF-IDF** no captura relaciones semánticas profundas entre palabras, lo que puede llevar a confusiones en la predicción.

### **4. Ambigüedad en las Descripciones**
- **Descripciones cortas o ambiguas** pueden no proporcionar suficiente información para una predicción precisa.

### **5. Falta de Datos de Entrenamiento**
- **Cantidad insuficiente de datos** puede reducir la capacidad del modelo para generalizar correctamente y clasificar las noticias de manera precisa.

---
## **Conclusión**
Este proyecto demuestra cómo implementar un sistema básico de **clasificación de texto** utilizando **Naive Bayes** y **TF-IDF**. Si bien el modelo muestra un rendimiento aceptable con una **precisión del 66%**, se podrían implementar mejoras utilizando técnicas más avanzadas, como **Word2Vec** o **BERT**. Este trabajo sienta las bases para futuros desarrollos más complejos en la clasificación de texto.

---