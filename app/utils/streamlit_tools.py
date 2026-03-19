import pandas as pd
import streamlit as st
import os
from huggingface_hub import hf_hub_download

HF_REPO_ID = "Rayane-K/Variants-Genomiques"
HF_FILENAME = "pathogenic_variants.parquet"
DATA_PATH = f"/tmp/{HF_FILENAME}" # /tmp is writable in Streamlit Cloud
# DATA_PATH = "data/pathogenic_variants.parquet"

@st.cache_data(show_spinner=False)  # Put in cache to avoid reloading
def load_data():
    # print(f"Current path: {os.getcwd()}")
    # Since Streamlit cannot directly read from LST data in git repo, we download from Hugging Face
    if not os.path.exists(DATA_PATH) or os.path.getsize(DATA_PATH) < 100000:
        os.makedirs("data", exist_ok=True)
        hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=HF_FILENAME,
            repo_type="dataset",
            #local_dir="data"
            local_dir="/tmp"
        )

    cols = ["GENEINFO", "CHROM", "POS", "REF", "ALT", "CLNSIG", "CLNVC", "CLNDN"]
    df = pd.read_parquet(DATA_PATH, columns=cols)

    # Extract the gene name GENEINFO > "OR4F5:79501" > "OR4F5"
    df['GENE'] = df['GENEINFO'].str.split(':').str[0]

    # Cleaning
    df['CHROM'] = df['CHROM'].astype(str)
    df['GENE']  = df['GENE'].fillna('Unknown')
    df['CLNSIG'] = df['CLNSIG'].fillna('Unknown')
    df['CLNVC']  = df['CLNVC'].fillna('Unknown')
    df['CLNDN']  = df['CLNDN'].fillna('Unknown')
   
    return df