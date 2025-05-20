import os
import pandas as pd

# Rutas de entrada y salida
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_opi_durante = os.path.join(ruta_base, "opi_durante_preprocesadas.txt")
ruta_opi_finales = os.path.join(ruta_base, "opi_finales_preprocesadas.txt")
ruta_etiquetado_durante = os.path.join(ruta_base, "opi_durante_etiquetadas.txt")
ruta_etiquetado_finales = os.path.join(ruta_base, "opi_finales_etiquetadas.txt")
ruta_datos = os.path.join(ruta_base, "datos_normalizados.csv")

# Leer el archivo de etiquetas
df_etiquetas = pd.read_csv(ruta_datos)

# Asegurarse de que la última columna contiene las etiquetas
columna_etiquetas = df_etiquetas.columns[-1]  # Última columna
df_etiquetas = df_etiquetas.rename(columns={columna_etiquetas: "Etiqueta_Sentimiento"})

# Limpieza de etiquetas: eliminar espacios y convertir a minúsculas
df_etiquetas["Etiqueta_Sentimiento"] = df_etiquetas["Etiqueta_Sentimiento"].str.strip().str.lower()

# Reasignar etiquetas
mapeo_etiquetas = {
    "a favor": "positivo",
    "en contra": "negativo",
    "neutro": "neutro",
    "neutra": "neutro"
}
df_etiquetas["Etiqueta_Sentimiento"] = df_etiquetas["Etiqueta_Sentimiento"].map(mapeo_etiquetas)

# Verificar etiquetas no mapeadas
etiquetas_no_mapeadas = df_etiquetas[df_etiquetas["Etiqueta_Sentimiento"].isna()]
if not etiquetas_no_mapeadas.empty:
    print("Advertencia: Se encontraron etiquetas no mapeadas:")
    print(etiquetas_no_mapeadas)

# Leer los archivos de opiniones
def cargar_opiniones(ruta):
    opiniones = []
    with open(ruta, "r", encoding="utf-8") as f:
        for i, linea in enumerate(f):  # Usar el índice como identificador
            texto = linea.strip()
            opiniones.append({"Index": i, "Opinion": texto})
    return pd.DataFrame(opiniones)

df_durante = cargar_opiniones(ruta_opi_durante)
df_finales = cargar_opiniones(ruta_opi_finales)

# Añadir un índice temporal a las etiquetas
df_etiquetas = df_etiquetas.reset_index().rename(columns={"index": "Index"})

# Unir las etiquetas con las opiniones usando el índice
df_durante_etiquetado = pd.merge(df_durante, df_etiquetas[["Index", "Etiqueta_Sentimiento"]], on="Index", how="left")
df_finales_etiquetado = pd.merge(df_finales, df_etiquetas[["Index", "Etiqueta_Sentimiento"]], on="Index", how="left")

# Guardar los archivos etiquetados sin el índice adicional
def guardar_opiniones_etiquetadas(df, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"{row['Opinion']} | {row['Etiqueta_Sentimiento']}\n")

guardar_opiniones_etiquetadas(df_durante_etiquetado, ruta_etiquetado_durante)
guardar_opiniones_etiquetadas(df_finales_etiquetado, ruta_etiquetado_finales)

print(f"Opiniones durante el paro etiquetadas en: {ruta_etiquetado_durante}")
print(f"Opiniones después del paro etiquetadas en: {ruta_etiquetado_finales}")