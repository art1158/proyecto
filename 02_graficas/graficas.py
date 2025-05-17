import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Ruta del archivo Excel
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(ruta_base, "datos_normalizados.csv")

df = pd.read_csv(ruta_excel, header=0)

print(df.head())
print(df.columns.tolist())

#horas de estudio vs promedio 
plt.figure(figsize=(11, 4))
sns.barplot(data=df, x='horas_estudio', y='promedio')
plt.title('Horas de estudio vs Promedio')
plt.tight_layout()
plt.savefig("estudiovscal.png")
plt.show()

#horas en redes sociales vs promedio
plt.figure(figsize=(11, 4))
sns.barplot(data=df, x='horas_redes', y='promedio')
plt.title('Horas en redes sociales vs Promedio')
plt.tight_layout()
plt.savefig("redesvscal.png")
plt.show()

#Pomedio vs semestre
plt.figure(figsize=(11, 4))
sns.barplot(data=df, x='semestre', y='promedio')
plt.title('Promedio vs Semestre')
plt.tight_layout()
plt.savefig("promediovsemestre.png")
plt.show()
