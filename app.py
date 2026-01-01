import streamlit as st
import pandas as pd
import dill
import plotly.express as px
import smtplib
from email.message import EmailMessage

# --- PAGE CONFIG ---
st.set_page_config(page_title="EduPredict Pro", page_icon="🎓", layout="wide")

# --- GLOBAL DARK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #1e293b !important; }
    .stSelectbox label, .stSlider label, .stHeader h1, .stHeader h2, p { color: #e2e8f0 !important; }
    div[data-baseweb="select"] > div { background-color: #1e293b !important; color: white !important; border: 1px solid #334155; }
    .prediction-container {
        background-color: #1e293b; padding: 40px; border-radius: 20px;
        color: #ffffff; text-align: center; border: 1px solid #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2); margin: 20px 0;
    }
    .score-value { font-size: 72px; font-weight: 800; color: #10b981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.5); margin: 0; }
    .stButton>button { background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%); color: white; border-radius: 12px; height: 3.5em; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- MODEL LOADING ---
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        return dill.load(f)

model = load_model()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📌 Dashboard")
page = st.sidebar.radio("Navigation", ["Single Prediction", "Batch Prediction", "Scenario Simulator", "Data Analytics"])

# --- PAGE 1: SINGLE PREDICTION ---
if page == "Single Prediction":
    st.title("🎓 Student Score Predictor")
    st.write("Enter details below to generate an AI-powered math score estimate.")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["female", "male"])
            race = st.selectbox("Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
            lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
        with col2:
            edu = st.selectbox("Parental Education", ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"])
            prep = st.selectbox("Test Prep Course", ["none", "completed"])
            reading = st.slider("Reading Score", 0, 100, 70)
            writing = st.slider("Writing Score", 0, 100, 70)
        
        submit = st.button("🚀 RUN ANALYSIS")

    if submit:
        data = pd.DataFrame([[gender, race, edu, lunch, prep, reading, writing]], 
                            columns=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course', 'reading_score', 'writing_score'])
        
        pred = model.predict(data)[0]
        final_score = max(0, min(100, pred))

        # NEON RESULT CARD
        st.markdown(f"""
            <div class="prediction-container">
                <p style="text-transform: uppercase; letter-spacing: 3px; font-size: 14px; color: #94a3b8;">Predicted Math Proficiency</p>
                <h1 class="score-value">{final_score:.2f}</h1>
                <p style="color: #64748b; font-size: 14px;">Calculated using Linear Regression v1.6.1</p>
            </div>
        """, unsafe_allow_html=True)

        if final_score >= 75: st.balloons()

        # --- NEW EMAIL FEATURE (Correctly Indented) ---
        st.markdown("---")
        st.subheader("📩 Send Report via Email")
        receiver_email = st.text_input("Enter recipient email address")
        
        if st.button("Send Prediction Report"):
            if receiver_email:
                try:
                    SENDER_EMAIL = "your_email@gmail.com"
                    SENDER_PASSWORD = "your_app_password" 

                    msg = EmailMessage()
                    msg.set_content(f"The predicted Math Score for the student is: {final_score:.2f}/100 based on their profile.")
                    msg['Subject'] = f"Student Performance Report - {final_score:.2f}%"
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = receiver_email

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                        smtp.send_message(msg)
                    
                    st.success(f"Report successfully sent to {receiver_email}!")
                except Exception as e:
                    st.error("Failed to send email. Check your SMTP settings and App Password.")
            else:
                st.warning("Please enter a valid email address.")

# --- PAGE 2: BATCH PREDICTION ---
elif page == "Batch Prediction":
    st.title("📁 Batch Processing")
    uploaded_file = st.file_uploader("Upload Student Data (CSV)", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if st.button("Process Batch"):
            df['Predicted_Math_Score'] = model.predict(df)
            st.dataframe(df)
            st.download_button("📥 Download Results", df.to_csv(index=False), "predictions.csv")

# --- PAGE 3: SCENARIO SIMULATOR ---
elif page == "Scenario Simulator":
    st.title("🧪 Scenario Simulator")
    r_score = st.slider("Mock Reading Score", 0, 100, 70)
    w_score = st.slider("Mock Writing Score", 0, 100, 70)
    
    res = []
    for p in ['none', 'completed']:
        d = pd.DataFrame([['female', 'group B', "some college", 'standard', p, r_score, w_score]], 
                         columns=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course', 'reading_score', 'writing_score'])
        res.append(model.predict(d)[0])
    
    st.write(f"Difference with Prep Course: **+{res[1]-res[0]:.2f} points**")
    st.bar_chart({"No Prep": res[0], "Completed Prep": res[1]})

# --- PAGE 4: DATA ANALYTICS ---
elif page == "Data Analytics":
    st.title("📊 Model Analytics")
    df_chart = pd.DataFrame({'Reading': range(40,100), 'Math': [x*0.85 + 7 for x in range(40,100)]})
    fig = px.scatter(df_chart, x="Reading", y="Math", trendline="ols", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("EduPredict Pro | Aman_Patre")