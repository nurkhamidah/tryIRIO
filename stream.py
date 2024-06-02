import streamlit as st
from data import *
from src.agstyler import PINLEFT, PRECISION_TWO
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext
# from llama_index.llms import openai
from llama_index.llms.openai import OpenAI
from streamlit_navigation_bar import st_navbar
from src.agstyler import *

st.set_page_config(
    page_title="BI Hackathon Prototype",
    page_icon="💸",
    layout='wide',
)

## ------------------------------ NAVBAR ------------------------------

page = st_navbar(["Home", "Tentang", "Ekspor-Impor", "PDRB", "Linkage", "Simulasi Pengganda", "Chat"])

## ------------------------------ Home ------------------------------
if page == "Home":
    st.write("Ini lagi di ", page)
    
## ------------------------ç------ About ------------------------------
if page == "Tentang":
    st.write("Ini lagi di ", page)
    
## ------------------------------ Eks-Imp ------------------------------
if page == "Ekspor-Impor":
    st.write("Ini lagi di ", page)
    eks0a, eks_col1a, eks_col1b, eks0b, eks_col1c = st.columns([2,2,3,1,3])
    with eks_col1a:
        eks_fil1 = st.radio('**Pilih Kriteria**', ['Industri', 'Provinsi'])
    with eks_col1b :
        if eks_fil1 == 'Industri':
            eks_fil2 = st.selectbox('**Pilih Industri:**', opt_eksim_ind)
        else :
            eks_fil2 = st.selectbox('**Pilih Provinsi:**', opt_provinsi)
    with eks_col1c:
        eks_fil3 = st.radio('**Pilih Jenis Transaksi:**', ["Ekspor antar Provinsi", "Impor antar Provinsi", "Net Ekspor"])
    data_eks = filterTableEksim(crit=eks_fil1, crit2=eks_fil2, jenis=eks_fil3)
    with st.expander('**Tabel Ekspor Impor**', expanded=True):
        st.dataframe(data_eks, use_container_width=True, height=600)
    
    dat3 = makeTableEksImp(crit=eks_fil1, crit2=eks_fil2, jenis=eks_fil3)
    fig3 = plotSpatial(dat3)
    eks_col2a, eks_col2b = st.columns([1,4])
    with eks_col2b:
        if eks_fil3 == "Impor antar Provinsi":
            st.markdown('<div style="text-align:center"><b>{} dari {} {} menurut Provinsi Asal (Miliar Rupiah)</b></div>'.format(eks_fil3, eks_fil1, eks_fil2), 
                        unsafe_allow_html=True)
        else:
            st.write('<div style="text-align:center"><b>{} dari {} {} menurut Provinsi Tujuan (Miliar Rupiah)</b></div>'.format(eks_fil3, eks_fil1, eks_fil2),
                    unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)
    with eks_col2a:
        '**PERDAGANGAN ANTAR PROVINSI**'
        nil_eks = get_total_eksim(crit = eks_fil1, crit2 = eks_fil2, data_eksim=df_eksim)[0]['nilai_mil']
        nil_imp = get_total_eksim(crit = eks_fil1, crit2 = eks_fil2, data_eksim=df_eksim)[1]['nilai_mil']
        st.metric('**Nilai Ekspor:**', 'Rp {} Miliar'.format(nil_eks.round(2)))
        st.metric('**Nilai Impor:**', 'Rp {} Miliar'.format(nil_imp.round(2)))
        if nil_imp > nil_eks:
            st.metric('**Defisit:**', 'Rp {} Miliar'.format((nil_imp - nil_eks).round(2)))
        else:
            st.metric('**Surplus:**', 'Rp {} Miliar'.format((nil_eks - nil_imp).round(2)))
            
    eks_col3a, eks_col3b = st.columns([1,1])
    eks_col4a, eks_col4b, eks_col4c = st.columns([1,1,1])
    df_4a = makeTableEksImp(crit = eks_fil1, crit2 = eks_fil2, jenis=eks_fil3).sort_values(['nilai_mil'], ascending = False)
    with eks_col4b:
        eks_slid = st.slider('**Masukkan Banyak Provinsi yang Ditampilkan**', 1, len(df_4a))
    with eks_col3a:
        fig4a = makeBarChart(df_4a.head(eks_slid), colx = 'kode_prov', coly = 'nilai_mil')
        st.plotly_chart(fig4a, use_container_width = True)
    with eks_col3b:
        df_4b = makeTableEksImp(crit = eks_fil1, crit2 = eks_fil2, jenis=eks_fil3).sort_values(['nilai_mil'], ascending = True)
        fig4b = makeBarChart(df_4b.head(eks_slid), colx = 'kode_prov', coly = 'nilai_mil')
        st.plotly_chart(fig4b, use_container_width = True)
        
## ------------------------------ PDRB ------------------------------
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
        

## ------------------------------ Linkage ------------------------------
if page == "Linkage":
    st.write("Ini lagi di ", page)


    lin_col1a, lin_col1b = st.columns([2,5])
    with lin_col1a:
        lin_prov = st.selectbox('**Pilih Provinsi:**', opt_provinsi)
        st.write('**Industri Unggulan Provinsi {} Berdasarkan Forward-Backward Linkage**'.format(lin_prov))
        lin_df, lin_fig1 = makeScatterPlotFLBL(df_flbl, lin_prov)
        unggulan_f_id = lin_df['nama_ind'][lin_df['n_forward'].idxmax()]
        unggulan_b_id = lin_df['nama_ind'][lin_df['n_backward'].idxmax()]
        st.metric('Forward Linkage', value=unggulan_f_id)
        st.metric('Backward Linkage', value=unggulan_b_id)
        
    with lin_col1b:
        st.plotly_chart(lin_fig1, use_container_width=True)

    lin_col2a, lin_col2b, lin_col2c = st.columns([1,1,1])
    with lin_col2b : 
        lin_slid1 = st.slider('**Masukkan Banyak Industri yang Ingin Ditampilkan:**', 1, len(lin_df))

    lin_col3a, lin_col3b = st.columns([1,1])
    with lin_col3a:
        lin_fig2a = makeBarChart(lin_df.sort_values('n_forward', ascending=False).head(lin_slid1), colx='nama_ind', coly='n_forward')
        st.plotly_chart(lin_fig2a)
    with lin_col3b:
        lin_fig2b = makeBarChart(lin_df.sort_values('n_backward', ascending=False).head(lin_slid1), colx='nama_ind', coly='n_backward')
        st.plotly_chart(lin_fig2b)
    
## ------------------------------ Multiplier ------------------------------
if page == "Simulasi Pengganda":
    st.write("Ini lagi di ", page)
    # AgGrid(base_irio,
    #        gridOptions = GridOptionsBuilder.from_dataframe(base_irio).build())
    
    sim_col1a, sim_col1b, sim_col1c = st.columns([1,1,1])
    with sim_col1a:
        '**Cari Berdasarkan:**'
        sim_opt1 = st.checkbox('Provinsi')
        sim_opt2 = st.checkbox('Industri')
    with sim_col1b:         
        if sim_opt1:
            sim_prov = st.selectbox('**Pilih Provinsi:**', opt_provinsi)
            sim_prov = [sim_prov]
        else:
            sim_prov = opt_provinsi 
        if sim_opt2:
            sim_ind = st.selectbox('**Pilih Industri:**', opt_ind)
            sim_ind = [sim_ind]
        else: 
            sim_ind = opt_ind
    df_sim = base_irio[base_irio['nama_prov'].isin(sim_prov)][base_irio['nama_ind'].isin(sim_ind)]   
    row_number = st.number_input('Number of rows', min_value=0, value=len(df_sim)) 
        
    formatter = {
        'id': ('ID', {**PINLEFT, 'width' : 40}),
        'nama_prov': ('Provinsi', {'width': 80}),
        'nama_ind': ('Industri', {'width': 200}),
        'final_demand': ('Final Demand', {**PRECISION_TWO, 'width': 100}),
        'nilai_jt': ('Nilai (jt)', {**PRECISION_TWO, 'width': 100}),
        'target': ('Target', {'editable': True, 'width':60})
    }

    data = draw_grid(
        df_sim.head(row_number),
        formatter=formatter,
        fit_columns=True,
        selection='multiple',  # or 'single', or None
        use_checkbox='True',  # or False by default
        max_height=500
    )
    data2 = data['data']
    updated_data = data2[(data2['target'] != 0) & (data2['target'].apply(lambda x: isinstance(x, int)))]
    sim_base, sim_sim = simulationIRIO(updated_data)
    
    with sim_col1c:
        sim_col1c_1, sim_col1c_2 = st.columns([1,1])
        with sim_col1c_1:
            st.metric('**Nilai PDRB Awal:**', sim_base)
        with sim_col1c_2:
            st.metric('**Nilai PDRB Akhir:**', sim_sim)
            
## ------------------------------ Chatbots ------------------------------
if page == "Chat":
    st.write("Ini lagi di ", page)
    st.title("Ini Hanya Bot")

## ------------------ RANDOM ANSWER
#     import random
#     import time

#     def response_generator():
#         response = random.choice(
#             [
#                 "Halo, ada yang bisa dibantu?",
#                 "Saya siap membantu Anda",
#                 "Layanan hari ini tutup.",
#             ]
#         )
#         for word in response.split():
#             yield word + " "
#             time.sleep(0.05)

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("What is up?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)
#         with st.chat_message("assistant"):
#             response = st.write_stream(response_generator())
#         st.session_state.messages.append({"role": "assistant", "content": response})

    ## ------------ WITH OPENAI
    # from openai import OpenAI

    # client = OpenAI(api_key = st.secrets['OPENAI_4'])
    
    # if "messages" not in st.session_state.keys(): 
    #     st.session_state.messages = [
    #     {"role": "assistant", "content": "Ask me a question!"}
    #     ]

    # if "openai_model" not in st.session_state:
    #     st.session_state["openai_model"] = "gpt-3.5-turbo"

    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # if prompt := st.chat_input("What is up?"):
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     with st.chat_message("user"):
    #         st.markdown(prompt)

    #     with st.chat_message("assistant"):
    #         stream = client.chat.completions.create(
    #             model=st.session_state["openai_model"],
    #             messages=[
    #                 {"role": m["role"], "content": m["content"]}
    #                 for m in st.session_state.messages
    #             ],
    #             stream=True,
    #         )
    #         response = st.write_stream(stream)
    #     st.session_state.messages.append({"role": "assistant", "content": response})
    
    api_key = OpenAI(api_key = st.secrets['OPENAI_4'])
    @st.cache_resource(show_spinner=False)
    def load_data():
        with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
            reader = SimpleDirectoryReader(input_dir="./corpus", recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            return index

    index = load_data()
    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages: 
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) 