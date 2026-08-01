"""
Genera el dataset sintético (v2) para el ML Recommender de ruta/contenido.

Cambio respecto a la v1: la señal DOMINANTE ahora es el desempeño real
demostrado en el quiz diagnóstico (porcentaje de acierto, cantidad de
lecciones ya dominadas) — no la autopercepción declarada en el perfil.
El nivel de lectura se conserva como un ajuste MENOR (afecta cómo se
presenta el contenido, no si la persona "sabe" del tema).

Esto resuelve una inconsistencia real detectada en producción: el
modelo v1 podía recomendar "Avanzada" a alguien que acertó solo 1 de
12 preguntas del quiz, porque se basaba únicamente en su perfil
declarado, sin conocer su desempeño real.
"""
import numpy as np
import pandas as pd

np.random.seed(42)

N_MUESTRAS = 800

NIVELES_LECTURA = ["Básico", "Intermedio", "Avanzado"]

porcentaje_acierto_quiz = np.random.uniform(0, 100, N_MUESTRAS)

# cantidad_lecciones_dominadas correlaciona con el % de acierto, pero con
# ruido real: acertar 1 de 2 preguntas en varias lecciones da buen %
# pero cero lecciones "dominadas" (se necesitan las 2 correctas de esa
# lección para contar como dominada) — un caso real, no un atajo.
base_dominadas = (porcentaje_acierto_quiz / 100) * 6
ruido_dominadas = np.random.normal(0, 1.2, N_MUESTRAS)
cantidad_lecciones_dominadas = np.clip(
    np.round(base_dominadas + ruido_dominadas), 0, 6
).astype(int)

nivel_lectura = np.random.choice(NIVELES_LECTURA, N_MUESTRAS)
ajuste_lectura = np.select(
    [nivel_lectura == "Básico", nivel_lectura == "Intermedio", nivel_lectura == "Avanzado"],
    [-8, 0, 8],
)

# Puntaje combinado: el quiz pesa mucho más que el nivel de lectura
puntaje_combinado = (
    porcentaje_acierto_quiz * 0.7
    + (cantidad_lecciones_dominadas / 6 * 100) * 0.25
    + ajuste_lectura * 0.05
)

nivel_dificultad = np.select(
    [puntaje_combinado >= 65, puntaje_combinado >= 35],
    ["Avanzada", "Moderada"],
    default="Leve",
)

df = pd.DataFrame(
    {
        "nivel_lectura": nivel_lectura,
        "porcentaje_acierto_quiz": porcentaje_acierto_quiz,
        "cantidad_lecciones_dominadas": cantidad_lecciones_dominadas,
        "nivel_dificultad_recomendado": nivel_dificultad,
    }
)

# 8% de ruido en la etiqueta, para evitar un patrón perfectamente separable
mascara_ruido = np.random.rand(N_MUESTRAS) < 0.08
opciones = np.array(["Leve", "Moderada", "Avanzada"])
df.loc[mascara_ruido, "nivel_dificultad_recomendado"] = np.random.choice(
    opciones, mascara_ruido.sum()
)

df.to_csv("dataset_sintetico_v2.csv", index=False)
print(f"Dataset generado: {len(df)} filas")
print(df["nivel_dificultad_recomendado"].value_counts())
