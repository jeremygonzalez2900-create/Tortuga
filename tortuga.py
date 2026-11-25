import streamlit as st
st.markdown("# Porcentajes")
a = st.input_number ("Valores", min_value= 1, max_value = 100000, value= 1, step= 1)
