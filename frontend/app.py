import streamlit as st
import requests
import pandas as pd
import uuid
from fpdf import FPDF

API_URL = "https://uvicorn-backend-app-main-app-host-0-0-0.onrender.com/analyze"

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.title("🥗 NutriSense AI")

st.markdown("### Paste ingredients (from label or OCR):")
text = st.text_area("Ingredients")

if st.button("Analyze"):
    data = {"text": text, "user_id": st.session_state.user_id}
    r = requests.post(API_URL, data=data, timeout=20)

    if r.status_code != 200:
        st.error(f"Backend error {r.status_code}: {r.text}")
    else:
        result = r.json()
        st.success("Analysis complete!")

        st.subheader("Ingredients")
        st.write(result.get("ingredients"))

        st.subheader("Health Score")
        st.metric("Score", result.get("health_score"), result.get("health_label"))

        st.subheader("Breakdown")
        st.dataframe(pd.DataFrame(result.get("categories", [])))

        st.subheader("Explanation")
        st.write(result.get("analysis"))