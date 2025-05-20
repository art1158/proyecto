#Rutas
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_vocabulario_durante = os.path.join(ruta_base, "vocabulario_durante.txt")
ruta_vocabulario_finales = os.path.join(ruta_base, "vocabulario_finales.txt")
ruta_durante = os.path.join(ruta_base, "opi_durante_preprocesadas.txt")
ruta_finales = os.path.join(ruta_base, "opi_finales_preprocesadas.txt")

def obtener_vocabulario(ruta_documentos):
    # Abrir el archivo de entrada
    with open(ruta_documentos, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # Obtener todas las palabras únicas de la colección (de 2 o más letras)
    vocabulario = set()
    for linea in lineas:
        partes = linea.split('|')
        if len(partes) < 2:
            continue  # Saltar líneas mal formateadas
        
        palabras = partes[1].strip().lower().split()
        palabras_filtradas = [p for p in palabras if len(p) >= 2]  # Filtrar palabras con 2 o más letras
        vocabulario.update(palabras_filtradas)
    
    return vocabulario

def procesar_vocabulario(ruta_documentos, ruta_vocabulario):
    # Llamar a la función para obtener el vocabulario
    vocabulario = obtener_vocabulario(ruta_documentos)

    # Ordenar el vocabulario y obtener su longitud
    vocabulario_ordenado = sorted(vocabulario)
    longitud_vocabulario = len(vocabulario_ordenado)

    with open(ruta_vocabulario, 'w', encoding='utf-8') as f:
        f.write('\n'.join(vocabulario_ordenado) + '\n')

    print("Longitud del vocabulario:", longitud_vocabulario)
    
procesar_vocabulario(ruta_durante, ruta_vocabulario_durante)
procesar_vocabulario(ruta_finales, ruta_vocabulario_finales)
