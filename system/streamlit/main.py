import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import optimal
import recommend

html_file_path = "./qgis2web_2024_05_29-11_00_56_078368/index.html"
# gpkg_path = "../../CandidateSites/rg1-hex-grid.gpkg"
gpkg_path = "../../CandidateSites/rg1_hexgrid.geojson"
x = "../../CandidateSites/rg1-clusters.csv"
rg1_clustered_df = pd.read_csv(x)
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
    # execute BPNN application here
    # call model





    cs_df = pd.read_csv('../../CandidateSites/rg1candidate_sites.csv')
    st.write(f"#### {len(cs_df['ID'])} Candidate Sites")
    cs_df['ID'] = cs_df['ID'].astype(int)
    st.write(cs_df)

st.write("## Display Optimal Sites")
num_optimal_sites = int(st.text_input("How many optimal sites would you want?", 1))
st.write("You entered:", num_optimal_sites)
if selected_region == "Region I":
    raw_rg1_clustered = pd.read_csv("../../CandidateSites/rg1_PCF.csv") # for finding optimal locations
    neighbors_df = pd.read_csv('../../CandidateSites/rg1_Neighbors.csv')
    candidate_sites = pd.read_csv("../../CandidateSites/rg1candidate_sites.csv")
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
os = list(set(selected_facilities_df['ID']))
# os_df = optimal.process_population_density(rg1_clustered_df, os)
os_df, rhus_per_city = optimal.MCLP(os, rg1_clustered_df)
# st.write(rhus_per_city)
for key, value in rhus_per_city.items():
    if value:
        st.write(f"{key}: {value}")

st.write("## Display Prioritized Sites")
recommend.recommend(os_df, rhus_per_city)