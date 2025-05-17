#En este codigo accederemos al archivo generado con las columans de interes para normalizar datos como nombres de columna y valores como el semestre
#Al final generamos un nuevo arvhico datos_normalizados en csv

import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Ruta del archivo Excel
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(ruta_base, "datos_seleccionados.xlsx")

# Leer el archivo Excel
df = pd.read_excel(ruta_excel)

#---------------Formateo de documentos----------------
##Normalizar nombres de columnas
df.rename(columns={"ID": "id","1. ¿Qué edad tienes?": "edad", "3. ¿Cuál es el semestre escolar que actualmente cursas?": "semestre",
                   "4. ¿Cuál es actualmente tu promedio escolar?": "promedio", "5. ¿Cuál es tu lugar de origen?": "origen",
                   "6. ¿Cuál es tu género?": "genero", "7. ¿Diariamente, cuánto horas dedicas a estudiar?": "horas_estudio",
                   "\n8. ¿Diariamente, cuánto tiempo dedicas a navegar en redes sociales?": "horas_redes", "9. ¿Cuántas horas duermes al día?": "horas_sueño",
                   "10. Actualmente tu nivel de estrés, lo consideras:": "nivel_estres", "1. ¿Participaste en el movimiento estudiantil de la BUAP el pasado febrero-marzo 2025?": "participacion_paro",
                   "2. ¿Cómo participaste?": "tipo_participacion", "De manera breve describe como participaste.": "descripcion_participacion",
                   "3. En un texto entre 3 y 5  líneas mínimo, expresa cómo te sentiste durante el movimiento estudiantil.": "sentimientos_paro", "4. ¿Cómo calificarías tu opinión con respecto al  movimiento estudiantil durante el mismo?": "postura",
                   "5. En un texto de  entre 3 y 5  líneas mínimo  expresa cómo te sentiste al concluir el  movimiento estudiantil.": "sentimientos_finales", "6. ¿Cómo calificarías tu opinión con respecto al movimiento estudiantil una vez que terminó?": "postura_final"
                     }, inplace=True)

df.set_index("id", inplace=True)
df.replace({'N/a': None, 'N/A': None, 'Ninguno': None, 'Ninguna': None, 'n/a': None}, inplace=True)                  

#---------------Normalizacion de datos----------------
#Diccionario para palabras a numeros
semestre_map = {
    "primero": 1,  "segundo": 2,  "tercero": 3,  "cuarto": 4, "quinto": 5, 
    "sexto": 6,  "septimo": 7, "octavo": 8, "noveno": 9, "decimo": 10, "décimo": 10
}

def normalizar_semestre(semestre):
    if pd.isna(semestre):
        return None
    #Convertir a minusculas
    semestre = str(semestre).lower()
    #Buscar numero en el texto
    numero = re.search(r'\d+', semestre)
    if numero:
        return int(numero.group()) #Si se encuentra un numero, devolverlo
    #Si no se encuentra un numero, buscar en el diccionario
    for palabra, valor in semestre_map.items():
        if palabra in semestre:
            return valor
    return None  # Si no se encuentra un número, devolver None

#Funcion para normalizar edades y eliminar palabras
def normalizar_edad(edad):
    if pd.isna(edad):
        return None
    # Convertir a string y eliminar caracteres no numéricos
    edad = str(edad)
    edad = re.sub(r'[^0-9]', '', edad)
    return int(edad) if edad else None

# Normalizar la columna "edad" (asegúrate de que exista) y pasar a enteros
if "edad" in df.columns:
    df["edad"] = df["edad"].apply(normalizar_edad)
    df["edad"] = pd.to_numeric(df["edad"], errors="coerce").fillna(0).astype(int)

# Normalizar la columna "semestre" (asegúrate de que exista) y passar a enteros
if "semestre" in df.columns:
    df["semestre"] = df["semestre"].apply(normalizar_semestre)
    df["semestre"] = pd.to_numeric(df["semestre"], errors="coerce").fillna(0).astype(int)

df['promedio'] = pd.to_numeric(df['promedio'], errors='coerce')

categoricas = ['genero', 'genero', 'nivel_estres', 'participacion_paro', 'postura', 'postura_final']
for col in categoricas:
    df[col] = df[col].astype('category')

for col in df.select_dtypes(include=['object', 'string', 'category']).columns:
    df[col] = df[col].str.lower()

#----------------Mostrar resumen----------------
print("Resumen de los datos normalizados:")
print(df.info()) 

#-----------------Exportar CSV----------------
ruta_csv = os.path.join(ruta_base, "datos_normalizados.csv")
df.to_csv(ruta_csv, index=False)

print(f"Datos normalizados guardados en '{ruta_csv}'.")
