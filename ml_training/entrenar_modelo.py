"""
Entrena un Árbol de Decisión (Scikit-learn) para el ML Recommender Service,
y lo exporta junto con los codificadores de categorías.

Este modelo corre en el BACKEND (Cloud), no en el celular — por eso no
necesita convertirse a TensorFlow Lite. Es la adaptación de RUTA/CONTENIDO
(RF-1) de la propuesta original, fiel al "Árbol de Decisión" que ahí se
especifica.
"""
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("dataset_sintetico.csv")

FEATURES = ["grado_perdida_auditiva", "nivel_lectura", "preferencia_comunicativa"]
LABEL = "nivel_dificultad_recomendado"

# Codificadores: uno por cada columna categórica, para convertir texto <-> número
encoders = {col: LabelEncoder().fit(df[col]) for col in FEATURES + [LABEL]}

X = pd.DataFrame({col: encoders[col].transform(df[col]) for col in FEATURES})
y = encoders[LABEL].transform(df[LABEL])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# max_depth=4 a propósito: un árbol poco profundo, para que aprenda el
# patrón general en vez de memorizar el ruido (evitando el sobreajuste
# que se explica en la Lección 5 del propio curso).
modelo = DecisionTreeClassifier(max_depth=4, random_state=42)
modelo.fit(X_train, y_train)

pred_train = modelo.predict(X_train)
pred_test = modelo.predict(X_test)

print(f"Precisión en entrenamiento: {accuracy_score(y_train, pred_train):.2%}")
print(f"Precisión en prueba:        {accuracy_score(y_test, pred_test):.2%}")
print()
print("Reporte de clasificación (conjunto de prueba):")
print(
    classification_report(
        y_test, pred_test, target_names=encoders[LABEL].classes_
    )
)

# Guarda el modelo Y los encoders juntos (se necesitan ambos para usar
# el modelo después: los encoders traducen texto <-> número en ambas
# direcciones).
joblib.dump(
    {"modelo": modelo, "encoders": encoders, "features": FEATURES, "label": LABEL},
    "modelo_recomendador.joblib",
)
print("\nModelo guardado en modelo_recomendador.joblib")
