import requests
import pandas as pd
import ssl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import SMOTE
import nltk

# === Configuración para evitar errores SSL ===
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Descargar stopwords si no están disponibles
nltk.download('stopwords')

# === Configuración de la API de NewsAPI ===
API_KEY = '8f76e3959ef94d108a86dc528f476967'
base_url = "https://newsapi.org/v2/everything?"


# Función para obtener noticias desde la API
def obtener_noticias(consulta, paginas=3):
    noticias = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    for pagina in range(1, paginas + 1):
        url = f"{base_url}q={consulta}&language=en&page={pagina}&apiKey={API_KEY}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            noticias.extend(response.json().get('articles', []))
        else:
            print(f"Error al obtener noticias en la página {pagina}: {response.status_code}")
            break
    return noticias


# Obtener noticias para varias categorías
categorias = ['technology', 'sports', 'politics', 'entertainment', 'health']
datos = []

for categoria in categorias:
    noticias = obtener_noticias(categoria)
    if not noticias:
        print(f"No se encontraron noticias para la categoría: {categoria}")
        continue
    for noticia in noticias:
        descripcion = noticia.get('description', "")
        # Validar que la descripción no sea None antes de aplicar strip()
        if descripcion and descripcion.strip():
            datos.append({'descripcion': descripcion, 'categoria': categoria})

# Crear DataFrame con los datos
df = pd.DataFrame(datos)

if df.empty or len(df['categoria'].unique()) < 2:
    print("No hay suficientes datos para entrenar el modelo.")
    exit()

# Preprocesamiento con TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 3))
X = vectorizer.fit_transform(df['descripcion'])
y = df['categoria']

# Aplicar SMOTE para balancear las categorías
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

print(f"Distribución de categorías después del sobremuestreo:\n{pd.Series(y_resampled).value_counts()}")

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3,
                                                    stratify=y_resampled, random_state=42)

# Optimización del hiperparámetro alpha usando GridSearchCV
param_grid = {'alpha': [0.1, 0.5, 1.0, 5.0, 10.0]}
grid = GridSearchCV(MultinomialNB(), param_grid, cv=5)
grid.fit(X_train, y_train)

# Entrenar el modelo con el mejor alpha
mejor_alpha = grid.best_params_['alpha']
modelo = MultinomialNB(alpha=mejor_alpha)
modelo.fit(X_train, y_train)

# Evaluar el Modelo
y_pred = modelo.predict(X_test)
print(f"\nPrecisión del modelo: {accuracy_score(y_test, y_pred):.2f}")
print("\nInforme de clasificación:")
print(classification_report(y_test, y_pred))


# Función para predecir categoría
def predecir_categoria(descripcion):
    X_nueva = vectorizer.transform([descripcion])
    prediccion = modelo.predict(X_nueva)
    return prediccion[0]


# Interacción con el usuario
if __name__ == "__main__":
    while True:
        nueva_descripcion = input("\nEscribe una nueva descripción (o 'salir' para terminar): ")
        if nueva_descripcion.lower() == 'salir':
            break
        categoria_predicha = predecir_categoria(nueva_descripcion)
        print(f"La categoría predicha es: {categoria_predicha}")