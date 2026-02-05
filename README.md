# NLP Resume Screening & Job Match System (AI-Powered ATS)

An AI-powered Applicant Tracking System (ATS) that automatically extracts resume text, processes job descriptions, generates semantic embeddings using SBERT, and produces a match score.  
Includes a **User Panel** + **Admin Dashboard** + **SQLite Database Storage**.

---

## 🚀 Features

### ✔ User Panel
- Upload **multiple resumes (PDF/DOCX)**
- Upload or paste **Job Description (JD)**
- Automatic text extraction (PDF/DOCX)
- JD processing + skill extraction
- Text preprocessing (cleaning, lemmatization)
- SBERT-based semantic embeddings
- Cosine similarity scoring
- Final match percentage
- Batch scoring for multiple resumes
- Cleaned resume & JD view with insights

---

## 🔐 Admin Dashboard
- View all uploaded resumes
- View extracted fields:
  - Name
  - Email
  - Phone
  - Education
  - Experience
  - Projects
- Download original resumes
- View all Job Descriptions
- View JD extracted skills + role
- See match results history
- Score distribution chart
- Admin-only secure panel

---

## 🧠 Tech Stack

### Backend
- Python 3.x  
- SQLite3  
- SentenceTransformers  
- NumPy, Pandas  
- Scikit-learn  
- NLTK  
- spaCy  

### Frontend / UI
- Streamlit  
- Modular components system  

---

## 📁 Project Structure

```
NLP_Resume_Screening_JobMatch_System/
│
├── app/
│   ├── main.py
│   ├── admin_app.py
│   ├── components/
│   │   ├── upload_section.py
│   │   ├── result_section.py
│   │   └── sidebar.py
│   ├── services/
│   │   ├── resume_parser.py
│   │   ├── jd_parser.py
│   │   ├── preprocessor.py
│   │   ├── embedding_model.py
│   │   ├── similarity_engine.py
│   │   └── scoring_engine.py
│   ├── utils/
│   │   ├── database.py
│   │   ├── section_parser.py
│   │   ├── logger.py
│   │   ├── file_handler.py
│   │   └── constants.py
│   └── assets/
│
├── models/
│   ├── sbert/
│   └── spacy/
│
├── data/
│
├── tests/
├── notebooks/
├── requirements.txt
├── LICENSE
├── .gitignore
└── README.md
```

---

## ⚙ How It Works (Pipeline)

### **1️⃣ Resume Processing**
- Extract text from PDF/DOCX  
- Clean text (lowercase, remove symbols, stopwords, lemmatize)
- Resume section parsing (name, phone, email, education, experience, projects)
- Detect skills based on JD

### **2️⃣ JD Processing**
- Clean job description
- Extract skills & role
- Generate JD embedding

### **3️⃣ Matching Engine**
- Convert all resumes → SBERT embeddings  
- Calculate cosine similarity  
- Combine:
  - Semantic similarity  
  - Skill match score  
- Final weighted match score generated

### **4️⃣ Output**
- Resume-wise match score
- Resume name-wise ranking
- Cleaned text and details
- Admin can inspect everything

---

## 📦 Installation

### 1️⃣ Clone Repository
```
git clone https://github.com/<your-username>/<repo-name>.git
cd NLP_Resume_Screening_JobMatch_System
```

### 2️⃣ Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Run User Application
```
streamlit run app/main.py
```

### 5️⃣ Run Admin Dashboard
```
streamlit run app/admin_app.py
```

---

## 🗃 Database

SQLite DB auto-created at:

```
app/database/resume_system.db
```

Stores:
- resumes  
- job_descriptions  
- match_results  

---

## 🧪 Testing

Tests located in:

```
tests/
```

---

## 📜 License

MIT License — free for academic & personal use.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

---

## 👨‍💻 Author

**Abdullah**  
NLP | Data Science | AI Engineering  

---


