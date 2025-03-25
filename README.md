---
title: "News Summarizer Hindi TTS"
emoji: "📰"
colorFrom: "purple"
colorTo: "pink"
sdk: streamlit
sdk_version: "1.32.2"
app_file: streamlit_app.py
pinned: false
---

# 📰 News Summarizer with Hindi Text-to-Speech (TTS)

This is a Streamlit-based app that summarizes news about any company, performs sentiment analysis, and provides both text and Hindi audio versions of the summaries.

---

## ✅ Features

- 🔎 **Real-time News Extraction** using BeautifulSoup
- 📄 Summarizes at least 10 valid, unique news articles
- 📊 **Sentiment Analysis** (Positive / Neutral / Negative)
- 🧠 **Comparative Analysis** across articles
- 🌐 **Hindi Translation** using Google Translate
- 🔈 **Hindi Text-to-Speech** using gTTS
- 🎯 **Streamlit UI**
- 🔗 **API Integration** using FastAPI (optional for deployment)
- 🚀 **Deployable on Hugging Face Spaces**

---

## 🗂️ Project Structure

```
.
├── streamlit_app.py         # Main Streamlit frontend app
├── api.py                   # FastAPI backend (optional)
├── app.py                   # Entry point for FastAPI (used on HF Spaces)
├── utils.py                 # Utility functions for scraping, TTS, etc.
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation (this file)
```

---

## 📦 Installation

### 1. Clone the repository


```

### 2. Create and activate a virtual environment

#### On Windows:

```bash
python -m venv env
env\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install all dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Running Locally

### ➤ Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

### ➤ FastAPI Backend (Optional)

```bash
uvicorn api:app --reload
```

---


---

## 📝 Requirements Fulfilled

- ✅ Extracts & scrapes non-JavaScript pages using `BeautifulSoup`
- ✅ 10 valid articles minimum, or graceful fallback
- ✅ Sentiment analysis via NLTK VADER
- ✅ Summary + audio in Hindi using `googletrans` and `gTTS`
- ✅ Simple UI using Streamlit
- ✅ API endpoint available via FastAPI
- ✅ Hugging Face deployment-ready
- ✅ `README.md`, `requirements.txt`, and organized structure

---

## 📄 Sample Files to Include in Repo

Make sure your repo contains:

- `streamlit_app.py`
- `utils.py`
- `api.py`
- `app.py`
- `requirements.txt`
- `README.md`

---

## 📌 Dependencies (requirements.txt)

```txt
streamlit
gtts
googletrans==4.0.0-rc1
beautifulsoup4
requests
nltk
fastapi
uvicorn
```

---

## 🤝 Contributions

Feel free to fork and contribute. Pull requests are welcome!

---

## 💡 Author

Built by Vaibhav
Deployed on Hugging Face Spaces 🚀  
