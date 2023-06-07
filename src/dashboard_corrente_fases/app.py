from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from analise import dados_input_validacao, grafico_potencia, grafico_corrente

dados_df = dados_input_validacao()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(className='row', children="Energia, Corrente, Potência e as fases respectivas",
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(
            options=[
                {'label':'Potência Ativa','value':'Potência Ativa'},
                {'label':'Potência Reativa','value':'Potência Reativa'},
                {'label':'Fator de Potência','value':'Fator de Potência'},
            ],
            value='Potência Ativa',
            inline=True,
            id='control-radio-items')
        ]),

    html.Div(className='row', children=[
        dcc.RadioItems(
            options=['Valor Absoluto','Valor Relativo',],
            value='Valor Absoluto',
            inline=True,
            id='control-radio-items-value')
        ]),    
        
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
           dash_table.DataTable(data=dados_df.to_dict('records'),
                                 page_size=23,
                                 style_table={'overflowX':'auto'})
        ]),
        
       html.Div(className='six columns', children=[
           html.Div(className='five row', children=[
               dcc.Graph(figure={}, id='control-graph'),
           ]),
           html.Div(className='two row', children=[
                dcc.Graph(figure=grafico_corrente(dados_df))                   
           ])                 
       ])
    ])
])

@callback(
    Output(component_id='control-graph', component_property='figure'),
    [
        Input(component_id='control-radio-items', component_property='value'),
        Input(component_id='control-radio-items-value', component_property='value')
    ]
)

def atualiza_grafico(col_chosen, value_type):
    fig = grafico_potencia(dados_df, col_chosen, value_type)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
