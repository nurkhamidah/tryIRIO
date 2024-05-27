import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df_pdrb = pd.read_csv("data_pdrb.csv", sep = ",")
df_pdrb_nasional = df_pdrb.groupby(['jenis_pdrb', 'nama_komp']).agg({"nilai_jt": "sum"}).reset_index()
opt_provinsi = df_pdrb['nama_prov'].unique()
opt_sektor_prod = df_pdrb.loc[df_pdrb['jenis_pdrb'].isin(['PRODUKSI'])]['nama_komp'].unique()
opt_sektor_peng = df_pdrb.loc[df_pdrb['jenis_pdrb'].isin(['PENGELUARAN'])]['nama_komp'].unique()
opt_sektor_pend = df_pdrb.loc[df_pdrb['jenis_pdrb'].isin(['PENDAPATAN'])]['nama_komp'].unique()

def plotBerdasarkanJenisPDRB(jenis_pdrb, nama_prov, nama_sektor):
    data = df_pdrb[df_pdrb['jenis_pdrb'] == jenis_pdrb][df_pdrb['nama_prov'].isin(nama_prov)][df_pdrb['nama_komp'].isin(nama_sektor)]
    x = data['nama_prov'].unique()
    fig = go.Figure()
    komps = data['nama_komp'].unique()
    for i in range(len(komps)):
        fig.add_trace(go.Bar(x=x, y=data['nilai_jt'][data['nama_komp'] == komps[i]], name=komps[i]))
    fig.update_layout(barmode='stack')
    return(data, fig)

def plotNasionalBerdasarkanJenisPDRB(jenis_pdrb, nama_sektor, n):
    data = df_pdrb_nasional[df_pdrb_nasional['jenis_pdrb'] == jenis_pdrb][df_pdrb_nasional['nama_komp'].isin(nama_sektor)].sort_values(['nilai_jt'], ascending=False)
    data2 = data.head(n).sort_values(['nilai_jt'], ascending=True)
    x = data2['nama_komp'].unique()
    fig = go.Figure(go.Bar(
            x=data2['nilai_jt'],
            y=x,
            orientation='h'))
    fig.update_layout(barmode='stack')
    return(data, fig)