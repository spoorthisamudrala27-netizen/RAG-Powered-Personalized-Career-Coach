# 🎯 RAG-Powered Next-Gen Career Coach & AI Interviewer

An advanced, interactive **Retrieval-Augmented Generation (RAG)** application built with **Streamlit** and powered locally by **Ollama (Llama 3.2)**. This application lets users upload their Resume or Syllabus PDFs to extract custom profiles, analyze skill gaps, generate multi-day learning roadmaps, simulate live mock interviews with real-time feedback, and map immediate or alternative career vectors.

---

## 🌟 Key Features

* **📄 Document Intelligence (RAG):** Upload any Resume, CV, or academic syllabus in PDF format. The app chunks, reads, and contextualizes text dynamically.
* **💡 Tab 1: Hyper-Personalized Career Guidance:** Get an instant skill gap analysis comparing your resume against your target job title. Features a structured 30-60-90 day learning blueprint.
* **🤖 Tab 2: AI Technical & Behavioral Mock Interview:** Generates 5 hard-hitting custom interview questions based directly on the tech stack found in your PDF. Includes an interactive evaluation sandbox that scores and corrects user answers out of 10.
* **💼 Tab 3: Dynamic Market Opportunity Mapping:** Explore immediate job roles you qualify for right now, long-term 5-year trajectories, and structural pivots into adjacent professional horizons.
* **🔒 100% Local & Secure:** Powered entirely by Ollama locally on your computer—no API keys or cloud configurations needed.

---

## 🛠️ Tech Stack

* **Frontend UI:** Streamlit
* **RAG Orchestration:** LangChain Ollama
* **PDF Parser:** pypdf
* **Vector Mechanics:** ChromaDB & LangChain Text Splitters
* **Local Inference Engine:** Ollama (Model: `llama3.2`)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.9 to 3.11** installed on your system. 

### 2. Install Dependencies
Open your terminal inside the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Set Up Ollama Local LLM
1. Download and install [Ollama](https://ollama.com).
2. Pull and start the required model in your terminal background:
   ```bash
   ollama run llama3.2
   ```
*(Keep this terminal active while running the application).*

### 4. Launch the Application
Start the Streamlit dashboard by running:
```bash
streamlit run app.py
```
Your browser will automatically launch and host the app interface at `http://localhost:8501`.

---

## 📂 Project Architecture

```text
├── app.py                # Main Streamlit Application Source Code
├── requirements.txt      # Python Project Dependency Formatures 
└── README.md             # Project Setup Guide & Specifications
```

---

## 💡 Troubleshooting Reference

* **ModuleNotFoundError (PyPDF2 vs pypdf):** The codebase leverages `pypdf`, which is the updated modern standard for parsing text chunks. Make sure your import states `from pypdf import PdfReader`.
* **Connection Error to Ollama:** If the application errors out stating it cannot communicate with the model, double check that your background command prompt running `ollama run llama3.2` is open and active.
