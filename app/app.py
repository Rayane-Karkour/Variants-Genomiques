import streamlit as st

st.title("Variant Genomics")

query = st.text_input("Entrez le genome chercher:")

if query:
    st.write(f"Vous avez cherchez: {query}")