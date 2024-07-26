import streamlit as st
import requests
import pandas as pd

st.set_page_config( layout="wide")
# API endpoints
ontology_from_metabolites_url = "https://rampdb.nih.gov/api/ontologies-from-metabolites"
pathways_from_analytes_url = "https://rampdb.nih.gov/api/pathways-from-analytes"
metabolites_from_ontologies_url = "https://rampdb.nih.gov/api/metabolites-from-ontologies"
analytes_from_pathways_url = "https://rampdb.nih.gov/api/analytes-from-pathways"

# Streamlit app
st.title("RAMPDB Data Explorer")

# Helper function to fetch and display data
def fetch_and_display_data(url, payload, title):
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        st.write(f"### {title}")

        if isinstance(response_data, dict):
            # For cases where the response is a dictionary with a key for data
            if 'data' in response_data:
                data = response_data['data']
            else:
                data = response_data
        elif isinstance(response_data, list):
            # If the response is directly a list of records
            data = response_data
        else:
            st.write("Unexpected response format.")
            return
        
        # Normalize and convert to DataFrame
        try:
            df = pd.json_normalize(data)
            st.dataframe(df, use_container_width=True)  # Display in full width
        except Exception as e:
            st.write(f"Error processing data: {e}")
    else:
        st.write("Failed to fetch data. Please try again.")

# Section for Analytes from Pathways
with st.expander("Fetch Analytes from Pathways", expanded=False):
    pathways_input = st.text_area("Enter pathways (comma-separated)", "De Novo Triacylglycerol Biosynthesis, sphingolipid metabolism")
    analyte_type = st.selectbox("Select Analyte Type", options=["both", "gene", "compound"])
    match = st.selectbox("Select Match Type", options=["exact", "partial"])
    if st.button("Submit Analytes from Pathways"):
        pathways_list = [pathway.strip() for pathway in pathways_input.split(',')]
        payload = {"pathway": pathways_list, "analyte_type": analyte_type, "match": match}
        fetch_and_display_data(analytes_from_pathways_url, payload, "Analytes from Pathways")

# Section for Ontologies from Metabolites
with st.expander("Fetch Ontologies from Metabolites", expanded=False):
    metabolites_input = st.text_area("Enter metabolites (comma-separated)", "ensembl:ENSG00000135679, hmdb:HMDB0000064, hmdb:HMDB0000148, ensembl:ENSG00000141510")
    names_or_ids = st.selectbox("Names or IDs", options=["names", "ids"])
    if st.button("Submit Ontologies from Metabolites"):
        metabolites_list = [met.strip() for met in metabolites_input.split(',')]
        payload = {"metabolite": metabolites_list, "namesOrIds": names_or_ids}
        fetch_and_display_data(ontology_from_metabolites_url, payload, "Ontologies from Metabolites")

# Section for Pathways from Analytes
with st.expander("Fetch Pathways from Analytes", expanded=False):
    analytes_input = st.text_area("Enter analytes (comma-separated)", "ensembl:ENSG00000135679, hmdb:HMDB0000064, hmdb:HMDB0000148, ensembl:ENSG00000141510")
    if st.button("Submit Pathways from Analytes"):
        analytes_list = [analyte.strip() for analyte in analytes_input.split(',')]
        payload = {"analytes": analytes_list}
        fetch_and_display_data(pathways_from_analytes_url, payload, "Pathways from Analytes")

# Section for Metabolites from Ontologies
with st.expander("Fetch Metabolites from Ontologies", expanded=False):
    ontology_input = st.text_area("Enter ontology terms (comma-separated)", "Colon, Liver, Lung")
    format_choice = st.selectbox("Select Format", options=["json", "xml"])
    if st.button("Submit Metabolites from Ontologies"):
        ontology_list = [ont.strip() for ont in ontology_input.split(',')]
        payload = {"ontology": ontology_list, "format": format_choice}
        fetch_and_display_data(metabolites_from_ontologies_url, payload, "Metabolites from Ontologies")

