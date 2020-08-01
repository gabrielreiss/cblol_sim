import pandas as pd
import os
import numpy as np

BASE_DIR = os.path.dirname('.')
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')

atual = pd.read_csv(os.path.join(DATA_DIR,'atual.csv'),encoding='utf-8')
rodadas = pd.read_csv(os.path.join(DATA_DIR,'rodadas.csv'),encoding='utf-8')

def simulacao(atual,rodadas,sim_n):
    atual.index = atual['sigla']
    rodadas['sim'] = 0
    for i in range(0, rodadas.shape[0]):
        if np.random.random_sample() >= 0.5:
            rodadas['sim'][i] = rodadas['time1'][i]
        else:
            rodadas['sim'][i] = rodadas['time2'][i]

    resultado = rodadas['sim'].groupby(rodadas['sim']).count()

    r2 = pd.merge(atual,resultado,how='left',left_index=True,right_index=True)
    r2 = r2.fillna(0)
    r3 = pd.DataFrame({
        'sim':sim_n,
        'sigla':r2['sigla'],
        'pontos':r2['Pontos']+r2['sim']
    })
    r3 = r3.sort_values(by='pontos',ascending=False)
    r3['class']=0
    r3['class'][0:4]=1
    return(r3)

total = 10000
df_sim=simulacao(atual,rodadas,0)
for n in range(1,total):
    #df_sim = pd.concat(df_sim,simulacao(atual,rodadas,n), axis=0)
    df_sim = df_sim.append(simulacao(atual,rodadas,n))

df_sim
df_sim=df_sim.groupby(level='sigla').sum()/total*100
df_sim=df_sim[['sigla','class']]
df_sim=df_sim.sort_values(by='class', ascending=False)
df_sim

df_sim.to_csv(os.path.join(DATA_DIR,'resultado.csv'))