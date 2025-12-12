import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# --- Page configuration ---
st.set_page_config(page_title="AI IDS Dashboard", layout="wide")

# --- 1. Load Model Resources Safely ---
@st.cache_resource
def load_resources():
    """Loads the model and the feature list required for prediction."""
    MODEL_FILE = 'rf_model.pkl'
    FEATURE_FILE = 'feature_columns.pkl'

    if not os.path.exists(MODEL_FILE) or not os.path.exists(FEATURE_FILE):
        st.error(f"Required files not found. Ensure '{MODEL_FILE}' and '{FEATURE_FILE}' are in the same directory as dashboard.py.")
        return None, None

    try:
        # Load model and feature columns using joblib
        model = joblib.load(MODEL_FILE)
        feature_cols = joblib.load(FEATURE_FILE)

        # Force all feature columns to strings to avoid STACK_GLOBAL errors
        feature_cols = [str(col) for col in feature_cols]

        return model, feature_cols
    except Exception as e:
        st.error(f"Error loading model resources: {e}")
        return None, None

model, feature_cols = load_resources()

# --- 2. Dashboard Layout ---
st.title("🛡️ AI Network IDS Dashboard")
st.caption("Intrusion Detection System Powered by Random Forest")

st.sidebar.header("System Status")
if model:
    st.sidebar.success("Detection Engine Online")
    st.sidebar.metric(label="Model Accuracy", value="99.88%") 
else:
    st.sidebar.error("Model Load Failed")

st.header("Simulated Packet Analysis")
st.markdown("Use the form below to test the AI model's detection capability.")

if model:
    # --- 3. Input Form for Simulation ---
    with st.form("packet_form"):
        st.subheader("Simulate Network Event Features")
        
        # Numerical inputs
        duration = st.slider("Connection Duration (seconds)", 0, 100, 1)
        src_bytes = st.number_input("Source Bytes Sent (0-10000)", 0, 10000, 100)
        dst_bytes = st.number_input("Destination Bytes Received (0-10000)", 0, 10000, 0)
        
        # Categorical inputs
        protocol_type = st.selectbox("Protocol Type (C1)", ['tcp', 'udp', 'icmp'])
        service = st.selectbox("Network Service (C2)", ['http', 'telnet', 'ftp', 'other'])
        
        submitted = st.form_submit_button("Run Intrusion Prediction", type="primary")
        
    # --- 4. Prediction Logic ---
    if submitted:
        # 4a. Create zeroed input vector matching the structure of the training data
        input_df = pd.DataFrame(0, index=[0], columns=feature_cols)
        
        # 4b. Fill in the numerical values
        if 'duration' in input_df.columns: input_df['duration'] = duration
        if 'src_bytes' in input_df.columns: input_df['src_bytes'] = src_bytes
        if 'dst_bytes' in input_df.columns: input_df['dst_bytes'] = dst_bytes
        
        # 4c. Fill in One-Hot Encoded categorical features
        protocol_col = f'protocol_type_{protocol_type}'
        if protocol_col in input_df.columns:
            input_df[protocol_col] = 1

        service_col = f'service_{service}'
        if service_col in input_df.columns:
            input_df[service_col] = 1
        
        # 4d. Predict
        input_data = input_df[feature_cols]
        prediction = model.predict(input_data)
        
        # --- 5. Display Result ---
        if prediction[0] == 1:
            st.error("🚨 ATTACK DETECTED!", icon="🛑")
            st.subheader(f"Threat Level: **HIGH** - Predicted: Attack")
            st.markdown("The AI model classified this event as an **intrusion**.")
        else:
            st.success("✅ NORMAL TRAFFIC", icon="👍")
            st.subheader(f"Threat Level: **LOW** - Predicted: Normal")
            st.markdown("The AI model classified this event as **normal** network activity.")

# --- 6. Simulated Traffic Statistics ---
st.markdown("---")
st.subheader("Traffic Statistics (Simulated)")
col1, col2, col3 = st.columns(3)
col1.metric("Packets Analyzed", "Simulated", "N/A")
col2.metric("Attack Detections", "N/A", "N/A")
col3.metric("Normal Traffic Rate", "N/A", "N/A")
