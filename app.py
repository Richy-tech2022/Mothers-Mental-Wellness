import streamlit as st
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder

# Load trained model
model = joblib.load("mental_health_model.pkl")

# Page title and intro
st.title("🤱 Mamastrong: Postpartum Mental Wellness Checker")
st.markdown("""
Welcome, mama 💜 This tool helps assess your **mental health risk level** based on common postpartum factors.

Please answer the following questions as honestly as you can.
""")

# Numeric Inputs
sleep_hours = st.number_input("🛌 How many hours do you sleep on average per day?", min_value=0.0, max_value=24.0, step= 1.0)
baby_age = st.number_input("👶 How old is your youngest child? (in months)", min_value=0, max_value=48)
alone_time = st.number_input("⏱️ How many hours of alone/rest time do you get per week?", min_value=0.0, max_value=168.0, step=1.0)

num_children = st.number_input("🧒 How many children do you have?", min_value=1, max_value=10)

# Categorical Inputs
marital = st.selectbox("💑 Do you feel emotionally supported by your partner?", ["Yes", "No"])
financial = st.selectbox("💸 Are financial pressures affecting your peace of mind?", ["Yes", "No"])
physical = st.selectbox("💢 Are you experiencing physical symptoms due to exhaustion or stress?", ["Yes", "No"])
spiritual = st.selectbox("🙏 Do you engage in any spiritual or religious activity regularly?", ["Yes", "No"])
help_from_others = st.selectbox("👥 Do you receive regular help with baby/house chores?", ["Yes", "No"])
workload = st.selectbox("📊 How overwhelming do your daily responsibilities feel?", ["Low", "Medium", "High"])
medical_access = st.selectbox("🩺 Can you access medical or mental health support easily?", ["Yes", "No"])

# Encode inputs for model
encoded = []

# 1. SleepHours, 2. BabyAgeMonths, 3. NumChildren, 4. AloneTimeHours → numerical (no encoding needed)
encoded.extend([sleep_hours, baby_age, alone_time, num_children])

# Encode Yes/No columns using 0/1
yes_no_fields = [marital, financial, physical, spiritual, help_from_others, medical_access]
encoded.extend([1 if val == "Yes" else 0 for val in yes_no_fields])

# Add AloneTimeHours (already added above)

# Encode workload
workload_encoder = LabelEncoder()
workload_encoder.fit(["Low", "Medium", "High"])
encoded.append(workload_encoder.transform([workload])[0])

# Predict and display result
if st.button("🧠 Check My Mental Health Risk"):
    prediction = model.predict([encoded])[0]
    
    if prediction == 1:
        st.error("⚠️ You are likely at **HIGH mental health risk**. Please consider speaking with a healthcare provider or joining a support group.")
    else:
        st.success("✅ You are currently at **LOW mental health risk**. Keep prioritizing your well-being, mama!")

    st.caption("Note: This tool is for educational use and should not replace professional diagnosis.")
