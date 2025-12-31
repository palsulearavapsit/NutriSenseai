import streamlit as st
import requests
import pandas as pd
import uuid
from fpdf import FPDF

# ================== GLOBAL STYLES ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background:
        radial-gradient(circle at 30% 10%, rgba(56,189,248,0.08), transparent 40%),
        radial-gradient(circle at 80% 20%, rgba(99,102,241,0.08), transparent 45%),
        linear-gradient(180deg, #0f172a 0%, #020617 70%);
    color: #e5e7eb;
}

.main { max-width: 900px; margin: auto; }

.navbar {
    position: sticky;
    top: 0;
    background: rgba(2, 6, 23, 0.9);
    backdrop-filter: blur(10px);
    padding: 1rem 0;
    border-bottom: 1px solid rgba(99,102,241,0.3);
    z-index: 999;
}

.stButton > button {
    border-radius: 10px;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    color: #020617;
    font-weight: 600;
    border: none;
    padding: 0.6rem 1.4rem;
    box-shadow: 0 0 12px rgba(99,102,241,0.6);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 18px rgba(34,211,238,0.9);
}

.card {
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(10px);
    border-radius: 14px;
    padding: 1.3rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(99,102,241,0.25);
}

h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #a5b4fc; }

[data-testid="stMetricValue"] {
    font-size: 2.2rem;
    font-weight: bold;
    color: #22d3ee;
}

[data-testid="stFileUploader"] {
    border: 2px dashed rgba(56,189,248,0.7);
    padding: 1rem;
    border-radius: 12px;
}

textarea {
    border-radius: 10px !important;
    background-color: rgba(2,6,23,0.6) !important;
    color: #e5e7eb !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== HELPERS ==================
def clean_for_pdf(text: str) -> str:
    if not text:
        return ""
    return text.encode("latin-1", "ignore").decode("latin-1")

API = "http://127.0.0.1:8000/analyze"

# ================== SESSION ==================
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "page" not in st.session_state:
    st.session_state.page = "Analyze"

# ================== NAVBAR ==================
st.markdown('<div class="navbar">', unsafe_allow_html=True)
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("🔍 Analyze", key="nav_analyze"):
        st.session_state.page = "Analyze"
with nav2:
    if st.button("📜 History", key="nav_history"):
        st.session_state.page = "History"
with nav3:
    if st.button("📄 Reports", key="nav_reports"):
        st.session_state.page = "Reports"
st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state.page
st.divider()

# ================== ANALYZE ==================
if page == "Analyze":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("🥗 NutriSense AI")
    st.caption("AI-powered food ingredient intelligence — from the universe to your plate 🌌")
    uploaded = st.file_uploader("Upload food label image", type=["jpg", "png"])
    text = st.text_area("Or paste ingredients manually")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Analyze", key="analyze_btn"):
        with st.spinner("Analyzing with cosmic intelligence..."):
            try:
                files = {"image": uploaded} if uploaded else None
                data = {"text": text, "user_id": st.session_state.user_id}
                r = requests.post(API, files=files, data=data, timeout=20)

                if r.status_code != 200:
                    st.error(f"Backend error: {r.text}")
                    st.stop()

                result = r.json()
                st.session_state.latest_result = result

            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
                st.stop()

            for title, content in [
                ("Ingredients", result.get("ingredients", "")),
                ("Health Score", None),
                ("Ingredient Breakdown", None),
                ("Explanation", result.get("analysis", "")),
            ]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader(title)
                if title == "Health Score":
                    st.metric("Score", result.get("health_score", "N/A"), result.get("health_label", ""))
                elif title == "Ingredient Breakdown":
                    st.dataframe(pd.DataFrame(result.get("categories", [])), use_container_width=True)
                else:
                    st.write(content)
                st.markdown('</div>', unsafe_allow_html=True)

# ================== HISTORY ==================
elif page == "History":
    st.title("📜 Scan History")
    try:
        h = requests.get(f"{API}/history/{st.session_state.user_id}", timeout=10)
        history = h.json() if h.status_code == 200 else []
    except:
        history = []

    st.markdown('<div class="card">', unsafe_allow_html=True)
    if isinstance(history, list) and history:
        st.dataframe(pd.DataFrame(history), use_container_width=True)
    else:
        st.info("No scans recorded yet.")
    st.markdown('</div>', unsafe_allow_html=True)

# ================== REPORTS ==================
elif page == "Reports":
    st.title("📄 AI Reports")

    if not st.session_state.latest_result:
        st.info("Analyze a product first to generate a report.")
    else:
        if st.button("Generate PDF Report", key="pdf_btn"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "NutriSense AI - Ingredient Report", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.ln(5)

            res = st.session_state.latest_result
            pdf.cell(0, 10, f"Health Score: {res.get('health_score')} ({res.get('health_label')})", ln=True)
            pdf.ln(5)
            pdf.multi_cell(0, 8, clean_for_pdf(f"Ingredients:\n{res.get('ingredients')}"))
            pdf.ln(5)

            pdf.cell(0, 10, "Breakdown:", ln=True)
            for c in res.get("categories", []):
                pdf.cell(0, 8, clean_for_pdf(f"- {c['name']} ({c['category']}, impact {c['impact']})"), ln=True)

            pdf.ln(5)
            pdf.multi_cell(0, 8, clean_for_pdf(f"Explanation:\n{res.get('analysis')}"))

            file_path = "nutrisense_report.pdf"
            pdf.output(file_path)

            with open(file_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name="nutrisense_report.pdf", mime="application/pdf")
