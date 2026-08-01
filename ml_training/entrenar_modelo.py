"""
Reentrena el Árbol de Decisión del ML Recommender (v2), usando desempeño
real del quiz diagnóstico en vez de solo autopercepción de perfil.
"""
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("dataset_sintetico.csv")

FEATURES_CATEGORICAS = ["nivel_lectura"]
FEATURES_NUMERICAS = ["porcentaje_acierto_quiz", "cantidad_lecciones_dominadas"]
LABEL = "nivel_dificultad_recomendado"

encoders = {col: LabelEncoder().fit(df[col]) for col in FEATURES_CATEGORICAS + [LABEL]}

X = pd.DataFrame(
    {
        "nivel_lectura": encoders["nivel_lectura"].transform(df["nivel_lectura"]),
        "porcentaje_acierto_quiz": df["porcentaje_acierto_quiz"],
        "cantidad_lecciones_dominadas": df["cantidad_lecciones_dominadas"],
    }
)
y = encoders[LABEL].transform(df[LABEL])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

modelo = DecisionTreeClassifier(max_depth=5, random_state=42)
modelo.fit(X_train, y_train)

pred_train = modelo.predict(X_train)
pred_test = modelo.predict(X_test)

print(f"Precisión en entrenamiento: {accuracy_score(y_train, pred_train):.2%}")
print(f"Precisión en prueba:        {accuracy_score(y_test, pred_test):.2%}")
print()
print(classification_report(y_test, pred_test, target_names=encoders[LABEL].classes_))

joblib.dump(
    {
        "modelo": modelo,
        "encoders": encoders,
        "features_categoricas": FEATURES_CATEGORICAS,
        "features_numericas": FEATURES_NUMERICAS,
        "label": LABEL,
    },
    "modelo_recomendador_v2.joblib",
)
print("\nModelo guardado en modelo_recomendador_v2.joblib")

# Prueba de sanidad: el caso exacto que detectaste (1/12 correctas, 0 dominadas)
prueba = pd.DataFrame({
    "nivel_lectura": [encoders["nivel_lectura"].transform(["Avanzado"])[0]],
    "porcentaje_acierto_quiz": [1 / 12 * 100],
    "cantidad_lecciones_dominadas": [0],
})
resultado = modelo.predict(prueba)[0]
print(f"\nCaso de prueba (1/12 correctas, nivel_lectura=Avanzado): {encoders[LABEL].inverse_transform([resultado])[0]}")
