import dash
from dash import html
from dash import dcc
import plotly.express as px
import os
import pandas as pd

# CARGA DE DATOS
directorio = '/home/julian/Documentos/Catedra-SostyCC'
archivos_csv = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.csv')]

ruta_csv_faltas = os.path.join('/home/julian/Documentos/Catedra-SostyCC/faltas_por_sesion.csv')
df_faltas_por_sesion = pd.read_csv(ruta_csv_faltas)

ruta_csv_justificaciones = os.path.join('/home/julian/Documentos/Catedra-SostyCC/inasistencias justificadas/justificaciones.csv')
df_justificaciones = pd.read_csv(ruta_csv_justificaciones)

ruta_csv_matriculados = os.path.join('/home/julian/Documentos/Catedra-SostyCC/matriculados/matriculados.csv')
datos_matriculados = pd.read_csv(ruta_csv_matriculados)

df_ausentes_por_sesion = pd.read_csv('sesiones_asistencia_ausentes.txt', sep='\t')
df_ausentes_por_sesion['sesion'] = df_ausentes_por_sesion['sesion'].astype(str)
df_ausentes_por_sesion['sesion'] = df_ausentes_por_sesion['sesion'].str.replace('sesion ', '')
df_ausentes_por_sesion['sesion'] = df_ausentes_por_sesion['sesion'].astype(int)
df_ausentes_por_sesion = df_ausentes_por_sesion.sort_values(by='sesion')

# CALCULOS
porcentaje_matriculados = datos_matriculados['OBSERVACIÓN'].value_counts(normalize=True) * 100

# GRAFICOS
fig_pastel_matriculados = px.pie(values=porcentaje_matriculados,
                                 names=porcentaje_matriculados.index,
                                 title='Porcentaje de Matriculados por Categoría',
                                 hole=0.5)

fig_ausentes = px.line(df_ausentes_por_sesion, x='sesion', y='ausentes',
                        title='Número de ausentes por sesión')


# Personalizar el estilo del gráfico
fig_ausentes.update_layout(
    plot_bgcolor='white',  # Establecer el color de fondo blanco
    xaxis=dict(showgrid=False, linecolor='black'), 
    yaxis=dict(showgrid=False, linecolor='black') 

)

# Crear el gráfico de barras comparativas
fig_barras_comparativas = px.bar(df_ausentes_por_sesion, x='sesion', y=['asistencia', 'ausentes'],
                                  barmode='group', labels={'value': 'Cantidad', 'variable': 'Tipo'},
                                  title='Asistencia vs Ausentes por Sesión')


# Personalizar el estilo del gráfico
fig_barras_comparativas.update_layout(
    plot_bgcolor='white',  # Establecer el color de fondo blanco
    xaxis=dict(showgrid=False, linecolor='black'),  # Mostrar líneas de la cuadrícula en el eje x y establecer el color de la cuadrícula en negro
    yaxis=dict(showgrid=False, linecolor='black')   # Mostrar líneas de la cuadrícula en el eje y y establecer el color de la cuadrícula en negro
)

# APLICACION
app = dash.Dash()

# Diseño de la aplicación
app.layout = html.Div(
    style={'max-width': '960px', 'margin': '0 auto'},  # Centrar horizontalmente el contenido
    children=[
        html.H1("Catedra Nacional de Sostenibilidad y Cambio Climatico"),
        
        # Primera fila
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_pastel_matriculados)
            ], className="six columns",style={'width': '45%', 'float': 'left'}),
            
            html.Div([
                dcc.Graph(figure=fig_ausentes)
            ], className="six columns",style={'width': '45%', 'float': 'left'}),
        ], className="row"),
        
        # Segunda fila
        html.Div([
            html.Div([
                dcc.Graph(figure=fig_barras_comparativas)
            ], className="twelve columns",style={'width': '90%', 'float': 'none', 'display': 'inline-block'})
        ], className="row")
    ]
)


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
