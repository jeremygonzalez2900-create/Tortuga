import streamlit as st

st.markdown("# Porcentajes")
a = st.number_input("Valores", min_value=1, value=1, step=1)
b = a + (a * 0.10)
st.markdown(f"### El valor del número con un 10 % es: **{b:.2f}**")

