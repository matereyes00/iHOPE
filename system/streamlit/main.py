import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import optimal
import recommend
import path 
import sys
import pickle
from io import StringIO
import requests


st.title("I-HOPE")

# List all files in the current directory
current_directory = os.getcwd()
file_list = os.listdir(current_directory)
existing_rhus_df='https://raw.githubusercontent.com/matereyes00/iHOPE/iHOPE_ver1.0/system/streamlit/health_facilities_with_coordinates.csv'
response = requests.get(existing_rhus_df)
if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text))
    selected_columns = ['Facility Name', 'Region Name', 'Latitude', 'Longitude']
    df = df[selected_columns]
    df = df.rename(columns={'Latitude': 'LAT', 'Longitude': 'LON'})
    df = df.dropna()

    st.write("## System Description")
    text = "iHOPE is a hybrid optimization and prioritization system that looks for new locations to put up rural health units in the Philippines. The user gets to select the region of their choice to select the number of RHUs to put up."
    st.write(text)
    st.write("## System Components:")
    st.write("### Existing RHUs:")
    st.write(df)
    st.map(df)
else:
    st.error("Failed to load data from GitHub.")


regions = [
    "Region I", "CAR", "Region II", "Region III", "Region IV-A", 
    "Region IV-B", "Region V", "Region VI", 
    "Region VII", "Region VIII", "Region IX", "Region X", 
    "Region XI", "Region XII", "Region XIII", "BARMM", "NCR"
]
selected_region = st.selectbox("Select a Region", regions)
st.write(f"You selected: {selected_region}")
st.write("## Display Candidate Sites")
st.write("Select a region to see where you want to put up rural health units")
if selected_region == "Region I":
    # execute BPNN application here
    # call model
    candidate_sites_df='https://raw.githubusercontent.com/matereyes00/iHOPE/iHOPE_ver1.0/system/streamlit/rg1candidate_sites.csv'
    candidate_sites_df_response = requests.get(candidate_sites_df)
    if candidate_sites_df_response.status_code == 200:
        cs_df = pd.read_csv(StringIO(candidate_sites_df_response.text))
        st.write(f"#### {len(cs_df['ID'])} Candidate Sites")
        cs_df['ID'] = cs_df['ID'].astype(int)
        st.write(cs_df)

st.write("## Display Optimal Sites")
st.write("Please input a number to begin the optimization process. You can only put a number less than or equal to the number of candidate sites specified above")
num_optimal_sites = int(st.text_input("How many optimal sites would you want?", 1))
st.write("You entered:", num_optimal_sites)
if selected_region == "Region I":
    PCF_df= 'https://raw.githubusercontent.com/matereyes00/iHOPE/iHOPE_ver1.0/system/streamlit/rg1_PCF.csv'
    NEIGHBOURS_df= 'https://raw.githubusercontent.com/matereyes00/iHOPE/iHOPE_ver1.0/system/streamlit/rg1_Neighbors.csv'
    CS_df='https://raw.githubusercontent.com/matereyes00/iHOPE/iHOPE_ver1.0/system/streamlit/rg1candidate_sites.csv'

    PCF_response=requests.get(PCF_df)
    NEIGHBOURS_response=requests.get(NEIGHBOURS_df)
    CS_response=requests.get(CS_df)

    if PCF_response.status_code == 200 and NEIGHBOURS_response.status_code == 200 and CS_response.status_code == 200:
        raw_rg1_clustered = pd.read_csv(StringIO(PCF_response.text)) # for finding optimal locations
        neighbors_df = pd.read_csv(StringIO(NEIGHBOURS_response.text))
        candidate_sites = pd.read_csv(StringIO(CS_response.text))
        neighbors_df.rename(columns={'fid': 'ID'}, inplace=True)
        # raw_rg1_clustered = rg1_clustered_df
        raw_rg1_clustered = raw_rg1_clustered.drop(columns=['Neighbors'])
        # selected_facilities_df, hex_with_RHU, og_HCFAI, updated_HCFAI = optimal.optimize(raw_rg1_clustered, candidate_sites, neighbors_df, num_optimal_sites) 
        selected_facilities_df, hex_with_RHU, og_HCFAI, updated_HCFAI = optimal.optimize(raw_rg1_clustered, candidate_sites, neighbors_df, num_optimal_sites)
        selected_facilities = list(set(selected_facilities_df['ID']))
        st.write(f"Original HCFAI: {og_HCFAI}")
        st.write(f"Updated HCFAI: {updated_HCFAI}")
        st.write(selected_facilities_df[['ID', 'RHU_Presence', 'HCFAI']])
        st.write("""<div style="width:100%;text-align:center;"><a href="https://matereyes00.github.io/iHOPE/rg1map/"</a>Region 1</div>""", unsafe_allow_html=True)

        st.write("## Cities needing RHUs: ")
        st.write("Based on the number of optimal sites you specified above, this section automatically generates the number of RHUs needed in the cities")
        os = list(set(selected_facilities_df['ID']))

        rg1_clusters_df = "https://raw.githubusercontent.com/matereyes00/iHOPE/iHOPE_ver1.0/system/streamlit/rg1-clusters.csv"
        rg1_clusters_df_response=requests.get(rg1_clusters_df)
        if rg1_clusters_df_response.status_code == 200:
            rg1_clustered_df = pd.read_csv(StringIO(rg1_clusters_df_response.text))
            os_df, rhus_per_city = optimal.MCLP(os, rg1_clustered_df)
            for key, value in rhus_per_city.items():
                if value:
                    st.write(f"{key}: {value}")
            st.write("## Display Prioritized Sites")
            st.write("Based on the number of optimal sites you specified above, this section automatically generates the areas that need RHUs, denoted by a hexagon ID.")
            recommend.recommend(os_df, rhus_per_city)