from dash import Dash, html, dcc, dash_table, callback, Input, Output
import analise as an
import plotly.express as px
import plotly.graph_objects as go
from analise import Vibracao
import numpy as np


df, dff = an.le_dados()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,  external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.Div(
        className='row', 
        children='Analise de Vibração', 
        style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}
    ), 
    
    html.Div(className='row', children=[  
        html.Div(className='six columns', children=[
            # dash_table.DataTable(
            #     data=dff.to_dict('records'),
            #     page_size=29,
            #     style_table={'overflowXm':'auto'}
            # ),
        html.Div(children=[
                dcc.Graph(figure={}, id='grafico1')
            ]),
        ]),
        
        html.Div(className='six columns', children=[
            html.Div(className='row', children=[
                # html.Div(children=[
                #     dcc.Graph(figure={}, id='grafico1')
                # ]),
                html.Div(children=[
                    dcc.Graph(figure={}, id='grafico2'),
                ]),
                html.Div([
                    html.P('Ingrese um número entre 1 e 20 para visualizar'),
                    dcc.Input(id='num', type='number', debounce=False, min=1, max=20, step=1, value=1),
                    html.P(id='err', style={'color': 'red'}),
                    html.P(id='out_ligado'),
                    html.P(id='out_desligado')
                ]),
            ]),
        ]),
        html.Div(className='row', children=[
            dcc.RadioItems(
                options=[
                    {'label':'Exio X', 'value':'x'},
                    {'label':'Exio Y', 'value':'y'},
                    {'label':'Exio Z', 'value':'z'}
                ],
                value='x',
                inline=True,
                id='eixo-espectro',
            )
        ]),
        html.Div(className='column', children=[
            dcc.Graph(figure={}, id='graf_espectro')
        ]),        
    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            #html.Img(id='fase_relativa')        
            dcc.Graph(figure={}, id='fase_relativa')
        ]),
        html.Div(className='six columns', children=[
            #html.Img(id='fase_diff')
            dcc.Graph(figure={}, id='fase_diff')
        ])   
    ])
])

@app.callback(
    Output(component_id='grafico1', component_property='figure'),
    Input(component_id='num', component_property='value')
)

def atualiza_grafico_1(n):
    fig = an.plot_aceleracao(df[n-1],n-1)
    return fig

@app.callback(
    Output(component_id='grafico2', component_property='figure'),
    Input(component_id='num', component_property='value')
)

def atualiza_grafico_2(n):
    fig = an.grafica_temp(df[n-1])
    return fig


@app.callback(
    Output(component_id='graf_espectro', component_property='figure'),
    [
        Input(component_id='num', component_property='value'),
        Input(component_id='eixo-espectro', component_property='value')
    ]
)

def atualiza_fourier(n, eixo):
    vib = Vibracao(df[n-1])
    fig = vib.plot_espectro(eixo=eixo)
    return fig

@app.callback(
    Output(component_id='out_ligado', component_property='children'),
    Input(component_id='num', component_property='value')
)

def atualiza_tempo_ligado(n):
    vib = Vibracao(df[n-1])
    tempo_ligado, _ = vib.tempo_ligado()
    return f'Tempo ligado {tempo_ligado} [s]'

@app.callback(
    Output(component_id='out_desligado', component_property='children'),
    Input(component_id='num', component_property='value')
)

def atualiza_tempo_desligado(n):
    vib = Vibracao(df[n-1])
    _, tempo_desligado = vib.tempo_ligado()
    return f'Tempo desligado {tempo_desligado} [s]'


@app.callback(
#    Output(component_id='fase_relativa', component_property='src'),
    Output(component_id='fase_relativa', component_property='figure'),
    Input(component_id='num', component_property='value')
)

def atualiza_fase_relativa(n):
    vib = Vibracao(df[n-1])
#     data = an.plot_fase_relativa(vib)
#     return "data:image/png;base64,{}".format(data)
    phase_angle_xy, phase_angle_yz, phase_angle_zx, \
            differen_phase_angle_xy, differen_phase_angle_yz, differen_phase_angle_zx\
                = vib.phase()
    phase_angle_xy[np.abs(phase_angle_xy) < np.pi/2] = 0
    #phase_angle_yz[np.abs(phase_angle_yz) < np.pi/2] = 0
    #phase_angle_zx[np.abs(phase_angle_zx) < np.pi/2] = 0
    fig = go.Figure(go.Scatter(x=vib.frequencias, y=phase_angle_xy, mode='lines'))
    fig.update_xaxes(range=[0,21])
    fig.update_layout(
        title = 'Fase relativa entre Aceleração X e Aceleracão Y',
        xaxis_title = 'Frequência [Hz]',
        yaxis_title = 'Fase relativa [rad]'
    )

    return fig

@app.callback(
#    Output(component_id='fase_diff', component_property='src'),
    Output(component_id='fase_diff', component_property='figure'),
    Input(component_id='num', component_property='value')
)

def atualiza_fase_difer(n):
    vib = Vibracao(df[n-1])
    # data1 = an.plot_fase_diferencia(vib)
    # return "data1:image/png;base64,{}".format(data1)
    phase_angle_xy, phase_angle_yz, phase_angle_zx, \
        differen_phase_angle_xy, differen_phase_angle_yz, differen_phase_angle_zx\
              = vib.phase()
    differen_phase_angle_xy[np.abs(differen_phase_angle_xy) < 180] = 0
    #differen_phase_angle_yz[np.abs(differen_phase_angle_yz) < 180] = 0
    #differen_phase_angle_zx[np.abs(differen_phase_angle_zx) < 180] = 0
    fig = go.Figure(go.Scatter(x=vib.frequencias, y=differen_phase_angle_xy, mode='lines'))
    fig.update_xaxes(range=[0,21])
    fig.update_layout(
        title = 'Diferencia de fase entre Aceleração X e Aceleracão Y',
        xaxis_title = 'Frequência [Hz]',
        yaxis_title = 'Diferencia de Fase [º]'
    )
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)





