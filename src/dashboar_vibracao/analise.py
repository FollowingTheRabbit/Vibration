import os
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import time
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

matplotlib.use('agg') #to plot plt in dash

def le_dados(PATH='../../Data/Dados de Vibração e Temperatura/'):
    """
    Le os arquivos de vibração desde o caminho asignado.
    Asocia a cada arquivo os tempos de duração baseado no nome do arquivo.
    Retorna uma lista de DataFrames, df, com cada arquivo e um DataFrame, dff, com todos os arquivos juntos.
    """
    
    direct = os.listdir(PATH)
    df = []
    direct
    for n, dr in enumerate(direct):
        #print(n,' lendo:', dr)
        start, end = int(str(dr).strip('.csv').split('-')[0]), int(str(dr).strip('.csv').split('-')[1]) 
        datetime_start = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(start))
        datetime_end = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(end))
        #print(f'Dados desde {datetime_start} até {datetime_end}')
        vib_df = pd.read_csv(PATH+dr, names=['x','y','z','Temperature  ºC'], sep=',')
        t_i = pd.to_datetime(datetime_start, format="%a, %d %b %Y %H:%M:%S +0000")
        t_f = pd.to_datetime(datetime_end, format="%a, %d %b %Y %H:%M:%S +0000")
        #delta_t = t_f - t_i
        #print(a)
        vib_df['t'] = pd.date_range(t_i, t_f, len(vib_df))
        df.append(vib_df)
    

    dff = pd.DataFrame(columns=df[0].columns)
    for n in range(len(df)):
        dff = pd.concat([dff,df[n]], ignore_index=True)

    return df, dff

def tempo_op(df):
    time_components = (str(df.iloc[-1]['t'] - df.iloc[0]['t']).split(' ')[-1]).split(':')
    hours, minutes, seconds = map(int, time_components)
    total_seconds = hours * 3600 + minutes * 60 + seconds
    
    return total_seconds

Df, _ = le_dados()
total_sec = []
for n in range(len(Df)):
     total_sec.append(tempo_op(Df[n]))
total_sec   
 
def plot_aceleracao(df,n):
    fig1 = go.Figure(data=go.Scatter(x=df.index*total_sec[n]/len(df), y=df['x'], mode='lines', name='Eixo X'))
    fig2 = go.Figure(data=go.Scatter(x=df.index*total_sec[n]/len(df), y=df['y'], mode='lines', name='Eixo Y'))
    fig3 = go.Figure(data=go.Scatter(x=df.index*total_sec[n]/len(df), y=df['z'], mode='lines', name='Eixo Z'))
    fig = go.Figure(data=fig1.data+fig2.data+fig3.data)

    #fig.update_xaxes(range=[0, total_sec[n]])
    fig.update_layout(
        title = dict(text='', x=0.5, xanchor='center'),
        xaxis_title = 'Tempo [s]',
        yaxis_title = 'Aceleração [m/s²]',
    )
    #fig.show()
    
    return fig

def grafica_temp(df):
    fig = go.Figure()
    fig = px.scatter(x=df.index*total_sec[n]/len(df),y=df['Temperature  ºC'], trendline='ols', trendline_color_override='magenta')
    fig.add_trace(
       go.Scatter(x=df.index*total_sec[n]/len(df),y=df['Temperature  ºC'], mode='lines', line_color='blue')
    )
    #fig.update_traces(showlegend=True)
    fig.update_layout(
        yaxis_title = 'Temperatura [ºC]',
        xaxis_title = 'Tempo [s]'
    )
    #fig.show()
    return fig

def polt_total(dff):
    fig, _ = plt.subplots(figsize=(11,5))
    plt.subplot(121)
    plt.scatter(dff.t, dff.x, label='Eixo X')
    plt.scatter(dff.t, dff.y, label='Eixo Y')
    plt.scatter(dff.t, dff.z, label='Eixo Z')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Aceleração [m/s²]')
    plt.xticks(rotation=45)

    plt.subplot(122)
    plt.scatter(dff.t, dff['Temperature  ºC'])
    plt.xticks(rotation=45)
    plt.xlabel('Tempo [s]')
    plt.ylabel('Temperatura [ºC]')
    fig.show()
    return fig 

class Vibracao:
    def __init__(self, df):
        self.df = df
        self.x = df.x.to_numpy()
        self.y = df.y.to_numpy()
        self.z = df.z.to_numpy()
        self.t = df.t.to_numpy()
        self.t = df.index.to_numpy()
        self.N = df.shape[0]
        
        self.total_sec = tempo_op(df)
        self.sample_rate = self.N/self.total_sec
        
        self.fourier_x = fft(self.x)
        self.fourier_y = fft(self.y)
        self.fourier_z = fft(self.z)
        
        self.frequencias = fftfreq(self.N, 1.0/self.total_sec)
      
        
    def rms(self, imprime=True):
        self.rms_x = np.sqrt(np.mean(self.x**2))
        self.rms_y = np.sqrt(np.mean(self.y**2))
        self.rms_z = np.sqrt(np.mean(self.z**2))
        
        if imprime == True:
            print('Valor RMS para os eixos x: %1.2f, y: %1.2f, z: %1.2f' %(self.rms_x, self.rms_y, self.rms_z))
        
        return self.rms_x, self.rms_y, self.rms_z
    
    def pico_pico(self, imprime=True):
        self.pico_pico_x = np.max(self.x) - np.min(self.x)
        self.pico_pico_y = np.max(self.y) - np.min(self.y)
        self.pico_pico_z = np.max(self.z) - np.min(self.z)
        
        if imprime == True:
            print('Valor Pico-Pico para os eixos x: %1.2f, y: %1.2f, z: %1.2f'
                  %(self.pico_pico_x, self.pico_pico_y, self.pico_pico_z))
        
        return self.pico_pico_x, self.pico_pico_y, self.pico_pico_z
    
    
    def uptime_downtime(self, thresh=0.15):
        self.rms(imprime=False)
        self.pico_pico(imprime=False)
        
        magnitude_x = np.abs(self.fourier_x)
        magnitude_y = np.abs(self.fourier_y)
        magnitude_z = np.abs(self.fourier_z)
                
        magnitude_x = magnitude_x[magnitude_x <= 2000]
        #magnitude_y = magnitude_y[magnitude_y <= 2000]
        magnitude_z = magnitude_z[magnitude_z <= 2000]
        
        max_magnitude_x = np.max(magnitude_x)
        max_magnitude_y = np.max(magnitude_y)
        max_magnitude_z = np.max(magnitude_z)
        
        threshold_x = thresh*max_magnitude_x
        threshold_y = thresh*max_magnitude_y
        threshold_z = thresh*max_magnitude_z
        
        significant_peak_index_x = np.where(magnitude_x >= threshold_x)[0]
        significant_peak_index_y = np.where(magnitude_y >= threshold_y)[0]
        significant_peak_index_z = np.where(magnitude_z >= threshold_z)[0]  
        
        significant_peak_frequencies_x = self.frequencias[significant_peak_index_x]
        significant_peak_frequencies_y = self.frequencias[significant_peak_index_y]
        significant_peak_frequencies_z = self.frequencias[significant_peak_index_z]
         
        if (len(significant_peak_frequencies_x) <= 9000) and (len(significant_peak_frequencies_z) <= 9000) and \
            (self.rms_y >= 0.05) and (self.pico_pico_y >= 0.3):
            return True
        
        return False
    
    def tempo_ligado(self):
        df_c = self.df.copy()        
        window = 10
        passo = 5
        df_c['y_rms'] = df_c.y.apply(lambda y: y*y).rolling(window=window, min_periods=1).apply(lambda x: x[:-1].mean()).apply(np.sqrt)
        df_c['pico_pico'] = df_c.y.rolling(window=window, min_periods=1).max()\
                            -df_c.y.rolling(window=window, min_periods=1).min()
        df_c['y_rms']
        df_c['sec'] = [td.total_seconds() for td in (df_c.t - df_c.t.iloc[0])]
        df_c['sec']
        ligado = True
        tempo_desligado = 0
        q = 0
        for p in range(int(passo), len(df_c)-passo, int(passo)):
            #print(p, df_c.loc[p,'sec'], df_c.loc[p,'pico_pico'], df_c.loc[p,'y_rms'])
            if ((df_c.loc[p,'pico_pico'] <= 0.05) or (df_c.loc[p,'y_rms'] <= 0.5)) and ligado==True:
                ligado = False
                tempo_desligado = tempo_desligado + df_c.loc[p,'sec'] - df_c.loc[q,'sec']
                q = p
            elif ((df_c.loc[p,'pico_pico'] <= 0.05) or (df_c.loc[p,'y_rms'] <= 0.5)) and ligado==False:
                tempo_desligado = tempo_desligado + df_c.loc[p,'sec'] - df_c.loc[q,'sec']
                q = p
            else:
                ligado=True
                q = p
                #print('ligado en t=', ultimo_instante_desligado)
        #print('desligado ', tempo_desligado, 's')
        df_c.iloc[-1:,7].values[0]
        #print('ligado ', df_c.iloc[-1:,7].values[0]-tempo_desligado, 's')
        tempo_ligado = df_c.iloc[-1:,7].values[0]-tempo_desligado
        
        return tempo_ligado, tempo_desligado
    
    def plot_espectro(self, eixo='x'):
        fig = go.Figure()

        if eixo=='x':
            fig.add_trace(
                go.Scatter(x=rfftfreq(self.N, d=1/self.sample_rate), y=np.abs(rfft(self.x))/(self.N/2.0), mode='lines', name='Eixo X')
            )
        
        elif eixo=='y':
            fig.add_trace(
                go.Scatter(x=rfftfreq(self.N, d=1/self.sample_rate), y=np.abs(rfft(self.y))/(self.N/2.0), mode='lines', name='Eixo Y')
            )

        else:
            fig.add_trace(
                go.Scatter(x=rfftfreq(self.N, d=1/self.sample_rate), y=np.abs(rfft(self.z))/(self.N/2.0), mode='lines', name='Eixo Z')
            )           
      
        fig.update_yaxes(range=[0, 0.25])
        fig.update_layout(
            title = 'Espectro',
            xaxis_title = 'Frequência [Hz]',
            yaxis_title = 'Amplitude'
        )
        #fig.show()
        return fig
        
    def plot_temperatura(self):
        plt.subplots(figsize=(13,7))
        plt.subplot(211)
        plt.plot(df[n].index*total_sec[n]/len(df[n]), df[n]['Temperature  ºC'])
        sns.regplot(data=df[n], x=df[n].index*total_sec[n]/len(df[n]), y=df[n]['Temperature  ºC'],
                    line_kws={'color':'b'}, scatter=False, label='Tendência')
        #plt.xlim(0,10)
        #plt.xlabel('Tempo [s]')
        plt.ylabel('Temperatura [ºC]')
        plt.title('Registro Completo')
        plt.legend()

        plt.subplot(212)
        plt.plot(df[n].index*total_sec[n]/len(df[n]), df[n]['Temperature  ºC'])
        plt.xlim(0,2)
        plt.xlabel('Tempo [s]')
        plt.ylabel('Temperatura [ºC]')
        plt.title('Zoom no tempo')
        plt.show()
        
    def phase(self):
        relative_phase_angle_xy = np.angle(self.fourier_x/self.fourier_y, deg=False)
        relative_phase_angle_yz = np.angle(self.fourier_y/self.fourier_z, deg=False)
        relative_phase_angle_zx = np.angle(self.fourier_z/self.fourier_x, deg=False)
        
        differen_phase_angle_xy = np.angle(self.fourier_x, deg=True)-np.angle(self.fourier_y, deg=True)
        differen_phase_angle_yz = np.angle(self.fourier_y, deg=True)-np.angle(self.fourier_z, deg=True)
        differen_phase_angle_zx = np.angle(self.fourier_z, deg=True)-np.angle(self.fourier_x, deg=True)
        
        #print(f'Valor fase para os eixos xy: {phase_angel_xy}, yz: {phase_angel_yz}, zx: {phase_angel_zx}')                
        
        return relative_phase_angle_xy, relative_phase_angle_yz, relative_phase_angle_zx,\
                differen_phase_angle_xy, differen_phase_angle_yz, differen_phase_angle_zx
        

def plot_fase_relativa(vib):
    phase_angle_xy, phase_angle_yz, phase_angle_zx, differen_phase_angle_xy, differen_phase_angle_yz, differen_phase_angle_zx = vib.phase()
    phase_angle_xy[np.abs(phase_angle_xy) < np.pi/2] = 0
    phase_angle_yz[np.abs(phase_angle_yz) < np.pi/2] = 0
    phase_angle_zx[np.abs(phase_angle_zx) < np.pi/2] = 0
    buf = io.BytesIO()
    plt.plot(vib.frequencias, phase_angle_xy)
    #plt.plot(vib.frequencias, phase_angle_yz)
    #plt.plot(vib.frequencias, phase_angle_zx)
    #plt.xlim(0,10)
    plt.title('Fase relativa entre Aceleração X e Aceleracão Y')
    plt.ylabel('Fase relativa [rad]')
    plt.xlabel('Frequência [Hz]')
    #plt.show()
    plt.savefig(buf, format = "png")
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    buf.close()

    return data

def plot_fase_diferencia(vib):
    phase_angle_xy, phase_angle_yz, phase_angle_zx, differen_phase_angle_xy, differen_phase_angle_yz, differen_phase_angle_zx = vib.phase()
    buff = io.BytesIO()
    plt.bar(range(vib.N), differen_phase_angle_xy)
    plt.xlabel('Registros')
    plt.ylabel('Diferencia de [º]')
    plt.title('Diferencia de fase entre Aceleração X e Aceleracão Y')
    #plt.show()
    plt.savefig(buff, format = "png")
    plt.close()
    data1 = base64.b64encode(buff.getbuffer()).decode("utf8") # encode to html elements
    buff.close()

    return data1