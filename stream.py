import streamlit as st
from data import *
# from temp import *
from streamlit_navigation_bar import st_navbar

st.set_page_config(
    page_title="BI Hackathon Prototype",
    page_icon="💸",
    layout='wide',
)

## ------------------------------ NAVBAR ------------------------------

page = st_navbar(["Home", "Tentang", "Ekspor-Impor", "PDRB", "Linkage", "Simulasi Pengganda"])

## ------------------------------ HOME ------------------------------
if page == "Home":
    st.write("Ini lagi di ", page)
    
## ------------------------------ SNAPSHOT ------------------------------
if page == "Tentang":
    st.write("Ini lagi di ", page)
    
## ------------------------------ USE ------------------------------
if page == "Ekspor-Impor":
    st.write("Ini lagi di ", page)
    

## ------------------------------ SUPPLY ------------------------------
if page == "PDRB":
    st.write("Ini lagi di ", page)
    st.dataframe(df_pdrb, use_container_width=True)
    opt_skala = st.toggle("Skala Provinsi")
    if opt_skala:
        pd_col1a, pd_col1b = st.columns([3,7])
        with pd_col1a:
            with st.container(border=True):
                jenis_pdrb = st.radio(label='**Pilih jenis PDRB :**', 
                                    options=['PRODUKSI', 'PENDAPATAN', 'PENGELUARAN'])

                    
            with st.container(border=True):
                if jenis_pdrb == 'PRODUKSI':
                    opt_sektor = opt_sektor_prod
                elif jenis_pdrb == 'PENDAPATAN':
                    opt_sektor = opt_sektor_pend
                else:
                    opt_sektor = opt_sektor_peng
                if st.checkbox('Semua Sektor'):
                    sektor = st.multiselect('**Pilih Sektor**',
                                                                opt_sektor,
                                                                disabled=True)
                    sektor =  opt_sektor.tolist()
                else:
                    sektor =  st.multiselect('**Pilih Sektor**',
                                                                opt_sektor)
                    
            with st.container(border=True):
                if st.checkbox('Semua Provinsi'):
                    provinsi = st.multiselect('**Pilih Provinsi**',
                                                                opt_provinsi,
                                                                disabled=True)
                    provinsi =  opt_provinsi.tolist()
                else:
                    provinsi =  st.multiselect('**Pilih Provinsi**',
                                                                opt_provinsi)
        with pd_col1b:   
            dat1, fig1 = plotBerdasarkanJenisPDRB(jenis_pdrb, provinsi, sektor)
            # data1 = df_pdrb[df_pdrb['jenis_pdrb'] == jenis_pdrb][df_pdrb['nama_prov'].isin(provinsi)][df_pdrb['nama_komp'].isin(sektor)]
            st.dataframe(dat1[['nama_prov', 'jenis_pdrb', 'nama_komp', 'nilai_jt']], use_container_width=True)
            
        pd_col2a, pd_col2b = st.columns([3,7])
        with pd_col2b:
            st.plotly_chart(fig1, use_container_width=True)
        
    else:
        pd_col3a, pd_col3b = st.columns([3,7])
        with pd_col3a:
            with st.container(border=True):
                jenis_pdrb = st.radio(label='**Pilih jenis PDRB :**', 
                                    options=['PRODUKSI', 'PENDAPATAN', 'PENGELUARAN'])
       
            with st.container(border=True):
                if jenis_pdrb == 'PRODUKSI':
                    opt_sektor = opt_sektor_prod
                elif jenis_pdrb == 'PENDAPATAN':
                    opt_sektor = opt_sektor_pend
                else:
                    opt_sektor = opt_sektor_peng
                if st.checkbox('Semua Sektor'):
                    sektor = st.multiselect('**Pilih Sektor**',
                                                                opt_sektor,
                                                                disabled=True)
                    sektor =  opt_sektor.tolist()
                    
                else:
                    sektor =  st.multiselect('**Pilih Sektor**',
                                                                opt_sektor)
               
                max_slider = len(df_pdrb_nasional[df_pdrb_nasional['jenis_pdrb'] == jenis_pdrb])
                n_sektor = st.slider("**Tentukan banyak sektor:**",
                                        min_value=1, max_value=max_slider)     
                
        with pd_col3b:   
            dat2, fig2 = plotNasionalBerdasarkanJenisPDRB(jenis_pdrb, sektor, n_sektor)
            st.dataframe(dat2[['nama_komp', 'nilai_jt']].sort_values(['nilai_jt'], ascending=False), use_container_width=True)
        pd_col4a, pd_col4b = st.columns([3,7])
        with pd_col4a:
            sum_pdrb = dat2['nilai_jt'].head(n_sektor).sum()
            st.metric("**Total PDRB:**", value = sum_pdrb.round(3))
        with pd_col4b:
            st.plotly_chart(fig2, use_container_width=True)
        

## ------------------------------ INDUSTRY ------------------------------
if page == "Linkage":
    st.write("Ini lagi di ", page)
    
## ------------------------------ I/O ------------------------------
if page == "Simulasi Pengganda":
    st.write("Ini lagi di ", page)
