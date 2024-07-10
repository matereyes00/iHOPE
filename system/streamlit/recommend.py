import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import streamlit as st
import os

def recommend(os_df, rhus_per_city):
    weights = {
        'popden_wom': 2,
        'popden_chi': 2,
        'popden_w_1': 2,
        'popden_you': 1,
        'popden_eld': 1
    }

    cities_in_solution = rhus_per_city.keys()
    filtered_df = os_df[os_df['city_name'].isin(cities_in_solution)]
    # Calculate priority score for each location in the new dataset
    filtered_df['Priority_Score'] = 0
    for group, weight in weights.items():
        filtered_df['Priority_Score'] += filtered_df[group] * weight

    # scaler = joblib.load('scaler.pkl')
    # Define the path to the .pkl file relative to the root of your GitHub repository
    scaler_file_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
    ANN_file_path = os.path.join(os.path.dirname(__file__), f'Neural_Network_model.pkl')

    # Check if the file exists in the specified path
    if os.path.exists(scaler_file_path):
        # Load the .pkl file using joblib
        scaler = joblib.load(scaler_file_path)
        # st.write("Scaler loaded successfullyyyyyy.")
        X_new = scaler.transform(filtered_df[['popden_wom', 'popden_chi', 'popden_w_1', 'popden_you', 'popden_eld', 'popden_all']])
        for name in ['Neural_Network']:
            if name == "Neural_Network":
                if os.path.exists(ANN_file_path):
                    model = joblib.load(ANN_file_path)
                    print("ANN called successfullyyyyyyyyyy....")
                    preds = model.predict(X_new)
                    filtered_df[f'{name}_Prediction'] = preds

        print(filtered_df[['ID', 'city_name', 'Priority_Score', 'Neural_Network_Prediction']])
        recommended_locations = {name: {} for name in ['Neural_Network']}
        # st.write(filtered_df[['ID', 'city_name', 'Priority_Score', 'Neural_Network_Prediction']])
        all_locations = []
        for city, num_rhus in rhus_per_city.items():
            if num_rhus >= 1:
                city_locations = filtered_df[filtered_df['city_name'] == city]
                top_locations = city_locations.nlargest(num_rhus, f'{name.replace(" ", "_")}_Prediction')
                recommended_locations[name][city] = top_locations['ID'].tolist()
                # print(recommended_locations[name][city])
                all_locations.append(recommended_locations[name][city])
                st.write(f"{city} : {recommended_locations[name][city]}")
    else:
        st.error(f"File '{file_path}' not found.")
    
    