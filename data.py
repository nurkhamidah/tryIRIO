import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pyreadr as pr

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
            data = (df_eksim[df_eksim['nama_prov_eks'] == 'Aceh']
                    .sort_values(by=['kode_prov_eks', 'nama_prov_eks', 
                           'kode_prov_imp', 'nama_prov_imp',
                           'kode_ind_eks', 'nama_ind_eks',
                           'penggunaan']))
            data_imp = (df_eksim[df_eksim['nama_prov_imp'] == 'Aceh']
                        .sort_values(by=['kode_prov_imp', 'nama_prov_imp', 
                             'kode_prov_eks', 'nama_prov_eks',
                             'kode_ind_eks', 'nama_ind_eks',
                             'penggunaan']))
            data['nilai_mil'] = data['nilai_mil'].values - data['nilai_mil'].values
    else:
        data = df_eksim[df_eksim['nama_ind_eks']==crit2]
    return data
            
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
    fig.update_layout(autosize=False,
                        margin = dict(
                                l=0,
                                r=0,
                                b=0,
                                t=0,
                                pad=4,
                                autoexpand=True
                            ),
                            width=800,
                            )
    fig.update_geos(fitbounds="locations", visible=False)
    return(fig)

## Func Get DF Eksim
def makeTableEksImp(crit, crit2, jenis):
    if crit == 'Ekspor antar Provinsi':
    # PROV - Ekspor Antar Provinsi
        df = (df_eksim[df_eksim['nama_prov_eks'] == crit2]
              .groupby('nama_prov_imp', as_index=False)
              .agg(nilai_mil=('nilai_mil', 'sum'))
              .assign(kode_prov=lambda x: x['nama_prov_imp']))

    # PROV - Impor Antar Provinsi
    else:
        df = (df_eksim[df_eksim['nama_prov_imp'] == crit2]
              .groupby('nama_prov_eks', as_index=False)
              .agg(nilai_mil=('nilai_mil', 'sum'))
              .assign(kode_prov=lambda x: x['nama_prov_eks']))
    return df

# PROV - Net Ekspor
nilai = (df_eksim[df_eksim['nama_prov_eks'] == 'Aceh']
         .groupby('nama_prov_imp', as_index=False)
         .agg(nilai_mil=('nilai_mil', 'sum'))
         .assign(kode_prov=lambda x: x['nama_prov_imp']))

# Second part: filtering, grouping, and summarising
nilai_im = (df_eksim[df_eksim['nama_prov_imp'] == 'Aceh']
            .groupby('nama_prov_eks', as_index=False)
            .agg(nilai_mil=('nilai_mil', 'sum'))
            .assign(kode_prov=lambda x: x['nama_prov_eks']))

# Assuming 'nilai' and 'nilai_im' have the same 'kode_prov' values and are sorted in the same order
nilai['nilai_mil'] = nilai['nilai_mil'] - nilai_im['nilai_mil']