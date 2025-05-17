#Lo primero que haremos sera acceder al archivo para seleccionar las columnas que son de nuestro interes y generar un nuevo archivo llamado datos_seleccionados

import pandas as pd
import os

# Ruta del archivo Excel
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(ruta_base, "Analisis_Opinion_Proyecto_RI.xlsx")

# Leer el archivo Excel
df = pd.read_excel(ruta_excel)

# Seleccionar las columnas específicas (índices basados en 0)
columnas_necesarias = [1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
df_seleccionado = df.iloc[:, columnas_necesarias]

# Mostrar las columnas seleccionadas a terminal 
print(df_seleccionado)

# Guardar las columnas seleccionadas en un nuevo archivo Excel que usaremos en el preprocesado
ruta_salida = os.path.join(ruta_base, "datos_seleccionados.xlsx")
df_seleccionado.to_excel(ruta_salida, index=False)