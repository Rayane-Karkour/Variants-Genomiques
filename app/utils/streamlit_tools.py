import pandas as pd
import streamlit as st
import os

DATA_PATH = "data/pathogenic_variants.parquet"

@st.cache_data  # Put in cache to avoid reloading
def load_data():
    # print(f"Current path: {os.getcwd()}")
    st.write("Working dir:", os.getcwd())
    st.write("Absolute path:", os.path.abspath(DATA_PATH))
    if not os.path.exists(DATA_PATH):
        st.error(f"Fichier introuvable: {DATA_PATH}.")
        st.stop()

    df = pd.read_parquet(DATA_PATH)

    # Extract the gene name GENEINFO > "OR4F5:79501" > "OR4F5"
    df['GENE'] = df['GENEINFO'].str.split(':').str[0]

    # Cleaning
    df['CHROM'] = df['CHROM'].astype(str)
    df['GENE']  = df['GENE'].fillna('Unknown')
    df['CLNSIG'] = df['CLNSIG'].fillna('Unknown')
    df['CLNVC']  = df['CLNVC'].fillna('Unknown')
    df['CLNDN']  = df['CLNDN'].fillna('Unknown')
   
    return df