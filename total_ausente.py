import pandas as pd

# Leer los archivos CSV
df_matriculados = pd.read_csv('matriculados/matriculados.csv')
sesiones = ['2', '3', '4', '5', '6', '7', '8']  # Números de sesión sin la extensión .csv

datos_sesiones = []

# Calcular el número de ausentes y asistentes para cada sesión
for sesion in sesiones:
    df_asistencia_sesion = pd.read_csv('/home/julian/Documentos/catedra/sesion ' + sesion + '.csv')
    total_matriculados = len(df_matriculados)
    total_asistencia_sesion = len(df_asistencia_sesion)
    ausentes_sesion = total_matriculados - total_asistencia_sesion
    datos_sesiones.append({'sesion': sesion, 'asistencia': total_asistencia_sesion, 'ausentes': ausentes_sesion})

# Crear DataFrame con las columnas "sesion", "asistencia" y "ausentes"
df_datos_sesiones = pd.DataFrame(datos_sesiones)

# Guardar el DataFrame en un archivo de texto
ruta_archivo_txt = 'sesiones_asistencia_ausentes.txt'
df_datos_sesiones.to_csv(ruta_archivo_txt, index=False, sep='\t')

print(f"El archivo '{ruta_archivo_txt}' se ha guardado correctamente.")