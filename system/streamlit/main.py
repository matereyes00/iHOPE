import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import optimal
# import recommend

html_file_path = "./qgis2web_2024_05_29-11_00_56_078368/index.html"
# gpkg_path = "../../CandidateSites/rg1-hex-grid.gpkg"
gpkg_path = "../../CandidateSites/rg1_hexgrid.geojson"
hexagons = gpd.read_file(gpkg_path)
print(hexagons)

st.title("I-HOPE")
df = pd.read_csv('health_facilities_with_coordinates.csv')
selected_columns = ['Facility Name', 'Region Name', 'Latitude', 'Longitude']
df = df[selected_columns]
df = df.rename(columns={'Latitude': 'LAT', 'Longitude': 'LON'})
df = df.dropna()

st.write("## System Description")
text = "iHOPE is a hybrid optimization and prioritization system that looks for new locations to put up rural health units in the Philippines."
st.write(text)
st.write("## System Components:")
# Display the DataFrame
st.write("### Existing RHUs:")
st.write(df)
st.map(df)

# Define the list of regions
regions = [
    "Region I", "CAR", "Region II", "Region III", "Region IV-A", 
    "Region IV-B", "Region V", "Region VI", 
    "Region VII", "Region VIII", "Region IX", "Region X", 
    "Region XI", "Region XII", "Region XIII", "BARMM", "NCR"
]
selected_region = st.selectbox("Select a Region", regions)
st.write(f"You selected: {selected_region}")
st.write("## Display Candidate Sites")
if selected_region == "Region I":
    cs_df = pd.read_csv('../../CandidateSites/rg1_candidate_sites.csv')
    cs_df['ID'] = cs_df['ID'].astype(int)
    st.write(cs_df)
    # st.write(hexagons)

st.write("## Display Optimal Sites")
num_optimal_sites = int(st.text_input("How many optimal sites would you want?", 1))
st.write("You entered:", num_optimal_sites)
if selected_region == "Region I":
    raw_rg1_clustered = pd.read_csv("../../CandidateSites/rg1_PCF_data.csv") # for finding optimal locations
    neighbors_df = pd.read_csv('../../CandidateSites/rg1_Neighbors.csv')
    candidate_sites = pd.read_csv("../../CandidateSites/rg1_candidate_sites.csv")
    neighbors_df.rename(columns={'fid': 'ID'}, inplace=True)
    raw_rg1_clustered = raw_rg1_clustered.drop(columns=['Neighbors'])

    selected_facilities_df, hex_with_RHU, og_HCFAI, updated_HCFAI = optimal.optimize(raw_rg1_clustered, candidate_sites, neighbors_df, num_optimal_sites) # 81 for dropping non buildable; 363 for validation)
    selected_facilities = list(selected_facilities_df['ID'])
    st.write(f"Original HCFAI: {og_HCFAI}")
    st.write(f"Updated HCFAI: {updated_HCFAI}")
    st.write(selected_facilities_df[['ID', 'RHU_Presence', 'HCFAI']])
    st.write("""<div style="width:100%;text-align:center;"><a href="https://matereyes00.github.io/iHOPE/rg1_map/"</a>Region 1</div>""", unsafe_allow_html=True)

st.write("## Display Prioritized Sites")
num_prioritized_sites = st.text_input("How many RHUs do you want to put up?", "")
st.write("You entered:", num_prioritized_sites)
