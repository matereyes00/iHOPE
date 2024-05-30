import pandas as pd 
import numpy as np
# Define the HCI calculation function
def HCI_calc(total_ai, total_gi, total_hi, total_ji, total_ki, total_mi,distance, road_bi, POI_ci, landCov_di, hazard1_ei, hazard2_ei, hazard3_ei, rhus_fi):
    total_vulnerable = total_gi + total_hi + total_ji + total_ki + total_mi
    total_pop = total_ai
    population_to_be_served = total_vulnerable + np.maximum(0, total_pop - total_vulnerable)
    # Calculate y for the entire Series without using if condition
    y = np.where(population_to_be_served == 0, 0, 20000 / ((population_to_be_served) * (distance + rhus_fi)))
    mc = np.tanh(y)
    w_bi = 0.3 # roads
    w_ci = 0.2 # POIs
    w_di = 0.5 # land cov
    b = (POI_ci * w_ci) + (road_bi * w_bi) + (landCov_di * w_di)
    # Normalize each factor
    rain_intensity_normalized = (hazard1_ei - hazard1_ei.min()) / (hazard1_ei.max() - hazard1_ei.min())
    flood_probability_normalized = (hazard2_ei - hazard2_ei.min()) / (hazard2_ei.max() - hazard2_ei.min())
    drought_mean_normalized = (hazard3_ei - hazard3_ei.min()) / (hazard3_ei.max() - hazard3_ei.min())
    w_rain = 0.4
    w_flood = 0.3
    w_drought = 0.3
    c = (w_rain * rain_intensity_normalized) + (w_flood * flood_probability_normalized) + (w_drought * drought_mean_normalized)
    f = b - c
    f = np.tanh(f)
    hci = mc * f
    hcfai = (1 + np.tanh(hci / 2)) / 2  # Sigmoid function

    return hcfai

# Computing overall HCFAI using SUM
def overallHCFAI(region_df):
    HCFAI_overall = region_df['HCFAI'].sum()
    return HCFAI_overall

# Select top N candidate sites based on HCFAI score computed from region_df
def selectTopSites(candidate_sites, region_df, n):
    # Merge candidate_sites with region_df based on a common identifier (e.g., ID)
    # print(f"Region df: {region_df.columns}")
    # print(f"Candidate sites: {candidate_sites.columns}")
    # Define the columns to merge
    columns_to_merge = ['ID',
                        'popden_chi', 'popden_eld', 'popden_wom', 'popden_you', 'popden_w_1',
                        'popden_all', 'flood_probability_value', 'rain intensity_value',
                        'drought_value', 'buildability_landcov', 'RHU_Presence',
                        'Road_Presence', 'POI_Presence', 'Nearest_RHU',
                        'Distance_to_Nearest_RHU_km', 'total_population']

    # Merge only the specified columns from region_df to candidate_sites
    merged_sites = candidate_sites.merge(region_df[columns_to_merge], on='ID', how='left')
    # print(f"Merged: {merged_sites.columns}")
    # Create a new DataFrame without the column 'Unnamed: 0'
    # merged_sites = candidate_sites.merge(region_df, on='ID', how='left')
    # Compute HCFAI scores for candidate sites using data from region_df
    merged_sites['HCFAI'] = HCI_calc(merged_sites['popden_all'],
                                    merged_sites['popden_chi'],
                                    merged_sites['popden_eld'],
                                    merged_sites['popden_wom'],
                                    merged_sites['popden_you'],
                                    merged_sites['popden_w_1'],
                                    merged_sites['Distance_to_Nearest_RHU_km'],
                                    merged_sites['Road_Presence'],
                                    merged_sites['POI_Presence'],
                                    merged_sites['buildability_landcov'],
                                    merged_sites['rain intensity_value'],
                                    merged_sites['flood_probability_value'],
                                    merged_sites['drought_value'],
                                    merged_sites['RHU_Presence'],
                                    )

    # Fill missing values from region_df to candidate_sites
    missing_cols = [col for col in region_df.columns if col != ['ID']]
    for col in missing_cols:
        # Set the index of region_df to 'ID' if it's not already set
        if 'ID' not in region_df.columns:
            region_df.set_index('ID', inplace=True)
        # Fill missing values in merged_sites using values from region_df
        merged_sites[col] = merged_sites[col].fillna(region_df[col])

    # Select top N sites based on computed HCFAI scores
    top_sites = merged_sites.sort_values(by='HCFAI', ascending=False).head(n)
    return top_sites

# Remove adjacent sites from the list of candidate sites
def removeAdjacentSites(region_df, candidate_sites, selected_sites, neighbors_df):
    # Get the indices of hexagons with existing health facilities
    idx_with_RHU = region_df[region_df['RHU_Presence'] == 1]
    # Initialize a set to store adjacent sites
    adjacent_sites = set()
    # Add neighbors of selected sites
    for site_id in selected_sites['ID']:
        if site_id in neighbors_df['ID'].values:
            neighbors = neighbors_df.loc[neighbors_df['ID'] == site_id, 'Neighbors'].iloc[0]
            adjacent_sites.update(neighbors.split(','))
    # Add hexagons with existing health facilities and the selected sites themselves
    adjacent_sites.update(idx_with_RHU['ID'])
    adjacent_sites.update(selected_sites['ID'])
    # Convert the adjacent sites to integers
    adjacent_sites = [int(site) for site in adjacent_sites]
    # Remove adjacent sites from the candidate sites
    candidate_sites = candidate_sites[~candidate_sites['ID'].isin(adjacent_sites)]
    # Recalculate HCFAI values for selected sites using data from region_df
    selected_sites['HCFAI'] = HCI_calc(selected_sites['popden_all'], selected_sites['popden_chi'],
                                    selected_sites['popden_eld'], selected_sites['popden_wom'],
                                    selected_sites['popden_you'], selected_sites['popden_w_1'],
                                    selected_sites['Distance_to_Nearest_RHU_km'],
                                    selected_sites['Road_Presence'], selected_sites['POI_Presence'],
                                    selected_sites['buildability_landcov'], selected_sites['rain intensity_value'],
                                    selected_sites['flood_probability_value'], selected_sites['drought_value'],
                                    selected_sites['RHU_Presence'])
    return candidate_sites, selected_sites, idx_with_RHU

# Optimize the selection of health facility sites
def optimize(region_df, candidate_sites, neighbors_df, num_facilities):
    # Print original HCFAI
    original_HCFAI = overallHCFAI(region_df)
    print("Original HCFAI:", original_HCFAI)
    selected_sites = pd.DataFrame(columns=region_df.columns)
    while len(selected_sites) < num_facilities:
        # Select top candidate sites
        top_sites = selectTopSites(candidate_sites, region_df, num_facilities - len(selected_sites))
        print("Selected candidate sites HCFAI:")
        # print(top_sites[['ID', 'HCFAI']])  # Print only ID and HCFAI columns

        # Remove adjacent sites from candidate list and update HCFAI for selected sites
        candidate_sites, top_sites, idx_with_RHU = removeAdjacentSites(region_df, candidate_sites, top_sites, neighbors_df)
        # Add selected sites to the final list
        selected_sites = pd.concat([selected_sites, top_sites])

        # Calculate HCFAI for the remaining sites in region_df
        remaining_sites = region_df[~region_df['ID'].isin(selected_sites['ID'])]
        remaining_HCFAI = overallHCFAI(remaining_sites)
        selected_sites_HCFAI = overallHCFAI(selected_sites)

        # Calculate updated overall HCFAI
        updated_HCFAI = remaining_HCFAI + selected_sites_HCFAI
        print("Updated HCFAI:", updated_HCFAI)

        if len(selected_sites) == num_facilities:
            print("Accept!!!!!!!!!!!!!!")
            return selected_sites, idx_with_RHU, original_HCFAI, updated_HCFAI
        else:
            print("Reject!!!!!!!!!!!!!!")
            print("Selected sites:", len(selected_sites))

    return selected_sites, idx_with_RHU, original_HCFAI, updated_HCFAI


# raw_rg1_clustered = pd.read_csv("../CandidateSites/rg1_PCF_data.csv") # for finding optimal locations
# # existing_region_rhus = pd.read_csv("../CandidateSites/rg1-clusters.xlsx") # finding existing rhus
# neighbors_df = pd.read_csv('../CandidateSites/rg1_Neighbors.csv')
# candidate_sites = pd.read_csv("../CandidateSites/rg1_candidate_sites.csv")
# neighbors_df.rename(columns={'fid': 'ID'}, inplace=True)
# raw_rg1_clustered = raw_rg1_clustered.drop(columns=['Neighbors'])
# # raw_rg1_clustered.columns

# # print(list(candidate_sites['ID']))
# print(f"Candidate sites: {len(candidate_sites)}")
# PCF = 363
# # Optimize selection of health facility sites
# selected_facilities, hex_with_RHU, og_HCFAI, updated_HCFAI = optimize(raw_rg1_clustered, candidate_sites, neighbors_df, PCF) # 81 for dropping non buildable; 363 for validation
# print(selected_facilities)

# selected_facilities = list(selected_facilities['ID'])
# print(selected_facilities)