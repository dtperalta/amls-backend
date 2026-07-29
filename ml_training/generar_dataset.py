"""
Genera un dataset sintético para el ML Recommender Service.

El patrón que se le enseña al modelo:
- El factor DOMINANTE es el nivel de lectura del estudiante.
- El grado de pérdida auditiva tiene una influencia SECUNDARIA: a mayor
  grado, se recomienda un nivel ligeramente más conservador (más carga
  cognitiva al depender más de canales visuales).
- La preferencia comunicativa NO tiene relación real con la dificultad
  recomendada — se incluye como feature de todas formas, y el ruido
  aleatorio garantiza que el árbol no le asigne importancia artificial.
- Se agrega ruido aleatorio (10% de las filas) para simular variabilidad
  real y evitar que el patrón sea perfectamente determinista (un dataset
  sin ruido en absoluto no es realista y no sirve para practicar contra
  el sobreajuste, tema de la Lección 5 del propio curso).
"""
import numpy as np
import pandas as pd

np.random.seed(42)

GRADOS = ["Leve", "Moderada", "Profunda"]
NIVELES_LECTURA = ["Básico", "Intermedio", "Avanzado"]
PREFERENCIAS = ["Subtítulos", "Lengua de Señas", "Mixto"]
DIFICULTADES = ["Leve", "Moderada", "Avanzada"]

N_MUESTRAS = 600


def recomendar_dificultad_base(nivel_lectura: str, grado_perdida: str) -> str:
    """Regla subyacente (con la que se genera el dataset "verdadero")."""
    puntaje = {"Básico": 0, "Intermedio": 1, "Avanzado": 2}[nivel_lectura]

    # Influencia secundaria: mayor grado de pérdida -> ligero ajuste conservador
    ajuste = {"Leve": 0, "Moderada": 0, "Profunda": -1}[grado_perdida]

    puntaje_final = max(0, min(2, puntaje + (1 if ajuste == 0 else 0) - (1 if ajuste == -1 and puntaje > 0 else 0)))

    # Regla simplificada y explícita (evita índices negativos confusos)
    if nivel_lectura == "Básico":
        return "Leve"
    if nivel_lectura == "Intermedio":
        return "Leve" if grado_perdida == "Profunda" else "Moderada"
    # Avanzado
    return "Moderada" if grado_perdida == "Profunda" else "Avanzada"


filas = []
for _ in range(N_MUESTRAS):
    grado = np.random.choice(GRADOS)
    nivel_lectura = np.random.choice(NIVELES_LECTURA)
    preferencia = np.random.choice(PREFERENCIAS)  # sin relación real con la etiqueta

    dificultad = recomendar_dificultad_base(nivel_lectura, grado)

    # 10% de ruido: en esas filas, se asigna una dificultad aleatoria distinta
    if np.random.rand() < 0.10:
        dificultad = np.random.choice(DIFICULTADES)

    filas.append(
        {
            "grado_perdida_auditiva": grado,
            "nivel_lectura": nivel_lectura,
            "preferencia_comunicativa": preferencia,
            "nivel_dificultad_recomendado": dificultad,
        }
    )

df = pd.DataFrame(filas)
df.to_csv("dataset_sintetico.csv", index=False)
print(f"Dataset generado: {len(df)} filas")
print(df["nivel_dificultad_recomendado"].value_counts())
