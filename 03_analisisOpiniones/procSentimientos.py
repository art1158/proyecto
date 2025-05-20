import pandas as pd
import os
import re
import string
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import stanza
from collections import Counter
import matplotlib.pyplot as plt

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
if not os.path.exists(ropiniones_durante):
    # Guardar las opiniones de "sentimientos_paro" en un archivo
    with open(ropiniones_durante, "w", encoding="utf-8") as f:
        for i, opinion in enumerate(opiniones_paro, start=1):
            f.write(f"{i} | {opinion}\n")
    print(f"Archivo generado: {ropiniones_durante}")
else:
    print(f"Archivo ya existe: {ropiniones_durante}")

# Guardar las opiniones de "sentimientos_finales" en un archivo
if not os.path.exists(ropiniones_finales):
    # Guardar las opiniones de "sentimientos_finales" en un archivo
    with open(ropiniones_finales, "w", encoding="utf-8") as f:
        for i, opinion in enumerate(opiniones_finales, start=1):
            f.write(f"{i} | {opinion}\n")
    print(f"Archivo generado: {ropiniones_finales}")
else:
    print(f"Archivo ya existe: {ropiniones_finales}")
        
#========Preprocesado========
def preprocesar_texto(ruta_entrada, ruta_salida_preprocesado):
    stop_w = set(stopwords.words("spanish")) 
    # Crear la expresión regular para eliminar puntuación, signos y números, donde la expresion regular [0-9] quita numeros y la funcion punctutation quita todos los signos
    # Quitamos puntuación (excepto el guion "-") y números
    re_punc = re.compile('[%s0-9]' % re.escape(string.punctuation))

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
                        if word.text not in stop_w: #Se usaa word.text para filtrar palabras vacías despues de la lematización
                            palabras_limpias.append(word.lemma)
                
                #Ordenar las palabras procesadas
                texto_ordenado_modificado = " ".join(palabras_limpias)
                
                #volvemos a guardar en el mismo formato
                salidaDocumento.write(f"{index} | {texto_ordenado_modificado}\n")

# Verificar si los archivos preprocesados ya existen antes de generarlos
if not os.path.exists(opiniones_durante_preprocesadas):
    preprocesar_texto(ropiniones_durante, opiniones_durante_preprocesadas)
    print(f"Archivo preprocesado generado: {opiniones_durante_preprocesadas}")
else:
    print(f"Archivo preprocesado ya existe: {opiniones_durante_preprocesadas}")
if not os.path.exists(opiniones_finales_preprocesadas):
    preprocesar_texto(ropiniones_finales, opiniones_finales_preprocesadas)
    print(f"Archivo preprocesado generado: {opiniones_finales_preprocesadas}")
else:
    print(f"Archivo preprocesado ya existe: {opiniones_finales_preprocesadas}")

## ======== Analisis de opiniones ========
def analizar_opiniones(ruta_entrada, ruta_salida, titulo_grafica):    
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

#======= Analisis categorico =======
#Agrupar datos por cateogria seleccionada
def analizar_datos_por_categoria(df, columna_categoria, ruta_preprocesado, ruta_salida_base, titulo_base):
    with open(ruta_preprocesado, "r", encoding="utf-8") as f:
        opiniones_preprocesadas = {}
        for linea in f:
            index, texto = linea.strip().split("|", 1)  # Dividir en índice y texto
            opiniones_preprocesadas[int(index)] = texto.strip()

    #Acumular palabras por categoria
    categorias = df[columna_categoria].dropna().unique() #btenemos valores unicos  por categoria (columna)
    palabras_por_categoria = {}
    
    for categoria in categorias:
        # Filtrar opiniones por categoria
        indices_categoria = df[df[columna_categoria] == categoria].index
        
        #Combinar las opiniones preprocesadas con los indices de la categoria
        palabras = []
        for idx in indices_categoria:
            if idx + 1 in opiniones_preprocesadas:
                palabras.extend(opiniones_preprocesadas[idx + 1].split())
                
        # Contar palabras más frecuentes para la categoría
        palabras_por_categoria[categoria] = Counter(palabras).most_common(20) #20 palabras mas frecuentes
        
    #Crear grafica combinada
    plt.figure(figsize=(12, 8))
    for categoria, palabras_comunes in palabras_por_categoria.items(): #Top 10 palabras mas frecuentes por categoria
        palabras, frecuencias = zip(*palabras_comunes)
        plt.barh([f"{palabra} ({categoria})" for palabra in palabras], frecuencias, label=f"{categoria}") #Mostramos la categoria en la grafica
    
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabras (categoria)")
    plt.title(titulo_base)
    plt.legend(title=columna_categoria, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(ruta_salida_base.replace(".txt", f"_{columna_categoria}.png"))
    plt.show()
    plt.close()           
        
    
analizar_datos_por_categoria(df, "genero", opiniones_durante_preprocesadas, "palabras_genero", "Palabras mas frecuentes por género")
analizar_datos_por_categoria(df, "semestre", opiniones_durante_preprocesadas, "palabras_semestre", "Palabras más frecuentes por semestre (durante el paro)")
analizar_datos_por_categoria(df, "edad", opiniones_finales_preprocesadas, "palabras_edad", "Palabras más frecuentes por edad (finales)")
