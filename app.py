import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path='apikey.env')

# Page config
st.set_page_config(
    page_title="AI Medical Diagnostics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextArea textarea {
        background-color: #262730;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .report-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #4a4a4a;
    }
    .card-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Header
st.title("🩺 AI Medical Diagnostics")
st.markdown("### Powered by Multi-Agent Artificial Intelligence")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info(
        "This application uses a multi-agent system to analyze medical reports. "
        "Agents include a Cardiologist, Psychologist, and Pulmonologist, "
        "culminating in a final diagnosis by a Multidisciplinary Team."
    )
    st.markdown("---")
    st.markdown("Made with ❤️ by Agentic AI")

# Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Patient Medical Report")
    medical_report = st.text_area(
        "Paste the medical report here:",
        height=400,
        placeholder="Enter patient details, symptoms, medical history, and test results..."
    )
    
    analyze_btn = st.button("🔍 Analyze Report", type="primary")

if analyze_btn and medical_report:
    with col2:
        st.subheader("📊 Analysis Results")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize agents
        agents = {
            "Cardiologist": Cardiologist(medical_report),
            "Psychologist": Psychologist(medical_report),
            "Pulmonologist": Pulmonologist(medical_report)
        }
        
        responses = {}
        
        # Run specialized agents concurrently
        status_text.text("Consulting specialists...")
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(agent.run): name for name, agent in agents.items()}
            
            completed_count = 0
            for future in as_completed(futures):
                agent_name = futures[future]
                try:
                    response = future.result()
                    responses[agent_name] = response
                    completed_count += 1
                    progress_bar.progress(int((completed_count / 4) * 100))
                except Exception as e:
                    st.error(f"Error from {agent_name}: {e}")
        
        # Display individual reports
        st.markdown("#### Specialist Consultations")
        
        with st.expander("🫀 Cardiologist Report", expanded=True):
            st.markdown(responses.get("Cardiologist", "No report generated."))
            
        with st.expander("🧠 Psychologist Report", expanded=True):
            st.markdown(responses.get("Psychologist", "No report generated."))
            
        with st.expander("🫁 Pulmonologist Report", expanded=True):
            st.markdown(responses.get("Pulmonologist", "No report generated."))
            
        # Run Multidisciplinary Team
        status_text.text("Convening Multidisciplinary Team...")
        
        team_agent = MultidisciplinaryTeam(
            cardiologist_report=responses.get("Cardiologist"),
            psychologist_report=responses.get("Psychologist"),
            pulmonologist_report=responses.get("Pulmonologist")
        )
        
        final_diagnosis = team_agent.run()
        progress_bar.progress(100)
        status_text.text("Analysis Complete")
        
        st.markdown("---")
        st.markdown("### 📋 Final Multidisciplinary Diagnosis")
        st.success(final_diagnosis)

elif analyze_btn and not medical_report:
    st.warning("Please enter a medical report to analyze.")
