import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os
import pandas as pd

# CARGA DE DATOS
directorio = './'
archivos_csv = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.csv')]

ruta_csv_faltas = os.path.join('faltas_por_sesion.csv')
df_faltas_por_sesion = pd.read_csv(ruta_csv_faltas)
df_faltas_por_sesion.nombre = df_faltas_por_sesion.nombre.str.capitalize()

ruta_csv_matriculados = os.path.join('matriculados/matriculados.csv')
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

server = app.server
# Layout de la aplicación
app.layout = html.Div([
    html.H1("Catedra Nacional de Sostenibilidad y Cambio Climatico"),
    
    # Dropdown para seleccionar el tipo de gráfico
    dcc.Dropdown(
        id='dropdown-graficos',
        options=[
            {'label': 'Gráficos', 'value': 'graficos'},
            {'label': 'Datos', 'value': 'datos'}
        ],
        value='graficos',  # Valor predeterminado
    ),
    
    # Div donde se mostrará el gráfico seleccionado
    html.Div(id='grafico-seleccionado')
])

# Callback para actualizar el gráfico según la opción seleccionada en el dropdown
@app.callback(
    Output('grafico-seleccionado', 'children'),
    [Input('dropdown-graficos', 'value')]
)
def actualizar_grafico(opcion):
    if opcion == 'graficos':
        return [
            html.Div(
                dcc.Graph(figure=fig_pastel_matriculados),
                style={'width': '45%', 'float': 'left', 'margin-right': '5px'}
            ),
            html.Div(
                dcc.Graph(figure=fig_ausentes),
                style={'width': '45%', 'float': 'left', 'margin-left': '5px'}
            ),
            html.Div(
                dcc.Graph(figure=fig_barras_comparativas),
                style={'width': '90%', 'float': 'none', 'display': 'inline-block', 'margin-left': '5px'}
            )
        ]
    if opcion == 'datos':
        return [
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in df_faltas_por_sesion.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(df_faltas_por_sesion.iloc[i][col]) for col in df_faltas_por_sesion.columns
                    ]) for i in range(len(df_faltas_por_sesion))
                ])
            ])
        ]

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
