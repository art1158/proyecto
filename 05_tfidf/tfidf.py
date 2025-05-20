import numpy as np
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
#Documentos de salida
ruta_salida_durante_tf_idf = os.path.join(ruta_base, "matriz_tf_durante_idf.csv")
ruta_salida_finales_tf_idf = os.path.join(ruta_base, "matriz_tf_finales_idf.csv")
#Documentos de entrada
ruta_vocabulario_durante = os.path.join(ruta_base, "vocabulario_durante.txt")
ruta_vocabulario_finales = os.path.join(ruta_base, "vocabulario_finales.txt")
ruta_opi_durante = os.path.join(ruta_base, "opi_durante_preprocesadas.txt")
ruta_opi_finales = os.path.join(ruta_base, "opi_finales_preprocesadas.txt")

def cargar_vocabulario(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        vocabulario = [line.strip().lower() for line in f]
    return vocabulario

# Leer documentos desde archivo con formato: id | texto
def cargar_documentos(path):
    documentos = []
    with open(path, 'r', encoding='utf-8') as f:
        for linea in f:
            _, texto = linea.strip().split('|', 1)
            palabras = texto.lower().split()  # Tokenización
            documentos.append(palabras)
    return documentos

# Calcular TF (frecuencia de término) para cada documento
def calcular_tf(documentos, vocabulario):
    matriz_tf = np.zeros((len(documentos), len(vocabulario)))
    for i, doc in enumerate(documentos):
        for j, palabra in enumerate(vocabulario):
            matriz_tf[i, j] = doc.count(palabra)  # Contar ocurrencias de la palabra en el documento
    return matriz_tf

# Calcular IDF para cada palabra del vocabulario regresando el número de documentos que la contienen
def calcular_idf(documentos, vocabulario):
    num_docs = len(documentos)
    idf = np.zeros(len(vocabulario))

    for j, palabra in enumerate(vocabulario):
        df = sum(1 for doc in documentos if palabra in doc) #documentos que contienen la palabra
        if df > 0:
            idf[j] = (np.log10(num_docs / df)) + 1 #si es mayor a 0 se calcula el idf - es el num de documentos / df
        
        else:
            idf[j] = 0.0  # o np.log(num_docs), pero depende del tratamiento de palabras ausentes
    return idf

# Guardar matriz TF-IDF
def guardar_matriz_tfidf(matriz, salida):
    np.savetxt(salida, matriz, fmt='%.6f', delimiter=',')
    
# Calcular matriz TF-IDF
def calcular_tfidf(matriz_tf, idf):
    return matriz_tf * idf  # broadcasting de NumPy

# Procesar documentos durante el paro
documentos_durante = cargar_documentos(ruta_opi_durante)
vocabulario_durante = cargar_vocabulario(ruta_vocabulario_durante)
tf_durante = calcular_tf(documentos_durante, vocabulario_durante)
idf_durante = calcular_idf(documentos_durante, vocabulario_durante)
tfidf_durante = calcular_tfidf(tf_durante, idf_durante)
guardar_matriz_tfidf(tfidf_durante, ruta_salida_durante_tf_idf)

# Procesar documentos después del paro
documentos_finales = cargar_documentos(ruta_opi_finales)
vocabulario_finales = cargar_vocabulario(ruta_vocabulario_finales)
tf_finales = calcular_tf(documentos_finales, vocabulario_finales)
idf_finales = calcular_idf(documentos_finales, vocabulario_finales)
tfidf_finales = calcular_tfidf(tf_finales, idf_finales)
guardar_matriz_tfidf(tfidf_finales, ruta_salida_finales_tf_idf)

