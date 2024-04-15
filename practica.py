import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os
import pandas as pd
import base64

# Función para modificar el color de todas las trazas de una figura
def aplicar_paleta_de_colores(figura, paleta):
    figura.update_traces(marker=dict(colors=paleta))
    return figura
# CARGA DE DATOS
directorio = './'
archivos_csv = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.csv')]

ruta_csv_faltas = os.path.join('faltas_por_sesion.csv')
df_faltas_por_sesion = pd.read_csv(ruta_csv_faltas)
df_faltas_por_sesion.nombre = df_faltas_por_sesion.nombre.str.capitalize()
df_faltas_por_sesion = df_faltas_por_sesion.sort_values(by='faltas',ascending=False)

ruta_csv_matriculados = os.path.join('matriculados/matriculados.csv')
datos_matriculados = pd.read_csv(ruta_csv_matriculados)

df_ausentes_por_sesion = pd.read_csv('sesiones_asistencia_ausentes.txt', sep='\t') 
df_ausentes_por_sesion['sesion'] = df_ausentes_por_sesion['sesion'].astype(str)
df_ausentes_por_sesion['sesion'] = df_ausentes_por_sesion['sesion'].str.replace('sesion ', '')
df_ausentes_por_sesion['sesion'] = df_ausentes_por_sesion['sesion'].astype(int)
df_ausentes_por_sesion = df_ausentes_por_sesion.sort_values(by='sesion')

df_cantidad_faltas = pd.read_csv("cantidad_faltas.csv")

# CALCULOS
porcentaje_matriculados = datos_matriculados['OBSERVACIÓN'].value_counts(normalize=True) * 100

# GRAFICOS
fig_pastel_matriculados = px.pie(values=porcentaje_matriculados,
                                 names=porcentaje_matriculados.index,
                                 title='Porcentaje de Matriculados por Categoría',
                                 hole=0.5)

fig_pastel_matriculados = aplicar_paleta_de_colores(fig_pastel_matriculados, px.colors.sequential.YlGnBu)

fig_pastel_matriculados.update_layout(title={'text': 'Porcentaje de Matriculados por Categoría', 
                                             'x':0.5, 'y':0.9, 'xanchor': 'center', 'yanchor': 'top'})

fig_ausentes = px.line(df_ausentes_por_sesion, x='sesion', y='ausentes',
                        title='Número de ausentes por sesión')
fig_ausentes.update_traces(line=dict(width=3))  # Ajustar el ancho de la línea a 3
fig_ausentes.update_layout(title={'text': 'Número de ausentes por sesión',
                                  'x':0.5, 'y':0.9, 'xanchor': 'center', 'yanchor': 'top'})
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
fig_barras_comparativas.update_layout(title={'text': 'Asistencia vs Ausentes por Sesión',
                                              'x': 0.5, 'y': 0.9, 'xanchor': 'center', 'yanchor': 'top'})

# Agregar colores personalizados a las barras de asistencia y ausentes
fig_barras_comparativas.update_traces(marker_color='#26c485', selector=dict(name='asistencia'))
fig_barras_comparativas.update_traces(marker_color='#32908F', selector=dict(name='ausentes'))

# Personalizar el estilo del gráfico
fig_barras_comparativas.update_layout(
    plot_bgcolor='white',  # Establecer el color de fondo blanco
    xaxis=dict(showgrid=False, linecolor='black'),  # Mostrar líneas de la cuadrícula en el eje x y establecer el color de la cuadrícula en negro
    yaxis=dict(showgrid=False, linecolor='black')   # Mostrar líneas de la cuadrícula en el eje y y establecer el color de la cuadrícula en negro
)




fig_pastel_cantidad_faltas = px.pie(values=df_cantidad_faltas['cantidad_faltas'],
                                     names=df_cantidad_faltas.index,
                                     title='Cantidad de faltas',
                                     hole=0.5)
fig_pastel_cantidad_faltas = aplicar_paleta_de_colores(fig_pastel_cantidad_faltas, px.colors.sequential.YlGnBu)
fig_pastel_cantidad_faltas.update_layout(title={'text': 'Cantidad de faltas',
                                                'x':0.5, 'y':0.9, 'xanchor': 'center', 'yanchor': 'top'})

# APLICACION
app = dash.Dash()

server = app.server

# Ruta de la imagen
image_filename = 'fondo de pantalla.jpg'  # Nombre de tu imagen
encoded_image = base64.b64encode(open(image_filename, 'rb').read())  # Leer y codificar la imagen

# Layout de la aplicación
app.layout = html.Div(style={'backgroundColor': '#f2f2f2'}, children=[  # Establecer el color de fondo gris claro
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '100%'}),  # Agrega la imagen de fondo aquí
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
                style={'width': '45%', 'float': 'left', 'margin-right': '5px', 'margin-top': '5px','margin-left': '80px'}
            ),
            html.Div(
                dcc.Graph(figure=fig_ausentes),
                style={'width': '45%', 'float': 'left', 'margin-top': '5px'}
            ),
            html.Div(
                dcc.Graph(figure=fig_barras_comparativas),
                style={'width': '90%', 'float': 'none', 'display': 'inline-block', 'margin-top': '5px', 'margin-left': '80px'}
            )
        ]
    if opcion == 'datos':
        return [
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col, style={'background-color': '#f2f2f2', 'border': '1px solid black'}) for col in df_faltas_por_sesion.columns], style={'text-align': 'center'})
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(df_faltas_por_sesion.iloc[i][col], style={'text-align': 'center', 'border': '1px solid black', 'background-color': '#f9f9f9' if i % 2 == 0 else '#e9e9e9'}) for col in df_faltas_por_sesion.columns
                    ]) for i in range(len(df_faltas_por_sesion))
                ])
            ]),
            # html.Div(
            #     dcc.Graph(figure=fig_pastel_cantidad_faltas),
            #     style={'width': '90%', 'float': 'none', 'display': 'inline-block', 'margin-left': '5px'}
            # )
        ]

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
