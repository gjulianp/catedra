import pandas as pd
import os
import matplotlib.pyplot as plt

# Cargar el archivo de matriculados
matriculados_df = pd.read_csv("matriculados/matriculados.csv")
matriculados_df.DOCUMENTO = matriculados_df.DOCUMENTO.astype(str).str.strip()
matriculados_df.DOCUMENTO = matriculados_df.DOCUMENTO.astype(int)

# Crear un DataFrame para almacenar las faltas
faltas_df = pd.DataFrame(columns=["nombre", "documento", "faltas"])

# Lista para almacenar los números de sesión en los que se presentaron faltas
sesiones_presentadas = []

# Obtener los archivos de sesiones a partir de la sesión 3
sesiones_files = [file for file in os.listdir() if file.startswith("sesion") and file.endswith(".csv") and not file.startswith("sesion 8")]
sesiones_files = sorted(sesiones_files, key=lambda x: int(x.split(".")[0][-1]))[1:]  # Ordenar y seleccionar desde la sesión 3 en adelante
# Iterar sobre cada archivo de sesión y cargarlo en un solo DataFrame

for sesion_file in sesiones_files:
    # Cargar el archivo de la sesión
    sesion_df = pd.read_csv(sesion_file)
    #quitar espacios en blanco de la quinta columna
    sesion_df.Documento = sesion_df.Documento.astype(str).str.strip()
    sesion_df.Documento = sesion_df.Documento.astype(int)

    # Obtener la lista de documentos de la sesión
    documentos_sesion = sesion_df.iloc[:, 4].tolist()
    
    # Contar las faltas para esta sesión
    for _, row in matriculados_df.iterrows():
        documento = row["DOCUMENTO"]
        nombre = row["APELLIDOS Y NOMBRE"]
        if documento not in documentos_sesion:
            # Si el documento no está en la lista de la sesión, aumentar el contador de faltas
            faltas_df = pd.concat([faltas_df, pd.DataFrame({"nombre": [nombre], "documento": [documento], "faltas": [1]})], ignore_index=True)
            # Agregar el número de sesión actual a la lista de sesiones_presentadas
            sesiones_presentadas.append(int(sesion_file.split(".")[0][-1]))

# Agregar una columna "sesiones" a faltas_df y llenarla con los números de sesión
faltas_df["sesiones"] = sesiones_presentadas

# Agrupar y contar el total de faltas por estudiante
faltas_df = faltas_df.groupby(["nombre", "documento"]).agg({"faltas": "sum", "sesiones": lambda x: list(x)}).reset_index()

# Guardar el DataFrame de faltas en un archivo CSV
faltas_df.to_csv("faltas_por_sesion.csv", index=False)

# Contar cuántos estudiantes tienen cada cantidad de faltas
faltas_por_cantidad = faltas_df['faltas'].value_counts()

# Contar cuántos estudiantes tienen cada cantidad de faltas
faltas_por_cantidad = faltas_df['faltas'].value_counts().reset_index()
faltas_por_cantidad.columns = ['cantidad_faltas', 'cantidad_estudiantes']

# Guardar el DataFrame con los datos de cantidad de estudiantes por cantidad de faltas
faltas_por_cantidad.to_csv("cantidad_faltas.csv", index=False)