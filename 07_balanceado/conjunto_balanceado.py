import pandas as pd
import os

# Rutas de entrada y salida
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_opi_durante = os.path.join(ruta_base, "opi_durante_etiquetadas.txt")
ruta_opi_finales = os.path.join(ruta_base, "opi_finales_etiquetadas.txt")
ruta_balanceado_durante = os.path.join(ruta_base, "opi_durante_balanceadas.txt")
ruta_balanceado_finales = os.path.join(ruta_base, "opi_finales_balanceadas.txt")

# Cargar opiniones etiquetadas
def cargar_opi(ruta):
    opiniones = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(" |", 2)  # Dividir en índice, opinión y etiqueta
            if len(partes) == 3:
                _, texto, etiqueta = partes  # Ignorar el índice
                opiniones.append({"Opinion": texto.strip(), "Etiqueta": etiqueta.strip()})
            else:
                print(f"Línea mal formateada: {linea.strip()}")
    return pd.DataFrame(opiniones)

# Balancear opiniones
def balancear_opiniones(df):
    # Contar número de opiniones por clase
    conteo_clases = df["Etiqueta"].value_counts()
    print("Distribución antes del balanceo:")
    print(conteo_clases)

    n_min = conteo_clases.min()  # Tamaño de la clase minoritaria
    print(f"Tamaño de la clase minoritaria: {n_min}")
    
    # Balancear
    df_balanceado = (
        df.groupby("Etiqueta", group_keys=False)
        .apply(lambda x: x.sample(n=n_min, random_state=42))
    )
    return df_balanceado

# Guardar opiniones balanceadas
def guardar_balanceadas(df, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"{row['Opinion']} | {row['Etiqueta']}\n")

# Función para cargar opiniones balanceadas
def cargar_opiniones_balanceadas(ruta):
    opiniones = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(" |", 1)
            if len(partes) == 2:
                texto, etiqueta = partes
                opiniones.append({"Opinion": texto.strip(), "Etiqueta": etiqueta.strip()})
    return pd.DataFrame(opiniones)

# Cargar y contar posturas en los archivos balanceados
def imprimir_distribucion(ruta, nombre_archivo):
    df = cargar_opiniones_balanceadas(ruta)
    print(f"Distribución de posturas en {nombre_archivo}:")
    print(df["Etiqueta"].value_counts())
    print()

# Procesar y balancear opiniones durante el paro
df_durante = cargar_opi(ruta_opi_durante)
df_durante_balanceado = balancear_opiniones(df_durante)
guardar_balanceadas(df_durante_balanceado, ruta_balanceado_durante)

# Procesar y balancear opiniones después del paro
df_finales = cargar_opi(ruta_opi_finales)
df_finales_balanceado = balancear_opiniones(df_finales)
guardar_balanceadas(df_finales_balanceado, ruta_balanceado_finales)

# Imprimir distribución de posturas en los archivos finales
imprimir_distribucion(ruta_balanceado_durante, "opi_durante_balanceadas.txt")
imprimir_distribucion(ruta_balanceado_finales, "opi_finales_balanceadas.txt")