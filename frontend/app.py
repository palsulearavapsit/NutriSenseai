import streamlit as st
import requests
import pandas as pd
import uuid
from fpdf import FPDF  # fpdf2 also uses this import name


# ---------------- CONFIG ----------------
API_URL = "https://uvicorn-backend-app-main-app-host-0-0-0.onrender.com/analyze"

# ---------------- SESSION ----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "page" not in st.session_state:
    st.session_state.page = "Analyze"

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

# ---------------- NAVBAR ----------------
st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("🔍 Analyze"):
        st.session_state.page = "Analyze"
with nav2:
    if st.button("📜 History"):
        st.session_state.page = "History"
with nav3:
    if st.button("📄 Reports"):
        st.session_state.page = "Reports"

st.divider()
page = st.session_state.page

# ---------------- ANALYZE ----------------
if page == "Analyze":
    st.title("🥗 NutriSense AI")
    st.caption("AI-powered food ingredient intelligence")

    uploaded = st.file_uploader("Upload food label image", type=["jpg", "png"])
    text = st.text_area("Or paste ingredients manually")

    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            files = {"image": uploaded} if uploaded else {}
            data = {"text": text or "", "user_id": st.session_state.user_id}
            r = requests.post(API_URL, files=files, data=data, timeout=30)

            if r.status_code != 200:
                st.error(r.text)
                st.stop()

            result = r.json()
            st.session_state.latest_result = result

        st.success("Analysis complete")

        st.subheader("Ingredients")
        st.write(result.get("ingredients"))

        st.subheader("Health Score")
        st.metric("Score", result.get("health_score"), result.get("health_label"))

        st.subheader("Breakdown")
        st.dataframe(pd.DataFrame(result.get("categories", [])))

        st.subheader("Explanation")
        st.write(result.get("analysis"))

# ---------------- HISTORY ----------------
elif page == "History":
    st.title("📜 Scan History")

    r = requests.get(f"{API_URL}/history/{st.session_state.user_id}")
    history = r.json() if r.status_code == 200 else []

    if history:
        st.dataframe(pd.DataFrame(history))
    else:
        st.info("No scans yet.")

# ---------------- REPORTS ----------------
elif page == "Reports":
    st.title("📄 Reports")

    if not st.session_state.latest_result:
        st.info("Analyze something first.")
    else:
        res = st.session_state.latest_result

        if st.button("Generate PDF"):
            import os
            from fpdf import FPDF

            # ✅ Absolute path to font (CRITICAL FIX)
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            FONT_PATH = os.path.join(BASE_DIR, "DejaVuSans.ttf")

            pdf = FPDF()
            pdf.add_page()

            # ✅ Unicode-safe font
            pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
            pdf.set_font("DejaVu", size=12)

            def safe(text):
                if not text:
                    return ""
                return str(text)

            pdf.cell(0, 10, safe("NutriSense AI Report"), ln=True)
            pdf.ln(2)

            pdf.cell(
                0,
                10,
                safe(f"Health: {res.get('health_score')} ({res.get('health_label')})"),
                ln=True
            )

            pdf.ln(4)
            pdf.multi_cell(0, 8, safe("Ingredients:\n" + res.get("ingredients", "")))

            pdf.ln(4)
            pdf.multi_cell(0, 8, safe("Explanation:\n" + res.get("analysis", "")))

            file_path = os.path.join(BASE_DIR, "nutrisense_report.pdf")
            pdf.output(file_path)

            with open(file_path, "rb") as f:
                st.download_button(
                    "⬇️ Download PDF",
                    f,
                    file_name="nutrisense_report.pdf",
                    mime="application/pdf"
                )

