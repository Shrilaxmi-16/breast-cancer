import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import numpy as np


st.set_page_config(

    page_title="Breast Cancer Prediction App",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_clean_data():
 data = pd.read_csv("data.csv")

 return data


def load_model(input_data):
    input_data = get_scaled_values(input_data)
    # Load the model and scaler
    loaded_voting_clf = joblib.load('voting_clf_model.joblib')
    loaded_scaler = joblib.load('scaler.joblib')
    return loaded_voting_clf, loaded_scaler


def get_scaled_values(input_dict) :
    data=get_clean_data()
    X = data.drop (['diagnosis'],axis=1)
    scaled_dict ={}
     
    for key,value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value-min_val)/(max_val-min_val)
        scaled_dict[key]= scaled_value

    return scaled_dict


def get_radar_chart(input_data):
    # Scale the values
    input_data = get_scaled_values(input_data)

    
    fig = go.Figure()  

    
    fig.add_trace(
        go.Scatterpolar(
            r=[input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
                input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
                input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
                input_data['fractal_dimension_mean']],

            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points',
                   'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Mean'
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'], input_data['area_se'],
                input_data['smoothness_se'], input_data['compactness_se'], input_data['concavity_se'],
                input_data['concave points_se'], input_data['symmetry_se'], input_data['fractal_dimension_se']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points',
                   'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Standard Error'
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
                input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
                input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
                input_data['fractal_dimension_worst']],
            theta=['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points',
                   'Symmetry', 'Fractal Dimension'],
            fill='toself',
            name='Worst'
        )
    )

    # Update the layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        autosize=True
    )
    return fig 


def add_sidebar(data):
    st.sidebar.header("Cell Nuclei Measurements  :microscope:")
    data=get_clean_data()
    # Define the labels
    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    
    input_data = {}

    for label, key in slider_labels:
        input_data[key] = st.sidebar.slider(
            label,
            min_value=float(0),
            max_value=float(data[key].max()),
            value=float(data[key].mean())
        )
        

    return input_data

    
def display_predictions(input_data, loaded_voting_clf, loaded_scaler):

    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_data_scaled = loaded_scaler.transform(input_array)
    prediction = loaded_voting_clf.predict(input_data_scaled)
    st.write("\n\n")

    st.subheader('Cell cluster prediction')
    st.write("\n\n")
    st.write("The cell cluster is: ")
    
    st.write("\n\n")
    

    if prediction[0] == 0:
        st.markdown(
            """
            <div style="background-color: green; color: white; padding: 20px; border-radius: 5px; width: 200px; margin: 20px auto; text-align: center; font-size: 24px; font-weight: bold; display: flex; justify-content: center; align-items: center;">
                Benign
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background-color: red; color: white; padding: 20px; border-radius: 5px; width: 250px; margin: 20px auto; text-align: center; font-size: 24px; font-weight: bold; display: flex; justify-content: center; align-items: center;">
                Malicious
            </div>
            """,
            unsafe_allow_html=True
        )
        
    



def main():


    data=get_clean_data()

    input_data = add_sidebar(data)

    st.title("Breast Cancer Predictor ")
    st.write("You can use this app to predict whether a breast mass is benign or malignant based on your cytology lab's measurements, and you can also adjust the values manually using the sidebar sliders.")
    
    
    col1, col2 = st.columns([2, 3])
    

    with col1:
        loaded_voting_clf, loaded_scaler = load_model(input_data)
        prediction_text = display_predictions(input_data, loaded_voting_clf, loaded_scaler)
        
    with col2:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart.to_dict())

  
st.markdown(
    """
    <style>
        .footer-warning {
            position: fixed;
            bottom: 10px;
            left: 10px;
            width: 100%;
            padding: 5px;
            text-align: center;
            font-weight: bold;
        }
    </style>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    
    <div class="footer-warning">
        <i class='fas fa-exclamation-triangle' style='font-size: 18px; color: red; margin-right: 5px;'></i>
        <span style='font-size: 14px;'>This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis!</span>
    </div>
    """,
    unsafe_allow_html=True
)

if __name__ == '__main__':
    main()