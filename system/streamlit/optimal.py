import pandas as pd 
import numpy as np
import streamlit as st
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
# ⭐️ this is the one!

def HCI_calc(total_ai, total_gi, total_hi, total_ji, total_ki, total_mi, distance, road_bi, POI_ci, landCov_di, hazard1_ei, hazard2_ei, hazard3_ei, rhus_fi):
    total_vulnerable = total_gi + total_hi + total_ji + total_ki + total_mi
    total_pop = total_ai
    population_to_be_served = total_vulnerable + np.maximum(0, total_pop - total_vulnerable)
    y = np.where(population_to_be_served == 0, 0, 20000 / ((population_to_be_served) * (distance + rhus_fi)))
    mc = np.tanh(y)
    w_bi = 0.3  # roads
    w_ci = 0.2  # POIs
    w_di = 0.5  # land cov
    b = (POI_ci * w_ci) + (road_bi * w_bi) + (landCov_di * w_di)
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

def overallHCFAI(region_df):
    if 'HCFAI' in region_df.columns:
        HCFAI_overall = region_df['HCFAI'].sum()
    elif 'new HCFAI' in region_df.columns:
        HCFAI_overall = region_df['new HCFAI'].sum()
    return HCFAI_overall

def selectTopSites(candidate_sites, region_df, selected_sites, n):
    if len(selected_sites) < n:  # if optimal and existing RHUs list is incomplete
        while len(selected_sites) < n:
            new_site = candidate_sites.iloc[:1].copy()
            selected_sites = pd.concat([selected_sites, new_site], ignore_index=True)
            selected_sites['RHU_Presence'] = 1
            candidate_sites = candidate_sites.drop(candidate_sites.index[0]).reset_index(drop=True)

    region_df = region_df.drop('total_population', axis=1)
    columns_to_merge = ['ID',
                        'popden_chi', 'popden_eld', 'popden_wom', 'popden_you', 'popden_w_1',
                        'popden_all', 'flood_probability_value', 'rain intensity_value',
                        'drought_value', 'buildability_landcov', 'RHU_Presence',
                        'Road_Presence', 'POI_Presence', 'Nearest_RHU', 
                        'Distance_to_Nearest_RHU_km']

    merged_sites = candidate_sites.merge(region_df[columns_to_merge], on='ID', how='left')
    
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

    missing_cols = [col for col in region_df.columns if col != 'ID']
    for col in missing_cols:
        if 'ID' not in region_df.columns:
            region_df.set_index('ID', inplace=True)
        merged_sites[col] = merged_sites[col].fillna(region_df[col])

    top_sites = merged_sites.sort_values(by='HCFAI', ascending=False).head(n)
    return top_sites

def removeAdjacentSites(region_df, candidate_sites, selected_sites, neighbors_df, n):
    idx_with_RHU = region_df[region_df['RHU_Presence'] == 1]
    adjacent_sites = set()
    with_RHU_indices = selected_sites['ID'].tolist()
    for site_id in selected_sites['ID']:
        if site_id in neighbors_df['ID'].values:
            neighbors = neighbors_df.loc[neighbors_df['ID'] == site_id, 'Neighbors'].iloc[0]
            adjacent_sites.update(neighbors.split(','))
    adjacent_sites.update(idx_with_RHU['ID'])
    adjacent_sites.update(selected_sites['ID'])
    adjacent_sites = [int(site) for site in adjacent_sites]
    candidate_sites = candidate_sites[~candidate_sites['ID'].isin(adjacent_sites)].reset_index(drop=True)

    print(f"{len(candidate_sites)} Candidate sites left")
    print(f"This is what we'll put on QGIS: {selected_sites['ID'].tolist()}")

    if len(candidate_sites) > n:
        for i in with_RHU_indices:
            print(f"Site {i} has the following sites to choose from: {candidate_sites['ID'].tolist()}")
            if i in adjacent_sites:
                print(f"Site {i} was highkey sus for not saying they have neighbors ...")
                with_RHU_indices.remove(i)
                selected_sites = selected_sites.drop(selected_sites[selected_sites['ID'] == i].index).reset_index(drop=True)
    elif len(candidate_sites) <= n:
        return candidate_sites, selected_sites, idx_with_RHU

    selected_sites['HCFAI'] = HCI_calc(selected_sites['popden_all'], selected_sites['popden_chi'],
                                        selected_sites['popden_eld'], selected_sites['popden_wom'],
                                        selected_sites['popden_you'], selected_sites['popden_w_1'],
                                        selected_sites['Distance_to_Nearest_RHU_km'],
                                        selected_sites['Road_Presence'], selected_sites['POI_Presence'],
                                        selected_sites['buildability_landcov'], selected_sites['rain intensity_value'],
                                        selected_sites['flood_probability_value'], selected_sites['drought_value'],
                                        selected_sites['RHU_Presence'])
    return candidate_sites, selected_sites, idx_with_RHU

def optimize(region_df, candidate_sites, neighbors_df, num_facilities):
    original_HCFAI = overallHCFAI(region_df)
    print("Original HCFAI:", original_HCFAI)
    selected_sites = pd.DataFrame(columns=region_df.columns)
    top_sites = selectTopSites(candidate_sites, region_df, selected_sites, num_facilities - len(selected_sites))

    while len(selected_sites) < num_facilities:
        candidate_sites, top_sites, idx_with_RHU = removeAdjacentSites(region_df, candidate_sites, top_sites, neighbors_df, num_facilities)
        if len(candidate_sites) <= num_facilities:
            top_sites = candidate_sites
        elif len(candidate_sites) > num_facilities:
            top_sites = selectTopSites(candidate_sites, region_df, selected_sites, num_facilities - len(selected_sites))
            selected_sites = top_sites
        selected_sites = pd.concat([selected_sites, top_sites]).reset_index(drop=True)
        remaining_sites = region_df[~region_df['ID'].isin(selected_sites['ID'])]
        remaining_HCFAI = overallHCFAI(remaining_sites)
        selected_sites_HCFAI = overallHCFAI(selected_sites)
        updated_HCFAI = remaining_HCFAI + selected_sites_HCFAI
        print("Updated HCFAI:", updated_HCFAI)
        print(f"{len(selected_sites)} selected sites")
        if len(selected_sites) == num_facilities:
            print("Accept!!!!!!!!!!!!!!")
            return selected_sites, idx_with_RHU, original_HCFAI, updated_HCFAI
        elif len(candidate_sites) <= num_facilities:
            return selected_sites, idx_with_RHU, original_HCFAI, updated_HCFAI
        else:
            print("Reject!!!!!!!!!!!!!!")
            print("Selected sites:", len(selected_sites))
            top_sites = selectTopSites(candidate_sites, region_df, selected_sites, num_facilities - len(selected_sites))

    return selected_sites, idx_with_RHU, original_HCFAI, updated_HCFAI

def process_population_density(rg1_clustered_df, os, a=1.65):
    # Filtering the DataFrame using the list of IDs
    os_df = rg1_clustered_df[rg1_clustered_df['ID'].isin(os)]

    # Population density columns
    all_pd = os_df['popden_all']
    women_pd = os_df['popden_wom']
    womenrep_pd = os_df['popden_w_1']
    youth_pd = os_df['popden_you']
    elder_pd = os_df['popden_eld']
    children_pd = os_df['popden_chi']

    # Calculating total population based on the multiplier 'a'
    os_df['total_population'] = all_pd * a
    os_df['total_population_women'] = women_pd * a
    os_df['total_population_womenrep'] = womenrep_pd * a
    os_df['total_population_youth'] = youth_pd * a
    os_df['total_population_elderly'] = elder_pd * a
    os_df['total_population_children'] = children_pd * a

    return os_df

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


# os = [2888904, 2879241, 2886146, 2934504, 2880629, 2924806, 2877860, 2926188, 2927569, 2926187, 2926192, 2926190, 2886161, 2963475, 2964859, 2966240, 2967622, 2966241, 2962084, 2962083, 2944191, 2927590, 2946965, 2948346, 2946966, 2931721, 2941372, 2948345, 2934475, 2969064, 2915170, 2938611, 2869558, 2967681, 2931720, 2915186, 2912423, 2913805, 2916568, 2944136, 2942762, 2888927, 2891691, 2891690, 2890308, 2945463, 2945464, 2946846, 2944082, 2944083, 2946847, 2905500, 2906881, 2902737, 2904118, 2899974, 2887545, 2956481, 2887544, 2934476, 2883394, 2882011, 2948211, 2946845, 2946844, 2948226, 2944081, 2945462, 2945461, 2942698, 2944080, 2942697, 2927608, 2901356, 2880628, 2880627, 2879244, 2924866, 2926225, 2937185, 2886155, 2882008, 2887536, 2883391, 2884772, 2882009, 2888919, 2909647, 2908265, 2908264, 2888920, 2890301, 2884775, 2886156, 2886157, 2887537, 2887538, 2883393, 2883392, 2884774, 2890300, 2884773, 2891683, 2882010, 2960769, 2962152, 2963534, 2886140, 2963533, 2959388, 2960770, 2875076, 2962151, 2960771, 2959387, 2985660, 2926226, 2949623, 2941316, 2945458, 2948223, 2946841, 2927574, 2937194, 2912413, 2911033, 2913796, 2902733, 2898587, 2901351, 2898589, 2895823, 2898588, 2899970, 2897206, 2946833, 2949599, 2949598, 2950979, 2950978, 2942753, 2917950, 2980135, 2978755, 2930262, 2901357, 2904121, 2904119, 2904120, 2905501, 2905502, 2902740, 2905503, 2906883, 2902739, 2906882, 2909648, 2902738, 2906884, 2906885, 2908266, 2941314, 2981515, 2949647, 2920714, 2909650, 2908267, 2908269, 2911030, 2911031, 2908268, 2911032, 2909649, 2905505, 2905504, 2904123, 2904122, 2906886, 2902741, 2941315, 2941406, 2928883, 2884765, 2886147, 2884764, 2941424, 2940042, 2938557, 2952388, 2952386, 2953768, 2939938, 2879218, 2908274, 2912417, 2911034, 2909654, 2911035, 2911036, 2911037, 2909653, 2912416, 2906891, 2915181, 2912418, 2906892, 2908273, 2913799, 2913800, 2908272, 2905510, 2898585, 2895822, 2897205, 2897204, 2898586, 2897199, 2895816, 2876471, 2956479, 2939990, 2937226, 2938608, 2904111, 2901346, 2901345, 2930332, 2948222, 2949604, 2945457, 2950985, 2946839, 2946840, 2945456, 2949605, 2949603, 2948221, 2942694, 2930335, 2931718, 2930336, 2931717, 2930337, 2928953, 2934458, 2935840, 2935841, 2873690, 2949634, 2982898, 2981516, 2868179, 2866797, 2877837, 2928949, 2905509, 2904127, 2906890, 2904126, 2905508, 2906889, 2909652, 2908271, 2939992, 2951008, 2952389, 2941324, 2952391, 2952390, 2951009, 2939941, 2872310, 2873691, 2876455, 2872309, 2870928, 2875073, 2906893, 2962023, 2883365, 2938609, 2882007, 2880626, 2935852, 2937232, 2935851, 2935818, 2913798, 2912415, 2913797, 2948240, 2945475, 2946858, 2913801, 2911039, 2912419, 2909657, 2909656, 2912420, 2906894, 2913802, 2908276, 2908275, 2915182, 2915183, 2916564, 2916565, 2911038, 2937227, 2931704, 2941412, 2964796, 2928972, 2928973, 2886154, 2886152, 2888916, 2888915, 2888914, 2888913, 2887535, 2890298, 2890299, 2887534, 2887533, 2887532, 2887531, 2886153, 2888917, 2884770, 2888918, 2886151, 2886150, 2884768, 2884769, 2869548, 2962022, 2963403, 2949593, 2948210, 2927573, 2877836, 2938655, 2948328, 2927592, 2869570, 2876458, 2877841, 2952387, 2951003, 2949622, 2951004, 2868169, 2890295, 2890293, 2894441, 2894443, 2894445, 2894446, 2890294, 2895824, 2895825, 2895826]
# rg = 1
# x = "../../CandidateSites/rg1-clusters.csv"
# rg1_clustered_df = pd.read_csv(x)
# rg1_clustered_df

def MCLP(os, rg1_clustered_df):
    os_df = process_population_density(rg1_clustered_df, os)

    os_df['HCFAI'] = HCI_calc(os_df['popden_all'], os_df['popden_chi'], os_df['popden_eld'],
                            os_df['popden_wom'],  os_df['popden_you'],  os_df['popden_w_1'],
                            os_df['Distance_to_Nearest_RHU_km'], os_df['Road_Presence'],
                            os_df['POI_Presence'], os_df['buildability_landcov'],
                            os_df['rain intensity_value'],
                            os_df['flood_probability_value'],
                            os_df['drought_value'], os_df['RHU_Presence'])

    grouped_df = os_df.groupby('city_name')
    grouped_df_visual = grouped_df.apply(lambda x: x.reset_index(drop=True))
    total_population_by_city = grouped_df_visual[['total_population', 'popden_all']]
    total_population_by_city_df = total_population_by_city.reset_index()
    total_population_grouped = total_population_by_city_df.groupby('city_name').sum()
    total_population_grouped = total_population_grouped.reset_index()
    total_population_grouped = total_population_grouped.drop(columns=['level_1'])
    total_population_dict = total_population_grouped.set_index('city_name')['total_population'].to_dict()

    rhu_capacity = 20000
    # Dictionary to store solutions for each solver
    all_solutions = {}
    solver_names = ['SAT', 'SCIP', 'GLOP', 'CBC']
    # Iterate over each solver
    for solver_name in solver_names:
        print(f"Solving with {solver_name} solver...")
        # Create the solver instance
        if solver_name == 'SAT':
            solver = pywraplp.Solver.CreateSolver('SAT')
        elif solver_name == 'SCIP':
            solver = pywraplp.Solver.CreateSolver('SCIP')
        elif solver_name == 'GLOP':
            solver = pywraplp.Solver.CreateSolver('GLOP')
        elif solver_name == 'CBC':
            solver = pywraplp.Solver.CreateSolver('CBC')
        else:
            raise ValueError(f"Unknown solver: {solver_name}")
        if not solver:
            raise Exception(f"{solver_name} solver not found!")

        # Define decision variables (number of RHUs to build for each city)
        rhus = {city: solver.IntVar(0, solver.infinity(), f'rhus_{city}') for city in total_population_dict.keys()}

        # Constraint: Ensure that the number of RHUs built in each city does not exceed the total population divided by the RHU capacity
        for city, population in total_population_dict.items():
            solver.Add(rhus[city] * rhu_capacity <= population)

        # Define the objective function: Maximize the total number of RHUs
        objective = solver.Objective()
        for city in rhus:
            objective.SetCoefficient(rhus[city], 1)
        objective.SetMaximization()

        # Solve the problem
        status = solver.Solve()

        # Check the result
        if status in [pywraplp.Solver.OPTIMAL]:
            print(f'Optimal solution found with {solver_name}!')
            total_rhus = 0
            rhus_per_city = {}
            for city in rhus:
                num_rhus = int(rhus[city].solution_value())
                total_rhus += num_rhus
                rhus_per_city[city] = num_rhus
                if num_rhus > 0:
                    print(f'{city}: Build {num_rhus} RHUs')
            print(f'Total RHUs built: {total_rhus}')
            all_solutions[solver_name] = rhus_per_city
        else:
            print(f'No optimal solution found with {solver_name}.')

    for solver_name, rhus_per_city in all_solutions.items():
        os_df[f'num_rhus_{solver_name}'] = os_df['city_name'].map(rhus_per_city).fillna(0).astype(int)
        if solver_name == "SCIP":
            return os_df, rhus_per_city