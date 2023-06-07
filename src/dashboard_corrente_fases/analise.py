import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def dados_input_validacao():
    input_df = pd.read_csv('../../Data/Input v2.csv', sep=';')
    input_df.dropna(inplace=True)
    
    validacao_df = pd.read_csv('../../Data/Validação v2.csv', encoding='unicode_escape', header=[0,1], sep=';')
    validacao_df.columns = ['_'.join(col) for col in validacao_df.columns]
    validacao_df.columns
    validacao_df.columns = ['DATA','energia_ativa_f1 Kwh (Consumo)','energia_ativa_f2 Kwh (Consumo)','energia_ativa_f3 Kwh (Consumo)',
                            'energia_ativa_total Kwh (Consumo)','energia_aparente_f1 kVAh','energia_aparente_f2 kVAh','energia_aparente_f3 kVAh',
                            'energia_aparente_total kVAh','energia_reativa_f2 kvarh','energia_reativa_f1 kvarh','energia_reativa_f3 kvarh',
                            'energia_reativa_total kvarh','fator_potencia_f1 kvarh','fator_potencia_f2 kvarh','fator_potencia_f3 kvarh',
                            'Fator_Potencia_Total kvarh', 'potencia_aparente_f1 VA','potencia_aparente_f2 VA','potencia_aparente_f3 VA',
                            'potencia_aparente_total VA','potencia_ativa_f1 W','potencia_ativa_f2 W','potencia_ativa_f3 W','potencia_ativa_total W',
                            'potencia_reativa_f1 var','potencia_reativa_f2 var','potencia_reativa_f3 var','potencia_reativa_total var','temperatura ºC',
                            'tensao_f1_f2 V','tensao_f2_f3 V','tensao_f3_f1 V','angulo_tensao_f1 º','angulo_tensao_f2 º','angulo_tensao_f3 º']
    validacao_df.drop_duplicates()
    validacao_df.isna().sum(), validacao_df.shape
    input_df.isna().sum(), input_df.shape

    indx = input_df.loc[input_df.DATA.isin(validacao_df.DATA)].index
    #input_df.loc[~input_df.DATA.isin(validacao_df.DATA)]
    idx = validacao_df.loc[validacao_df.DATA.isin(input_df.DATA)].index
    validacao_df.loc[~validacao_df.DATA.isin(input_df.DATA)]

    #input_df.loc[indx]
    df1 = pd.merge(validacao_df.loc[idx], input_df.loc[indx], on='DATA', how='left').drop_duplicates()

    cols = ['DATA', 'corrente_neutro',
            'potencia_reativa_f1 var', 'potencia_reativa_f2 var','potencia_reativa_f3 var','potencia_reativa_total var',
            'potencia_ativa_f1 W','potencia_ativa_f2 W', 'potencia_ativa_f3 W','potencia_ativa_total W', 
            'fator_potencia_f1 kvarh','fator_potencia_f2 kvarh', 'fator_potencia_f3 kvarh','Fator_Potencia_Total kvarh', 
            'energia_ativa_total Kwh (Consumo)', 'energia_reativa_total kvarh']
    df2 = df1[cols].copy()
    df2.DATA = pd.to_datetime(df2.DATA, format='%d/%m/%Y %H:%M')
    #df1.sort_values(by='DATA', ascending=False, inplace=True)
    for col in df2.select_dtypes('object').columns:
        df2[col] = df2[col].str.replace(',','.').astype('float')

    df2['Hora'] = df2.DATA.dt.strftime('%H:%M')

    return df2

def grafico_potencia(df, cols_chosen, values_type):
    if cols_chosen == 'Potência Ativa':
        val_total = 'potencia_ativa_total W'
        fase_1 = 'potencia_ativa_f1 W'
        fase_2 = 'potencia_ativa_f2 W'
        fase_3 = 'potencia_ativa_f3 W'
        name = 'Potência Ativa '

    elif cols_chosen == 'Potência Reativa':
        val_total = 'potencia_reativa_total var'
        fase_1 = 'potencia_reativa_f1 var'
        fase_2 = 'potencia_reativa_f2 var'
        fase_3 = 'potencia_reativa_f3 var'
        name = 'Potência Retiva '        

    elif cols_chosen == 'Fator de Potência':
        val_total = 'Fator_Potencia_Total kvarh'
        fase_1 = 'fator_potencia_f1 kvarh'
        fase_2 = 'fator_potencia_f2 kvarh'
        fase_3 = 'fator_potencia_f3 kvarh'
        name = 'Fator de Potência '        

    if values_type == 'Valor Absoluto':
        title = 'Valor Absoluto'
        fig1 = go.Figure(data=go.Scatter(x=df.DATA, y=df[val_total], mode='lines', name= name+'Total'))
        fig2 = go.Figure(data=go.Scatter(x=df.DATA, y=df[fase_1], mode='lines', name=name+'f1'))
        fig3 = go.Figure(data=go.Scatter(x=df.DATA, y=df[fase_2], mode='lines', name=name+'f2'))
        fig4 = go.Figure(data=go.Scatter(x=df.DATA, y=df[fase_3], mode='lines', name=name+'f3'))
        fig = go.Figure(data=fig1.data+fig2.data+fig3.data+fig4.data)

    elif values_type == 'Valor Relativo':
        title = 'Valor Porcentual'
        fig1 = go.Figure(data=go.Scatter(x=df.DATA, y=100*df[fase_1]/df[val_total], mode='lines', name=name+'f1'))
        fig2 = go.Figure(data=go.Scatter(x=df.DATA, y=100*df[fase_2]/df[val_total], mode='lines', name=name+'f2'))
        fig3 = go.Figure(data=go.Scatter(x=df.DATA, y=100*df[fase_3]/df[val_total], mode='lines', name=name+'f3'))
        fig = go.Figure(data=fig1.data+fig2.data+fig3.data)
    
    fig.update_layout(
        title = dict(text=title, x=0.5, xanchor='center'),
        xaxis_title = 'Data e Hora'
    )
    #fig.show()
    return fig

def grafico_corrente(df):
    fig = px.scatter(
        df, 
        y='Fator_Potencia_Total kvarh',
        x='corrente_neutro',
        size='energia_ativa_total Kwh (Consumo)',
        color='energia_reativa_total kvarh',
        hover_data=['Hora'],
        size_max=13
    )

    fig.update_layout(
        title = dict(text='Corrente, Energia e Fator de Potência Totais'),
        yaxis_title = 'Fator de Potência Total [kvarh]',
        xaxis_title = 'Corrente Total [A]',
        coloraxis_colorbar = dict(title='Energia Reativa Total [kvarh]')
    )
    #fig.show()

    return fig