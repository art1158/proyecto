import pandas as pd
import os
import re
import string
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import stanza

#Inicializamos pipeline de Stanza
stanza.download("es")
nlp = stanza.Pipeline("es", processors="tokenize,mwt,pos,lemma", use_gpu=False)


# Ruta del archivo CSV
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(ruta_base, "datos_normalizados.csv")
ropiniones_durante = os.path.join(ruta_base, "opi_durante.txt")
ropiniones_finales = os.path.join(ruta_base, "opi_finales.txt")
opiniones_durante_preprocesadas = os.path.join(ruta_base, "opi_durante_preprocesadas.txt")
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
    stop_w = set(stopwords.words("spanish")) 
    # Crear la expresión regular para eliminar puntuación, signos y números, donde la expresion regular [0-9] quita numeros y la funcion punctutation quita todos los signos
    # Quitamos puntuación (excepto el guion "-") y números
    re_punc = re.compile('[%s0-9]' % re.escape(string.punctuation.replace("-", " ")))

    with open(ruta_entrada, "r", encoding="utf-8") as nuevoCargaDocumento, open(ruta_salida_preprocesado, "w",encoding="utf-8") as salidaDocumento:
        for linea in nuevoCargaDocumento:
            partes = linea.strip().split("|",1) # con esto esperamos eliminar espacios y saltos con strip y con split la creacion de una lista de palabras siguiendo el formato
            if len(partes) == 2:
                index, texto = partes # extraemos los valores diferentes
                #limpiar el texto
                texto = re_punc.sub(" ", texto) #Eliminamos puntuacion y numeros
                texto = texto.lower()
                #Procesar el texto con Stanza
                doc = nlp(texto)
                palabras_limpias = []
                for sentence in doc.sentences:
                    for word in sentence.words:
                        # Filtrar palabras vacías y agregar lemas
                        if word.text not in stop_w:
                            palabras_limpias.append(word.lemma)
                
                #Ordenar las palabras procesadas
                texto_ordenado_modificado = " ".join(palabras_limpias)
                
                #volvemos a guardar en el mismo formato
                salidaDocumento.write(f"{index} | {texto_ordenado_modificado}\n")

preprocesar_texto(ropiniones_durante, opiniones_durante_preprocesadas)
preprocesar_texto(ropiniones_finales, opiniones_finales_preprocesadas)
print("Opiniones extraídas y guardadas en 'opiniones_durante.txt' y 'opiniones_finales.txt'.")

## ======== Analisis de opiniones ========
def analizar_opiniones(ruta_entrada, ruta_salida, titulo_grafica):
    from collections import Counter
    import matplotlib.pyplot as plt
    
    #Leemos archivos preprocesados
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        palabras = []
        for linea in f:
            _, texto = linea.strip().split("|", 1) # Dividir en indice y texto
            palabras.extend(texto.split()) #Dividir el texto en palabras
            
        #Contar palabras mas frecuentes
        contador = Counter(palabras)
        palabras_comunes = contador.most_common(20) #20 palabras mas frecuentes
        palabras_no_comunes = contador.most_common()[:-21:-1] #20 palabras menos frecuentes
        
        #Graficar palabras frecuentes
        palabras, frecuencias = zip(*palabras_comunes)
        plt.figure(figsize=(10, 6))
        plt.barh(palabras, frecuencias, color='skyblue')
        plt.xlabel("Frecuencia")
        plt.ylabel("Palabras")
        plt.title(f"{titulo_grafica} más frecuentes")
        plt.gca().invert_yaxis()
        plt.savefig(ruta_salida.replace(".txt", "mas_frecuentes.png"))
        plt.show()
        plt.close()
        
        #Graficar palabras frecuentes
        palabras, frecuencias = zip(*palabras_no_comunes)
        plt.figure(figsize=(10, 6))
        plt.barh(palabras, frecuencias, color='skyblue')
        plt.xlabel("Frecuencia")
        plt.ylabel("Palabras")
        plt.title(f"{titulo_grafica} menos frecuentes")
        plt.gca().invert_yaxis()
        plt.savefig(ruta_salida.replace(".txt", "menos_frecuentes.png"))
        plt.show()
        plt.close()
#Analizar las opiniones preprocesadas
analizar_opiniones(opiniones_durante_preprocesadas, opiniones_durante_preprocesadas, "Palabras en opiniones durante el paro")
analizar_opiniones(opiniones_finales_preprocesadas, opiniones_finales_preprocesadas, "Palabras en opiniones finales")

