# **Sistema de Control Difuso para Aire Acondicionado**

## **Autor**
- **Alejandro Ignacio Ortiz Ortega**
--- 
## **Índice**
1. [Planteamiento del Problema](#planteamiento-del-problema)
2. [Introducción y Objetivo](#introducción-y-objetivo)
3. [Proceso de Desarrollo](#proceso-de-desarrollo)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Instrucciones de Uso](#instrucciones-de-uso)
6. [Implementación de Lógica Difusa](#implementación-de-lógica-difusa)
7. [Diseño de la Interfaz Gráfica](#diseño-de-la-interfaz-gráfica)
8. [Comentarios Importantes del Código](#comentarios-importantes-del-código)
9. [Pruebas y Validación](#pruebas-y-validación)
10. [Conclusión](#conclusión)

---

## **Planteamiento del Problema**

Desarrollar un sistema de control difuso que regule el funcionamiento de un aire acondicionado (AC) en función de las 
condiciones climáticas actuales, específicamente la temperatura y la humedad. El sistema debe obtener datos climáticos 
en tiempo real y ajustar el nivel de enfriamiento del AC de manera eficiente. Además, se requiere una interfaz gráfica 
de usuario (GUI) atractiva e interactiva que permita al usuario ingresar la ciudad de la cual obtener los datos climáticos 
y visualizar los resultados de forma dinámica.

---

## **Introducción y Objetivo**

El objetivo principal de este proyecto es implementar un sistema inteligente que utilice la lógica difusa para controlar 
un aire acondicionado basado en las condiciones climáticas actuales. La lógica difusa permite manejar la incertidumbre y 
proporcionar un control más humano y adaptable.

Adicionalmente, se busca desarrollar una interfaz gráfica amigable y visualmente atractiva utilizando PyQt5, incorporando 
animaciones y efectos visuales que mejoren la experiencia del usuario.

---

## **Proceso de Desarrollo**

### **1. Obtención de Datos Climáticos**
- Se utiliza la **API de WeatherAPI** para obtener datos climáticos en tiempo real de una ciudad específica.
- Se maneja la respuesta de la API para asegurar que los datos sean correctos y se implementa manejo de errores en caso 
de respuestas inválidas.

### **2. Implementación de Lógica Difusa**
- Se definen las variables difusas de **temperatura**, **humedad** y **ajuste del AC** utilizando la biblioteca 
**scikit-fuzzy.**
- Se establecen las funciones de membresía para cada variable.
- Se crean reglas difusas que relacionan las variables de entrada con la salida.

### **3. Diseño de la Interfaz Gráfica**
- Se utiliza **PyQt5** para construir la GUI.
- Se añaden elementos visuales como imágenes de fondo, íconos y estilos personalizados.
- Se incorporan animaciones y efectos visuales para mejorar la interactividad.

### **4. Integración y Pruebas**
- Se integra la lógica difusa con la interfaz gráfica.
- Se realizan pruebas para asegurar el correcto funcionamiento del sistema en diversos escenarios.

---

## **Estructura del Proyecto**

- **Código Principal**: Contiene la implementación del sistema difuso y la interfaz gráfica.
- **Recursos:**: 
  - **background.jpg**: Imagen de fondo de la aplicación.
  - **icon.png**: Ícono utilizado en la interfaz.
  
- **Dependencias**:
  - `requests`
  - `scikit-fuzzy`
  - `numpy`
  - `PyQt5`

---

## **Instrucciones de Uso**

### **1. Preparación**
Instala las dependencias necesarias:
```bash
pip install requests scikit-fuzzy numpy PyQt5
```

### **2. Configuración**
- Obtén una **API Key** válida de [WeatherAPI](https://www.weatherapi.com/) y reemplázala en la variable `API_KEY` 
dentro del código. 
    ```python
    API_KEY = 'TU_API_KEY'  # Reemplaza con tu clave de API
    ```
    **Nota**: No compartas tu API Key públicamente.


### **3. Archivos Necesarios**
- Asegúrate de tener los archivos `background.jpg` y `icon.png` en el mismo directorio que el script principal.

### **4. Ejecución del Programa**

- Ejecuta el script desde la terminal o tu entorno de desarrollo:
    ```bash
    python control_ac.py
    ```

### **5. Uso de la Aplicación**
- Al iniciar, ingresa el nombre de la ciudad en el campo correspondiente.
- Haz clic en "Ejecutar Simulación" para obtener los datos climáticos y el ajuste recomendado del AC.

---

## **Implementación de Lógica Difusa**

### **1. Variables Difusas**
- **Entradas**:
  - Temperatura (`-10°C` a `40°C`):
    - Fría
    - Moderada
    - Caliente
  - Humedad (`0%` a `100%`):
    - Baja
    - Media
    - Alta
- **Salida**
  - Ajuste del AC (`0%` a `100%`):
  - Bajo
  - Medio
  - Alto
  
### **2. Funciones de Membresía**
- Se definen funciones de membresía trapezoidales y triangulares para cada categoría.
- Ejemplos:
  - Temperatura fría: `fuzz.trapmf(temperatura.universe, [-10, -10, 0, 15])`
  - Humedad alta: `fuzz.trapmf(humedad.universe, [60, 80, 100, 100])`

### **3. Reglas Difusas**
- **Regla 1**: Si la temperatura es fría o la humedad es baja, entonces el ajuste del AC es bajo.
- **Regla 2**: Si la temperatura es moderada, entonces el ajuste del AC es medio.
- **Regla 3**: Si la temperatura es caliente y la humedad es alta, entonces el ajuste del AC es alto.

### **4. Inferencia y Defuzzificación**
- Se utiliza el método de inferencia de **Mamdani**.
- La defuzzificación se realiza mediante el método del centroide para obtener un valor preciso de salida.

---
## **Diseño de la Interfaz Gráfica**

### **1. Elementos Principales**
- **Ventana Principal**:
  - Tamaño fijo de `600x500` píxeles.
  - Imagen de fondo personalizada.
- **Título**:
  - Texto estilizado con fuente Arial y tamaño `26`.
  - Color azul profundo (`#1565C0) con efecto de sombra.
- **Campo de Entrada**:
  - Etiqueta "Ingrese la ciudad:" con estilo y fuente en negrita y tamaño `14`.
  - Campo de texto estilizado con fondo semitransparente y bordes redondeados.
- **Botón**
  - Botón "Ejecutar Simulación" con degradado azul y efectos al interactuar.
- **Etiqueta de Resultados**:
  - Muestra la información climática y el ajuste del AC.
  - Estilizada con fondo semitransparente oscuro y texto claro.

### **2. Estilos y Efectos**
- Se aplican estilos **CSS** para mejorar la apariencia de los widgets.
- Uso de colores que representan el clima, principalmente tonos de azul.
- Bordes redondeados y sombras para dar profundidad a los elementos.
---


## **Comentarios Importantes del Código**

### **1. Función `obtener_datos_climaticos(ciudad)`**
- **Descripción**: Obtiene los datos climáticos actuales de la ciudad ingresada utilizando la API de WeatherAPI.
- **Retorna**: Temperatura, humedad, URL del ícono del clima y descripción de las condiciones climáticas.
- **Manejo de Errores**: Si la API no responde correctamente, retorna `None` en todos los valores.

### **2. Definición de Variables Difusas**
- **Variables de Entrada**:
  - **Temperatura**: Categorías difusas definidas como fría, moderada y caliente.
  - **Humedad**: Categorías difusas definidas como baja, media y alta.
- **Variable de Salida**:
  - **Ajuste del AC**: Indica el nivel de ajuste necesario para el aire acondicionado (bajo, medio, alto).
- **Funciones de Membresía**: Se utilizan funciones trapezoidales (`fuzz.trapmf`) y triangulares (`fuzz.trimf) para modelar las 
categorías difusas.

### **3. Reglas Difusas**
- Las reglas establecen la lógica de control, relacionando las variables de entrada con la salida.
- Ejemplo de una regla:
  ```python
  regla1 = ctrl.Rule(temperatura['fria'] | humedad['baja'], ajuste_ac['bajo'])
  ```

### **4. Clase `VentanaPrincipal`**
- **Responsabilidad**: Maneja la interfaz gráfica de usuario (GUI) y las interacciones del usuario.
- **Componentes Clave**:
  - **Animaciones**: Incluye animaciones como la aparición suave de la ventana y el movimiento de salto del ícono.
  - **Configuración de la UI**: Crea y estiliza widgets, y organiza los elementos en la ventana.
  - **Método `ejecutar_simulacion(self)`**:
    - Se activa al presionar el botón o la tecla Enter.
    - Obtiene la ciudad ingresada y valida la entrada.
    - Llama a la función para obtener los datos climáticos.
    - Actualiza la interfaz con la información obtenida.
    - Calcula el ajuste del aire acondicionado utilizando el sistema difuso.

### **5. Animaciones y Efectos**
- **Animación de Entrada**: La ventana aparece gradualmente aumentando su opacidad de 0 a 1 en 500 ms.
- **Movimiento del Ícono**: El ícono realiza un movimiento de salto hacia arriba y hacia abajo para captar la atención del usuario.
- **Efectos al Interactuar**:
  - El botón cambia ligeramente de tamaño y color al pasar el cursor o ser presionado.
  - El campo de entrada cambia su opacidad al enfocarse.
 
---


## **Pruebas y Validación**
- Se realizaron pruebas ingresando diferentes ciudades para verificar la correcta obtención y visualización de los datos climáticos.
- Se validó el funcionamiento del sistema difuso comprobando que el ajuste del AC sea coherente con las condiciones climáticas.
- Se probaron las animaciones y efectos visuales para asegurar una experiencia de usuario fluida y agradable.
- Se manejaron excepciones y errores, mostrando mensajes de advertencia en caso de entradas inválidas o problemas de conexión.
---
## **Conclusión**
Este proyecto combina la **lógica difusa** con una **interfaz gráfica interactiva** para crear un sistema inteligente de control 
de aire acondicionado. Al utilizar datos climáticos en tiempo real y reglas difusas, el sistema proporciona 
recomendaciones eficientes y adaptadas a las necesidades del usuario. Las animaciones y efectos visuales enriquecen 
la experiencia, haciendo que la aplicación sea no solo funcional sino también atractiva y moderna.

---