import pandas as pd
import os
import re
import string
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

import spacy


# Ruta del archivo CSV
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(ruta_base, "datos_normalizados.csv")
ropiniones_durante = os.path.join(ruta_base, "opi_durante.txt")
ropiniones_finales = os.path.join(ruta_base, "opi_finales.txt")
opiniones_paro_preprocesadas = os.path.join(ruta_base, "opi_paro_preprocesadas.txt")
opiniones_finales_preprocesadas = os.path.join(ruta_base, "opi_finales_preprocesadas.txt")

# Leer el archivo CSV
df = pd.read_csv(ruta_csv)

# Extraer las columnas de opiniones
opiniones_paro = df["sentimientos_paro"].dropna().reset_index(drop=True)
opiniones_finales = df["sentimientos_finales"].dropna().reset_index(drop=True)

# Guardar las opiniones de "sentimientos_paro" en un archivo
with open(ropiniones_durante, "w", encoding="utf-8") as f:
    for i, opinion in enumerate(opiniones_paro, start=1):
        f.write(f"{i} | {opinion}\n")

# Guardar las opiniones de "sentimientos_finales" en un archivo
with open(ropiniones_finales, "w", encoding="utf-8") as f:
    for i, opinion in enumerate(opiniones_finales, start=1):
        f.write(f"{i} | {opinion}\n")
        
#========Preprocesado========
def preprocesar_texto(ruta_entrada, ruta_salida_preprocesado):
    snow = SnowballStemmer("spanish") #instancia para el stemmer en espanol
    # instancia para cargar als palabras vacias que vamos a eliminar
    stop_w = set(stopwords.words("spanish")) 
    # Crear la expresión regular para eliminar puntuación, signos y números, donde la expresion regular [0-9] quita numeros y la funcion punctutation quita todos los signos
    # Quitamos puntuación (excepto el guion "-") y números
    re_punc = re.compile('[%s0-9]' % re.escape(string.punctuation.replace("-", " ")))

    with open(ruta_entrada, "r", encoding="utf-8") as nuevoCargaDocumento, open(ruta_salida_preprocesado, "w",encoding="utf-8") as salidaDocumento:
        for linea in nuevoCargaDocumento:
            partes = linea.strip().split("|",1) # con esto esperamos eliminar espacios y saltos con strip y con split la creacion de una lista de palabras siguiendo el formato
            if len(partes) == 2:
                index, texto = partes # extraemos los valores diferentes

                #Tokenizar palabras (separarlas en una lista)
                palabras = texto.split()
                #Aqui hacemos uso de nuestra expresion regular y el escape de signos que cambiamos por espacios vacios
                palabras_limpias = [re_punc.sub("", word.replace("-"," ")) for word in palabras] #se cambian guiones por espacios

                #quitamos las palabras vacias y aplicamos snowball
                palabrasproceso = [snow.stem(word) for word in palabras_limpias if word not in stop_w]

                #ordenamos
                texto_ordenado_modificado = " ".join(palabrasproceso)

                #volvemos a guardar en el mismo formato
                salidaDocumento.write(f"{index} | {texto_ordenado_modificado}\n")

preprocesar_texto(ropiniones_durante, opiniones_paro_preprocesadas)
preprocesar_texto(ropiniones_finales, opiniones_finales_preprocesadas)


print("Opiniones extraídas y guardadas en 'opiniones_paro.txt' y 'opiniones_finales.txt'.")