import pandas as pd
import os

# Cargar el archivo de matriculados
matriculados_df = pd.read_csv("matriculados/matriculados.csv")

# Crear un DataFrame para almacenar las faltas
faltas_df = pd.DataFrame(columns=["nombre", "documento", "faltas"])

# Obtener los archivos de sesiones a partir de la sesión 3
sesiones_files = [file for file in os.listdir() if file.startswith("sesion") and file.endswith(".csv")]
sesiones_files = sorted(sesiones_files, key=lambda x: int(x.split(".")[0][-1]))[2:]  # Ordenar y seleccionar desde la sesión 3 en adelante

for sesion_file in sesiones_files:
    # Cargar el archivo de la sesión
    sesion_df = pd.read_csv(sesion_file)
    
    # Obtener la lista de documentos de la sesión
    documentos_sesion = sesion_df.iloc[:, 4].tolist()
    
    # Contar las faltas para esta sesión
    for _, row in matriculados_df.iterrows():
        documento = row["DOCUMENTO"]
        nombre = row["APELLIDOS Y NOMBRE"]
        if documento not in documentos_sesion:
            # Si el documento no está en la lista de la sesión, aumentar el contador de faltas
            faltas_df = pd.concat([faltas_df, pd.DataFrame({"nombre": [nombre], "documento": [documento], "faltas": [1]})], ignore_index=True)

# Agrupar y contar el total de faltas por estudiante
faltas_df = faltas_df.groupby(["nombre", "documento"]).agg({"faltas": "sum"}).reset_index()

# Guardar el DataFrame de faltas en un archivo CSV
faltas_df.to_csv("faltas_por_sesion.csv", index=False)
