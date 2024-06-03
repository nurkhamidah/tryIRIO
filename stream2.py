import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc

menu_data = [
    {'id': 'home', 'label':'Home'},
    {'id': 'about', 'label':'About'},
    {'id': 'pdrb', 'label':'PDRB'},
    {'id': 'eksim', 'label':'Ekspor-Impor'},
    {'id': 'flbl', 'label':'Forward-Backward Linkage'},
    {'id': 'simul', 'label':'Simulasi Pengganda'},
    {'id': 'clust', 'label':'Model Segmentasi'},
    {'id': 'chat', 'label':'Chatbot'}    
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=False,
    sticky_nav=True, 
    sticky_mode='pinned', 
)

#get the id of the menu item clicked
st.write(menu_id)