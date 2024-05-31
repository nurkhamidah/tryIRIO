import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pyreadr as pr
from st_aggrid import AgGrid, GridOptionsBuilder

## PDRB

df_pdrb = pd.read_csv("data/data_pdrb.csv", sep = ",")
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


## LOC
import requests
geojson = requests.get(
    #"https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"
    #"https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson"
    #"https://raw.githubusercontent.com/Vizzuality/growasia_calculator/master/public/indonesia.geojson"
    "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson"
).json()

d_find_and_replace = {'Bangka-Belitung' : 'Kep. Bangka Belitung', 
                      'Kepulauan Riau' : 'Kep. Riau', 
                      'Jakarta Raya' : 'DKI Jakarta',
                      'Yogyakarta' : 'DI Yogyakarta'}

for i in range(0, 34):
    for bef in d_find_and_replace.keys():
        if geojson['features'][i]['properties']['state'] == bef:
            geojson['features'][i]['properties']['state'] = d_find_and_replace[bef]

df = pd.DataFrame(
    {"Column": pd.json_normalize(geojson["features"])["properties.state"]}
).assign(Columnnext=lambda d: d["Column"].str.len())
            
def plotSpatial(dat):
    df2 = df.merge(dat, left_on='Column', right_on='kode_prov')
    fig = go.Figure(
        data=go.Choropleth(
            geojson=geojson,
            locations=df["Column"], 
            featureidkey="properties.state",
            z=df2['nilai_mil'],
            colorscale="Reds",
            colorbar_title="Column"))
    fig.update_layout(autosize=True,
                        margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                pad=4,
                                autoexpand=True
                            ),
                            width = 1200
                            )
    fig.update_geos(fitbounds="locations", visible=False)
    return(fig)

## EKS-IMP

df_eksim = pr.read_r('data/data_eksim_ap.rds')[None]
opt_eksim_ind = df_eksim['nama_ind_eks'].unique()

def filterTableEksim(crit, crit2, jenis):
    if crit == 'Provinsi':
        if jenis == 'Ekspor antar Provinsi':
            data = df_eksim[df_eksim['nama_prov_eks'] == crit2]
        elif jenis == 'Impor antar Provinsi':
            data = df_eksim[df_eksim['nama_prov_imp'] == crit2]
        else :
            data = (df_eksim[df_eksim['nama_prov_eks'] == crit2]
                    .sort_values(by=['kode_prov_eks', 'nama_prov_eks', 
                           'kode_prov_imp', 'nama_prov_imp',
                           'kode_ind_eks', 'nama_ind_eks',
                           'penggunaan']))
            data_imp = (df_eksim[df_eksim['nama_prov_imp'] == crit2]
                        .sort_values(by=['kode_prov_imp', 'nama_prov_imp', 
                             'kode_prov_eks', 'nama_prov_eks',
                             'kode_ind_eks', 'nama_ind_eks',
                             'penggunaan']))
            data['nilai_mil'] = data['nilai_mil'].values - data['nilai_mil'].values
    else:
        data = df_eksim[df_eksim['nama_ind_eks'] == crit2]
    return data
            
def makeTableEksImp(crit, crit2, jenis):
    if crit == 'Provinsi':
        if jenis == 'Ekspor antar Provinsi':
        # PROV - Ekspor antar Provinsi
            df = (df_eksim[df_eksim['nama_prov_eks'] == crit2]
                .groupby('nama_prov_imp', as_index=False)
                .agg(nilai_mil=('nilai_mil', 'sum'))
                .assign(kode_prov=lambda x: x['nama_prov_imp']))
        # PROV - Impor antar Provinsi
        elif jenis == 'Impor antar Provinsi':
            df = (df_eksim[df_eksim['nama_prov_imp'] == crit2]
                .groupby('nama_prov_eks', as_index=False)
                .agg(nilai_mil=('nilai_mil', 'sum'))
                .assign(kode_prov=lambda x: x['nama_prov_eks']))
        # PROV - Net Ekspor
        else:
            df = (df_eksim[df_eksim['nama_prov_eks'] == crit2]
                .groupby('nama_prov_imp', as_index=False)
                .agg(nilai_mil=('nilai_mil', 'sum'))
                .assign(kode_prov=lambda x: x['nama_prov_imp']))
            df_im = (df_eksim[df_eksim['nama_prov_imp'] == crit2]
                .groupby('nama_prov_eks', as_index=False)
                .agg(nilai_mil=('nilai_mil', 'sum'))
                .assign(kode_prov=lambda x: x['nama_prov_eks']))
            df['nilai_mil'] = df['nilai_mil'] - df_im['nilai_mil']
    else:
        if jenis == "Ekspor antar Provinsi":
            df = (df_eksim[df_eksim['nama_ind_eks'] == crit2]
                .groupby('nama_prov_eks', as_index=False)
                .agg(nilai_mil=('nilai_mil', 'sum'))
                .assign(kode_prov=lambda x: x['nama_prov_eks']))
        elif jenis == "Impor antar Provinsi":
            df = (df_eksim[df_eksim['nama_ind_eks'] == crit2]
                .groupby('nama_prov_imp', as_index=False)
                .agg(nilai_mil=('nilai_mil', 'sum'))
                .assign(kode_prov=lambda x: x['nama_prov_imp']))
        else:
            df = (df_eksim[df_eksim['nama_ind_eks'] == crit2]
                .groupby('nama_prov_eks', as_index=False)
                .agg(nilai_mil=('nilai_mil', 'sum'))
                .assign(kode_prov=lambda x: x['nama_prov_eks']))
            df_im = (df_eksim[df_eksim['nama_ind_eks'] == crit2]
                    .groupby('nama_prov_imp', as_index=False)
                    .agg(nilai_mil=('nilai_mil', 'sum'))
                    .assign(kode_prov=lambda x: x['nama_prov_imp']))
            df['nilai_mil'] = df['nilai_mil'] - df_im['nilai_mil']
    return df

def get_total_eksim(crit, crit2, data_eksim):
    if crit == "Provinsi":
        tot_eks = (data_eksim[data_eksim['nama_prov_eks'] == crit2]
                   .agg(nilai_mil=('nilai_mil', 'sum')))
        
        tot_imp = (data_eksim[data_eksim['nama_prov_imp'] == crit2]
                   .agg(nilai_mil=('nilai_mil', 'sum')))
    else:
        tot_eks = (data_eksim[data_eksim['nama_ind_eks'] == crit2]
                   .agg(nilai_mil=('nilai_mil', 'sum')))
        
        tot_imp = tot_eks
    
    return tot_eks['nilai_mil'], tot_imp['nilai_mil']

def makeBarChart(df, colx, coly):
    fig = px.bar(df, x=colx, y=coly, color=colx, height=400)
    return fig

## FL-BL 
df_flbl = pr.read_r('data/flbl_detail.rds')[None]

def makeScatterPlotFLBL(df, prov):
    data = df[df['nama_prov'] == prov]
    fig = px.scatter(data, x='n_forward', y='n_backward',
                 title='Grafik Forward-Backward Linkage Provinsi {}'.format(prov),
                 labels={'n_forward': 'Forward', 'n_backward': 'Backward'},
                 template='simple_white', custom_data=['nama_ind'])
    fig.update_traces(marker=dict(size=13,
                                color='LightSkyBlue',
                                line=dict(width=2,
                                            color='DarkSlateGrey')),
                    hovertemplate="<br>".join([
                        "Forward: %{x}",
                        "Backward: %{y}",
                        "%{customdata[0]}"]))
    fig.add_hline(y=1, line_width=2, opacity=0.8)
    fig.add_vline(x=1, line_width=2, opacity=0.8)
    fig.update_layout(yaxis=dict(showline=False),
                    xaxis=dict(showline=False))
    return(data, fig)

## SIMULASI
leontif = pr.read_r("data/leontif.rds")[None]
base_irio = pr.read_r("data/sim_irio.rds")[None]
out_irio = pr.read_r("data/out_irio.rds")[None]