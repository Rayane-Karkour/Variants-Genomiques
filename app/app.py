import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.streamlit_tools import load_data


##### Config #####
st.set_page_config(
    page_title="Explorateur de Variants Génomiques",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="logo.png"
)

df = load_data()

##### Sidebar #####
with st.sidebar:
    st.title("Explorateur de Variants")
    st.caption("Source : ClinVar / NCBI")
    st.markdown(f"**{len(df):,}** variants chargés")
    st.markdown("""
    ## À propos de l'application :
    Cette app vous permet de visualiser et filtrer des variants génomiques pathogènes du [génome humain GRCh37](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/) issus de [ClinVar (NCBI)](https://www.ncbi.nlm.nih.gov/clinvar/), 
    d'explorer les gènes, leurs maladies associées et de télécharger des extraits de données pour vos analyses.  
    
    ## Contexte :
    Bonjour et bienvenue sur mon explorateur de variants génomiques !  

    J'ai créé cette application pour me familiariser avec la bioinformatique. 
    Ça m'a permis de mieux comprendre quelles connaissances en biologie me seraient utiles.  

    Je ne vais pas le cacher : j'étais un peu dépassé au début, mais dans l'ensemble, c'était une très bonne expérience. 
    Il y a encore pas mal de choses à améliorer, surtout au niveau du nettoyage des données, 
    mais j'ai vraiment pris plaisir à explorer les variants.  

    Je prévois, quand j'aurai un peu plus de temps, de continuer à améliorer l'application et voir ce que je peux en tirer.
    
    ## Technologies utilisées :
    - Python
    - Streamlit
    - Pandas
    - Plotly
                
    """)

##### Body #####
st.title("Explorateur de Variants Génomiques")
st.markdown("Analyse des variants pathogènes issus de **ClinVar (NCBI)**")

st.divider()
##### Metrics 1 : Dataset General #####
col1, col2, col3 = st.columns(3)
col1.metric("Variants pathogènes", f"{len(df):,}")
col2.metric("Gènes uniques",       f"{df['GENE'].nunique():,}")
col3.metric("Types de variants",   f"{df['CLNVC'].nunique()}")


st.divider()
##### Visualisation : Bar graph & pie generale #####
col_left, col_right = st.columns(2)

##### Bar #####
with col_left:
    counts = df['CHROM'].value_counts().sort_index()
    fig_chrom = go.Figure(go.Bar(
        x=counts.index,
        y=counts.values,
    ))
    fig_chrom.update_layout(title="Distribution des variants par chromosome")
    st.plotly_chart(fig_chrom)

##### Pie #####
with col_right:
    clnsig_counts = df['CLNSIG'].value_counts().head(6)
    fig_pie = px.pie(
        values=clnsig_counts.values,
        names=clnsig_counts.index,
        hole=0.4,
        title="Signification clinique des variants"
    )
    st.plotly_chart(fig_pie)


##### Last info : Top Gene #####
st.subheader("Gènes par nombre de variants pathogènes (20 premiers)")

top_genes = df['GENE'].value_counts().head(20)
fig_genes = px.bar(
    top_genes.sort_values(),
    x=top_genes.values,
    y=top_genes.index,
    orientation='h',
)
st.plotly_chart(fig_genes)


st.divider()
##### Filtre & Table #####
col_g, col_t = st.columns(2)

##### Filtre #####
with col_g:
    st.header("Filtres")
    CHROM_ORDER = [str(i) for i in range(1, 23)] + ['X', 'Y']
    available_chroms = [c for c in CHROM_ORDER if c in df['CHROM'].values]

    selected_chroms = st.multiselect(
        "Chromosomes",
        options=available_chroms,
        default=available_chroms,
    )

    selected_clnsig = st.multiselect(
        "Signification clinique",
        options=df['CLNSIG'].unique(),
        default=df['CLNSIG'].unique(),
    )

    selected_vc = st.multiselect(
        "Type de variant",
        options=df['CLNVC'].unique(),
        default=[f for f in df['CLNVC'].unique().tolist() if f != 'single_nucleotide_variant']
    )
    st.caption("Par défaut, les variants de type 'single_nucleotide_variant' sont exclus pour mieux visualiser les autres types de variants.")

    mask = (
        df['CHROM'].isin(selected_chroms) &
        df['CLNSIG'].isin(selected_clnsig) &
        df['CLNVC'].isin(selected_vc)
    )
    df_filtered = df[mask]

##### Pie 2 : Variants x Signification #####
with col_t:
    st.subheader("Types de variants (sélection)")
    fig_pie2 = px.pie(
        df_filtered['CLNVC'].value_counts().reset_index(),
        names="CLNVC", values='count', hole=0.4,
    )
    st.plotly_chart(fig_pie2)

st.divider()
##### Export Dataset #####

cols_display = ['CHROM', 'POS', 'REF', 'ALT', 'GENE', 'CLNSIG', 'CLNVC', 'CLNDN']
cols_ok = [c for c in cols_display if c in df_filtered.columns]

df_sample = df_filtered.sample(n=min(10000, len(df_filtered)))
st.subheader(f"Variants : {len(df_sample):,} affichés sur {len(df_filtered):,} filtrés")

st.dataframe(
    df_sample[cols_ok],
    use_container_width=True,
    height=400,
    hide_index=True
)

csv_data = df_sample[cols_ok].to_csv(index=False) # cols_ok reutilisé de la ligne 125

st.download_button(
    label="Télécharger CSV",
    data=csv_data,
    file_name="sample_10k.csv",
    mime="text/csv",
)

all_genes = sorted(df['GENE'].dropna().unique().tolist())

st.divider()
##### Recherche par gène #####

st.title("Recherche par Gène")
st.markdown("Explorez tous les variants pathogènes d'un gène spécifique.")
selected_gene = st.selectbox(
    "Rechercher un gène (ex : TTN, BRCA1, ATM, NF1...)",
    options=[""] + all_genes,
)


if not selected_gene:
    st.info("Sélectionnez un gène pour afficher les détails.")
else:
    df_gene = df[df['GENE'] == selected_gene].copy()

    chrom   = df_gene['CHROM'].mode()[0]
    gene_id = df_gene['GENEINFO'].iloc[0].replace('|', ':').split(':')[1]
    ncbi_url = f"https://www.ncbi.nlm.nih.gov/gene/{gene_id}"

    st.divider()
    #### Metrics & header #####
    st.title(f"Gène sélectionné : **{selected_gene}**")

    st.markdown(f"Chromosome : {chrom} | [{selected_gene} sur NCBI]({ncbi_url})")

    #### Metrics #####
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total variants", len(df_gene), help="Nombre total de variants pathogènes référencés pour ce gène.")
    k2.metric("Types distincts", df_gene['CLNVC'].nunique(),help="Nombre de types de variants différents (ex : délétion, insertion...)")
    k3.metric("Maladies associées", df_gene['CLNDN'].nunique(), help="Nombre de maladies différentes associées à ce gène.")
    k4.metric("Significations", df_gene['CLNSIG'].nunique(), help="Nombre de significations cliniques différentes (ex : Pathogenic, Likely pathogenic...)")


    st.divider()
    #### Diseases table #####

    st.subheader("Maladies associées (10 premières)")
    diseases = (
        df_gene['CLNDN']
        .str.replace('_', ' ')
        .value_counts().head(10)
        .reset_index()
    )
    diseases.columns = ['Maladie', 'Variants']
    st.dataframe(diseases, use_container_width=True, hide_index=True, height=300)

    st.divider()
    #### Variants table & export #####
    st.subheader("Variants pathogènes du gène sélectionné")
    st.dataframe(df_gene[cols_ok], use_container_width=True, hide_index=True) # cols_ok reutilisé de la ligne 125

    csv = df_gene[cols_ok].to_csv(index=False).encode('utf-8') 
    st.download_button(
        f"Télécharger CSV",
        data=csv,
        file_name=f"variants_{selected_gene}.csv",
        mime="text/csv",
    )