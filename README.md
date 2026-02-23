# 🥗 NutriSense AI

**AI-powered food ingredient intelligence — from the universe to your plate 🌌**

NutriSense AI is a full-stack AI application that analyzes food ingredient labels from images or text and converts them into clear, understandable health insights. It helps users understand what they’re eating by categorizing ingredients, computing a health score, highlighting risks, and generating explainable reports.

---

## 🚀 Features

- 📷 Upload a food label image (OCR powered)
- ✍️ Paste ingredients manually
- 🧠 AI-based ingredient normalization & understanding
- 🧪 Automatic ingredient categorization:
  - Sugar
  - Fats
  - Additives
  - Others
- 📊 Health scoring with labels (Good / Moderate / Poor)
- 👥 Highlights who should be cautious (allergies, sugar intake, etc.)
- 📜 Per-user scan history
- 📄 Downloadable PDF reports
- 🎨 Hackathon-ready futuristic UI

---

## 🧠 How It Works

1. **Image/Text Input**  
   User uploads an image or pastes ingredients.

2. **OCR & Cleaning**  
   Tesseract extracts text and fixes OCR errors like `sug ugar → sugar`.

3. **Ingredient Intelligence**

   - Deduplicates ingredients
   - Categorizes them (sugar, fat, additive, etc.)
   - Assigns impact weights

4. **Health Scoring**
   A weighted algorithm converts ingredient impact into a health score.

5. **AI Explanation**
   LLM generates a human-friendly explanation of the product.

6. **Storage & Reporting**
   - Saves scan history per user
   - Generates PDF reports on demand

---

## 🏗️ Tech Stack

### Frontend

- Streamlit
- Inline CSS (Glassmorphism + Neon theme)
- FPDF for report generation

### Backend

- FastAPI
- Tesseract OCR
- Custom ingredient reasoning engine
- Optional LLM for explanation

### Data

- JSON-based history storage
- Session-based user identification

---

## 📂 Project Structure

```
NutriSense AI/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── reasoning.py
│   │   │   └── history.py
│   │   ├── services/
│   │   │   ├── vision.py
│   │   │   └── llm.py
│   │   ├── routes/
│   │   │   └── analyze.py
│   │   └── main.py
│   └── history/
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/nutrisense-ai.git
cd nutrisense-ai
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 5️⃣ Run frontend

```bash
cd ../frontend
streamlit run app.py
```

---

## 🎯 Use Cases

- Health-conscious consumers
- People managing sugar intake
- Parents choosing packaged food
- Fitness & nutrition enthusiasts
- Allergy-sensitive individuals

---

## 🏆 Why NutriSense AI?

| Traditional Apps        | NutriSense AI            |
| ----------------------- | ------------------------ |
| Static nutrition labels | AI-powered understanding |
| Manual reading          | Image + OCR              |
| No explanations         | Transparent reasoning    |
| No history              | User scan tracking       |
| No reports              | PDF export               |

NutriSense AI focuses on **explainability**, not just prediction.

---

## 🌱 Future Enhancements

- Barcode scanning
- Country-specific ingredient regulations
- Personalized diet recommendations
- Nutrition goal tracking
- Mobile app integration
- Smart alerts (e.g., "High Sugar Warning")

---

## 🧩 Team & Credits

Built with ❤️ for hackathons, learning, and impact.

---

## 📜 License

MIT License — feel free to use, modify, and extend.

---

> _"NutriSense AI helps you understand what you eat — so you can choose what’s best for you."_
