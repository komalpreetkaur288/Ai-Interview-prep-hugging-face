# AI Virtual Interview Preparation Platform
## Complete Project Documentation Report

---

## TABLE OF CONTENTS

1. [Project Synopsis](#1-project-synopsis)
2. [Project Overview](#2-project-overview)
3. [Technology Stack](#3-technology-stack)
4. [Project Architecture](#4-project-architecture)
5. [Directory Structure](#5-directory-structure)
6. [Database Design](#6-database-design)
7. [Authentication & Authorization](#7-authentication--authorization)
8. [Resume Parsing Logic](#8-resume-parsing-logic)
9. [Question Generation Logic](#9-question-generation-logic)
10. [Scoring & Evaluation Logic](#10-scoring--evaluation-logic)
11. [Speech Services (STT & TTS)](#11-speech-services-stt--tts)
12. [Face Detection System](#12-face-detection-system)
13. [API Endpoints Reference](#13-api-endpoints-reference)
14. [Frontend Pages & Components](#14-frontend-pages--components)
15. [Complete Data Flow](#15-complete-data-flow)
16. [AI/LLM Integration Details](#16-aillm-integration-details)
17. [Session Management](#17-session-management)
18. [Error Handling & Fallback Mechanisms](#18-error-handling--fallback-mechanisms)
19. [Security Considerations](#19-security-considerations)
20. [Deployment & Configuration](#20-deployment--configuration)

---

## 1. PROJECT SYNOPSIS

### Title
**AI-Powered Virtual Interview Preparation System**

### Abstract
This project is a web-based AI-powered interview preparation platform designed to help job seekers practice and improve their interview performance. The system simulates a real interview environment by analyzing the candidate's resume, generating personalized technical questions using a Large Language Model (LLM), evaluating answers using Natural Language Processing (NLP), and providing detailed feedback with scores.

### Problem Statement
Job seekers often struggle with interview preparation due to:
- Lack of personalized practice questions tailored to their specific skills and experience
- No real-time feedback on answer quality
- Absence of simulated interview conditions (time pressure, camera presence)
- Generic practice resources that don't match individual backgrounds

### Proposed Solution
An intelligent web application that:
1. Parses the candidate's resume and extracts their skills and experience
2. Uses an LLM (Groq's LLaMA model) to generate personalized, resume-specific interview questions
3. Provides a realistic interview experience with a 60-second timer per question, camera monitoring, and speech-to-text input
4. Evaluates answers using TF-IDF cosine similarity against ideal answers
5. Generates a detailed score report with feedback and correct answers for learning

### Key Features
- Resume-based personalized question generation using AI
- Speech-to-text answer recording via Deepgram API
- Text-to-speech question reading via Google TTS
- Face detection to simulate real interview presence requirements
- Automated answer evaluation using ML (TF-IDF + Cosine Similarity)
- Detailed performance report with ideal answers and improvement feedback
- Topic-based interviews (15+ technical topics) without resume upload
- Session history tracking for progress monitoring

### Objectives
1. Build an intelligent system that generates interview questions from any uploaded resume
2. Create a realistic interview simulation with timing and camera constraints
3. Implement NLP-based answer evaluation to provide objective feedback
4. Help candidates identify knowledge gaps through ideal answer comparison
5. Track improvement over multiple interview sessions

### Scope
- **Users:** College students and job seekers preparing for technical interviews
- **Domains Covered:** Python, Java, JavaScript, SQL, Machine Learning, Data Science, HR/Behavioral
- **Platform:** Web application (desktop browser focused)
- **Access:** Login-based with user accounts

---

## 2. PROJECT OVERVIEW

### What the Application Does

The AI Virtual Interview Platform is a full-stack web application built with Python Flask on the backend and HTML/CSS/Vanilla JavaScript on the frontend. It follows a step-by-step interview workflow:

```
REGISTER / LOGIN → UPLOAD RESUME → CAMERA CHECK → INTERVIEW → RESULTS
```

**Step 1: Registration & Login**
Users create an account with a username and password. Passwords are securely hashed before storage.

**Step 2: Resume Upload**
Users upload their resume as a PDF file. The system:
- Extracts text from the PDF using PyPDF2
- Identifies technical skills from the extracted text (70+ skill keywords)
- Calls the Groq API (LLaMA model) to generate 8 personalized interview questions
- Stores questions with ideal answers in the database

**Step 3: Dashboard**
The dashboard shows:
- Detected skills from the resume
- Option to start a resume-based or topic-based interview
- History of past interview sessions with scores

**Step 4: Camera Check (Interview Ready Page)**
Before the interview begins, the system verifies:
- Camera is accessible and active
- Candidate's face is visible and detectable

**Step 5: Interview**
For each question (up to 8 questions):
- Question is displayed and optionally read aloud via TTS
- Candidate has 60 seconds to answer
- Answer can be typed OR spoken (real-time transcription via Deepgram STT)
- Timer auto-submits the answer when time expires
- Answer is saved and evaluated immediately

**Step 6: Results**
After all questions are answered:
- Overall score out of 10 is displayed with color-coded performance rating
- Each question shows: user's answer, ideal answer, individual score, and feedback
- Options to retry or return to dashboard

---

## 3. TECHNOLOGY STACK

### Backend Technologies

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python 3 | 3.8+ | Primary backend programming language |
| Flask | Latest | Web framework for routing, request handling, templating |
| Flask-Login | Latest | User session management and authentication |
| Werkzeug | Latest | Password hashing (PBKDF2-SHA256) |
| SQLite | Built-in | Relational database for data persistence |
| scikit-learn | Latest | TF-IDF vectorization and cosine similarity for answer evaluation |
| PyPDF2 | Latest | PDF text extraction from uploaded resumes |
| gTTS | Latest | Google Text-to-Speech for reading questions aloud |
| python-dotenv | Latest | Environment variable management |
| requests | Latest | HTTP requests to external APIs |
| groq | Latest | Official Groq Python SDK for LLaMA API calls |

### Frontend Technologies

| Technology | Purpose |
|-----------|---------|
| HTML5 | Page structure and semantic markup |
| CSS3 | Styling, animations, responsive design |
| Vanilla JavaScript (ES6+) | Client-side interactivity and API calls |
| RecordRTC | Browser-based audio recording library |
| face-api.js | Client-side face detection using TensorFlow.js |
| FaceDetector API | Native browser face detection (with face-api.js fallback) |
| WebSocket API | Real-time communication with Deepgram STT |
| Fetch API | AJAX calls to backend endpoints |

### External APIs & Services

| Service | Purpose | API Type |
|---------|---------|---------|
| Groq API (LLaMA 3.1 8B Instant) | Resume-based question generation | REST |
| Deepgram API | Speech-to-text transcription | REST & WebSocket |
| Google TTS (gTTS) | Text-to-speech for questions | Library |

### Development Tools
- **Database:** SQLite (file-based, `database.db`)
- **Environment:** `.env` file for API keys
- **Version Control:** Git (not actively used in current state)

---

## 4. PROJECT ARCHITECTURE

### Architectural Pattern
The application follows the **MVC (Model-View-Controller)** pattern:

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND (View)                   │
│  HTML Templates + CSS + JavaScript                   │
│  login.html, dashboard.html, interview.html, etc.    │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP Requests
┌──────────────────────▼──────────────────────────────┐
│                  FLASK APP (Controller)              │
│  app.py - Routes, Request Handling, Business Logic   │
└──────┬──────────┬────────────┬──────────────────────┘
       │          │            │
┌──────▼──┐  ┌───▼─────┐  ┌──▼──────────────────────┐
│  utils/ │  │Templates│  │     External Services    │
│ auth.py │  │ Jinja2  │  │  Groq API (LLaMA 3.1)    │
│ db.py   │  │ Engine  │  │  Deepgram STT API        │
│ resume  │  └─────────┘  │  Google TTS              │
│ _parser │               └──────────────────────────┘
│ question│
│_generato│
│ ml_model│
└──────┬──┘
       │
┌──────▼──────────────────────────────────────────────┐
│                  DATABASE (Model)                   │
│  SQLite: users, interviews, resume_questions tables │
└─────────────────────────────────────────────────────┘
```

### Request-Response Cycle
```
User Browser
    │
    │ 1. HTTP Request (GET/POST)
    ▼
Flask Router (app.py)
    │
    │ 2. Route Handler Executes
    │    - Checks @login_required
    │    - Reads/writes database via db.py
    │    - Calls utility functions (resume_parser, question_generator, ml_model)
    │    - Makes external API calls (Groq, Deepgram)
    │
    │ 3. Render Template or Return JSON
    ▼
Jinja2 Template Engine
    │
    │ 4. HTML Response with Dynamic Data
    ▼
User Browser
    │
    │ 5. JavaScript enhances UI (RecordRTC, face-api, WebSocket)
    ▼
API Callbacks (/api/transcribe, /api/tts)
```

---

## 5. DIRECTORY STRUCTURE

```
interview-AI/
│
├── app.py                      # Main Flask application (359 lines)
│                               # All route definitions and business logic
│
├── requirements.txt            # Python package dependencies
│
├── .env                        # Environment variables (API keys)
│                               # DEEPGRAM_API_KEY, GROQ_API_KEY
│
├── database.db                 # SQLite database file
│                               # Auto-created on first run
│
├── README.md                   # Basic project description
│
├── Project_Synopsis.docx       # Project synopsis document
│
├── utils/                      # Backend utility modules
│   ├── __init__.py            # Package marker (empty)
│   ├── auth.py                # User authentication (22 lines)
│   │                          # Flask-Login user class, DB user lookups
│   ├── db.py                  # Database setup (62 lines)
│   │                          # SQLite connection, table creation
│   ├── resume_parser.py       # PDF parsing (34 lines)
│   │                          # PyPDF2 extraction, skill detection
│   ├── question_generator.py  # Question logic (227 lines)
│   │                          # Static Q&A database + Groq AI integration
│   └── ml_model.py            # Answer evaluation (34 lines)
│                               # TF-IDF + cosine similarity scoring
│
├── templates/                  # Jinja2 HTML templates
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main user dashboard
│   ├── upload_resume.html     # Resume upload with drag & drop
│   ├── interview_ready.html   # Pre-interview camera verification
│   ├── interview.html         # Live interview question page
│   └── result.html            # Score report and feedback page
│
└── static/                     # Static assets
    └── style.css              # Global CSS styles (300+ lines)
```

---

## 6. DATABASE DESIGN

### Database: SQLite (`database.db`)
The application uses three tables managed through `utils/db.py`.

---

### Table 1: `users`
Stores registered user accounts.

```sql
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| username | TEXT | UNIQUE, NOT NULL | User's login name |
| password | TEXT | NOT NULL | Werkzeug-hashed password (PBKDF2-SHA256) |

**Notes:**
- Passwords are NEVER stored in plaintext
- A default `admin/admin123` account is created on first initialization
- Username uniqueness is enforced at database level

---

### Table 2: `interviews`
Stores each question-answer record from every interview session.

```sql
CREATE TABLE IF NOT EXISTS interviews (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    question   TEXT,
    answer     TEXT,
    score      REAL,
    feedback   TEXT,
    session_id TEXT,
    ideal_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-incremented record ID |
| user_id | INTEGER | Foreign key linking to users table |
| question | TEXT | The interview question asked |
| answer | TEXT | The candidate's actual answer (or "SKIPPED") |
| score | REAL | Float score 0.0–10.0 from TF-IDF evaluation |
| feedback | TEXT | Textual feedback ("Good answer", "Needs improvement", etc.) |
| session_id | TEXT | UUID grouping all answers from one interview session |
| ideal_answer | TEXT | The correct/model answer for comparison |
| created_at | TIMESTAMP | Auto-set to current timestamp on insert |

**Notes:**
- One row is created per question per interview session
- `session_id` is a UUID4 generated at interview start, used to group and retrieve results
- Skipped questions get score=0 and feedback="Question skipped"

---

### Table 3: `resume_questions`
Stores AI-generated questions derived from the user's uploaded resume.

```sql
CREATE TABLE IF NOT EXISTS resume_questions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    question     TEXT NOT NULL,
    ideal_answer TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-incremented record ID |
| user_id | INTEGER | Foreign key linking to users table |
| question | TEXT | The AI-generated interview question |
| ideal_answer | TEXT | Key points / model answer from AI |
| created_at | TIMESTAMP | When the question was generated |

**Notes:**
- Existing resume questions for a user are DELETED and replaced each time a new resume is uploaded
- Questions are loaded from this table when a user starts a resume-based interview

---

### Entity-Relationship Diagram

```
users (1) ──────── (N) interviews
  │
  └──────────────── (N) resume_questions

users.id = interviews.user_id
users.id = resume_questions.user_id
```

---

### Database Connection (`utils/db.py`)

```python
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Rows accessible as dictionaries
    return conn
```

- `sqlite3.Row` factory allows column access by name: `row['username']`
- Connection is opened per request (not pooled — appropriate for SQLite)
- `init_db()` is called at app startup to create tables if they don't exist

---

## 7. AUTHENTICATION & AUTHORIZATION

### Technology Used
- **Flask-Login** for session management
- **Werkzeug Security** for password hashing

### User Class (`utils/auth.py`)

```python
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username
```

`UserMixin` provides default implementations for:
- `is_authenticated` → True if user is logged in
- `is_active` → True (all users are active)
- `is_anonymous` → False for logged-in users
- `get_id()` → Returns `str(self.id)` for session storage

### Registration Flow

```
User fills registration form
    ↓
POST /register
    ↓
Check if username already exists in DB
    ↓ (if exists)
Flash "Username already exists" → Redirect to /register
    ↓ (if new)
Hash password with generate_password_hash()
    ↓
INSERT INTO users (username, password) VALUES (?, ?)
    ↓
Redirect to / (login page) with success message
```

### Login Flow

```
User fills login form
    ↓
POST /
    ↓
SELECT user WHERE username = ?
    ↓ (not found)
Flash "Invalid credentials" → Reload form
    ↓ (found)
check_password_hash(stored_hash, entered_password)
    ↓ (mismatch)
Flash "Invalid credentials" → Reload form
    ↓ (match)
login_user(User object)  ← Flask-Login sets session cookie
    ↓
Redirect to /dashboard
```

### Route Protection
All protected routes use the `@login_required` decorator:

```python
@app.route('/dashboard')
@login_required
def dashboard():
    ...
```

Unauthenticated users are redirected to the login page automatically.

### Password Hashing Algorithm
Werkzeug uses **PBKDF2-HMAC-SHA256** with a random salt:
- Input: plaintext password
- Output: `pbkdf2:sha256:260000$<salt>$<hash>` (stored in DB)
- Verification: `check_password_hash(stored, input)` — timing-safe comparison

---

## 8. RESUME PARSING LOGIC

**File:** `utils/resume_parser.py`

### Overview
The resume parser extracts text from PDF files and identifies technical skills mentioned in the resume.

### Function 1: `extract_text_from_pdf(file_bytes)`

```python
def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
```

**How It Works:**
1. Receives the raw bytes of the uploaded PDF file
2. Wraps bytes in `io.BytesIO` to create a file-like object (no disk write needed)
3. `PdfReader` parses the PDF structure
4. Iterates through every page and extracts text content
5. Concatenates all page text into one string
6. Returns the full resume text

**Limitations:**
- Only works with text-based PDFs (not scanned images)
- Complex formatting (tables, columns) may extract in unexpected order
- PyPDF2 may struggle with some PDF encodings

---

### Function 2: `extract_skills(text)`

**Complete Skill Keyword List:**
```python
SKILL_KEYWORDS = [
    "python", "java", "javascript", "c++", "c#", "sql", "mysql", "postgresql",
    "mongodb", "html", "css", "react", "angular", "vue", "node", "django",
    "flask", "spring", "machine learning", "deep learning", "nlp", "tensorflow",
    "keras", "scikit-learn", "pandas", "numpy", "matplotlib", "git", "github",
    "docker", "kubernetes", "aws", "azure", "gcp", "linux", "agile", "scrum",
    "rest api", "graphql", "php", "ruby", "swift", "kotlin", "android", "ios",
    "excel", "tableau", "power bi", "r", "scala", "hadoop", "spark", "hive",
    "elasticsearch", "redis", "kafka", "microservices", "devops", "ci/cd",
    "selenium", "junit", "pytest", "maven", "gradle", "jenkins"
]
```

**Algorithm:**
```python
def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found_skills.append(skill.title())
    return list(set(found_skills))  # Remove duplicates
```

1. Converts entire resume text to lowercase for case-insensitive matching
2. Checks if each keyword is a substring anywhere in the text
3. Returns title-cased unique skills (e.g., "python" → "Python")

**Limitation:** Simple substring matching — "Java" would also match "JavaScript". More robust parsing would use word boundaries.

---

### Function 3: `generate_summary(text)`

```python
def generate_summary(text):
    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 30]
    return ' | '.join(lines[:3]) if lines else "No summary available"
```

1. Splits text by newline
2. Strips whitespace from each line
3. Keeps only lines longer than 30 characters (filters headers/short labels)
4. Returns the first 3 such lines joined with ` | `

**Purpose:** Creates a brief readable summary for display on the interview-ready page.

---

### Resume Upload Flow in `app.py`

```python
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['resume']
        # 1. Validate file type
        if not file.filename.endswith('.pdf'):
            flash('Please upload a PDF file')
            return redirect(url_for('upload'))
        
        # 2. Extract text from PDF
        file_bytes = file.read()
        resume_text = extract_text_from_pdf(file_bytes)
        
        # 3. Extract skills
        skills = extract_skills(resume_text)
        
        # 4. Generate summary
        summary = generate_summary(resume_text)
        
        # 5. Generate AI questions
        qa_pairs = generate_questions_from_resume(resume_text)
        
        # 6. Save to database (delete old, insert new)
        db.execute('DELETE FROM resume_questions WHERE user_id = ?', [current_user.id])
        for item in qa_pairs:
            db.execute('INSERT INTO resume_questions (user_id, question, ideal_answer) VALUES (?,?,?)',
                      [current_user.id, item['q'], item['a']])
        
        # 7. Store in session
        session['skills'] = skills
        session['resume_summary'] = summary
        
        return redirect(url_for('dashboard'))
```

---

## 9. QUESTION GENERATION LOGIC

**File:** `utils/question_generator.py`

### Overview
Two modes of question generation are available:

1. **AI-Powered (Resume-Based):** Uses Groq API with LLaMA model to generate personalized questions from resume text
2. **Static (Topic-Based):** Serves pre-written Q&A pairs from a built-in database of 15+ topics

---

### Static Question Database

The file contains `TOPIC_QUESTIONS` — a dictionary mapping topic names to lists of Q&A pairs.

**Topics Covered:**
- `python` — 14 questions (data structures, OOP, generators, decorators, etc.)
- `java` — 10 questions (JVM, OOP concepts, collections, multithreading)
- `javascript` — 10 questions (closures, promises, event loop, ES6+)
- `sql` — 10 questions (joins, normalization, indexes, transactions)
- `data science` — 10 questions (statistics, EDA, feature engineering)
- `machine learning` — 10 questions (algorithms, overfitting, validation)
- `hr` — 8 questions (behavioral, strengths/weaknesses, teamwork)

**Example Question Entry:**
```python
TOPIC_QUESTIONS = {
    "python": [
        {
            "q": "What are Python decorators and how do you use them?",
            "a": "Decorators are functions that modify the behavior of other functions..."
        },
        ...
    ]
}
```

---

### Skill-to-Topic Mapping

```python
SKILL_TO_TOPIC = {
    "python": "python",
    "java": "java",
    "javascript": "javascript",
    "js": "javascript",
    "react": "javascript",
    "angular": "javascript",
    "node": "javascript",
    "sql": "sql",
    "mysql": "sql",
    "postgresql": "sql",
    "machine learning": "machine learning",
    "deep learning": "machine learning",
    "data science": "data science",
    "pandas": "data science",
    "numpy": "data science",
}
```

This dictionary maps detected skill keywords to the appropriate topic category in `TOPIC_QUESTIONS`.

---

### Function 1: `generate_questions_from_resume(resume_text, num_questions=8)`

This is the **primary AI-powered question generation function**.

**Implementation:**

```python
def generate_questions_from_resume(resume_text, num_questions=8):
    if not GROQ_API_KEY:
        return get_questions_for_skills(extract_skills_simple(resume_text))
    
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    Analyze this resume and generate {num_questions} personalized interview questions.
    
    IMPORTANT RULES:
    - Questions must be STRICTLY based on what's explicitly written in the resume
    - Do NOT generate generic behavioral questions
    - Each question should directly reference specific skills, projects, or experience
    - Include key points for ideal answers
    
    Resume (first 5000 chars):
    {resume_text[:5000]}
    
    Respond ONLY in this JSON format:
    {{
        "skills": ["skill1", "skill2", ...],
        "questions": [
            {{"q": "specific question", "a": "key points for ideal answer"}},
            ...
        ]
    }}
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a JSON generating assistant that outputs only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.5,
        max_tokens=2000
    )
    
    data = json.loads(response.choices[0].message.content)
    questions = data.get("questions", [])
    
    # Validate: need at least 3 questions
    if len(questions) < 3:
        raise ValueError("Not enough questions")
    
    return questions
```

**Key Design Decisions:**
- `resume_text[:5000]` — Limits input to 5000 chars to manage API cost and latency
- `temperature=0.5` — Balanced between creative and deterministic output
- `response_format={"type": "json_object"}` — Forces Groq to return valid JSON
- System prompt sets the model role explicitly for consistent JSON behavior
- Minimum 3 questions threshold before falling back to static questions

---

### Function 2: `get_questions_for_skills(skills, count=8)`

**Fallback function** used when Groq API is unavailable or fails.

```python
def get_questions_for_skills(skills, count=8):
    questions = []
    seen_topics = set()
    
    for skill in skills:
        skill_lower = skill.lower()
        topic = SKILL_TO_TOPIC.get(skill_lower)
        
        if topic and topic not in seen_topics:
            seen_topics.add(topic)
            topic_questions = TOPIC_QUESTIONS.get(topic, [])
            # Take 2 questions per skill topic
            sample = random.sample(topic_questions, min(2, len(topic_questions)))
            questions.extend(sample)
    
    # Always add 2 HR questions
    hr_questions = TOPIC_QUESTIONS.get("hr", [])
    questions.extend(random.sample(hr_questions, min(2, len(hr_questions))))
    
    # Shuffle to mix topics
    random.shuffle(questions)
    
    return questions[:count]
```

**Logic:**
1. Iterates through detected skills
2. Maps each skill to a topic using `SKILL_TO_TOPIC`
3. Avoids duplicate topics (one set of questions per topic)
4. Samples 2 random questions per unique topic
5. Always appends 2 HR/behavioral questions
6. Shuffles the final list
7. Returns at most `count` questions (default 8)

---

### Function 3: `get_questions_for_topic(topic, count=5)`

Used when the user selects a specific topic from the dashboard dropdown.

```python
def get_questions_for_topic(topic, count=5):
    topic_lower = topic.lower()
    questions = TOPIC_QUESTIONS.get(topic_lower, TOPIC_QUESTIONS.get("hr", []))
    return random.sample(questions, min(count, len(questions)))
```

- Accepts any topic name (case-insensitive)
- Defaults to HR questions if topic not found
- Returns random sample of the requested count

---

### Question Generation Decision Tree

```
User clicks "Start Interview"
         │
         ├─── Resume-based?
         │         │
         │         └─── Load from resume_questions table (DB)
         │                   │
         │                   └─── AI questions stored here
         │
         └─── Topic-based?
                   │
                   └─── get_questions_for_topic(selected_topic)
                             │
                             └─── Random sample from TOPIC_QUESTIONS dict

At Upload Time (AI question generation):
         │
         └─── generate_questions_from_resume()
                   │
                   ├─── GROQ_API_KEY exists? 
                   │         │
                   │         └─── Call Groq API → Parse JSON → Validate ≥3 questions
                   │
                   └─── API fails / key missing / <3 questions?
                             │
                             └─── get_questions_for_skills(detected_skills)
                                       │
                                       └─── Map skills → topics → sample 2 per topic
                                                 + 2 HR questions always added
```

---

## 10. SCORING & EVALUATION LOGIC

**File:** `utils/ml_model.py`

### Overview
The answer evaluation system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization combined with **Cosine Similarity** to measure how semantically similar the candidate's answer is to the ideal answer.

### Core Algorithm: `evaluate_answer(user_answer, ideal_answer)`

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_answer(user_answer, ideal_answer):
    # Step 1: Handle skipped/empty answers
    if not user_answer or user_answer.strip() == "" or user_answer == "SKIPPED":
        return 0, "Question skipped"
    
    # Step 2: Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_answer, ideal_answer])
    
    # Step 3: Compute cosine similarity
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    # Step 4: Scale to 0-10
    score = round(similarity * 10, 2)
    
    # Step 5: Generate feedback
    if score >= 7.0:
        feedback = "Good answer! Well explained."
    elif score >= 4.0:
        feedback = "Average answer. Try to add more detail."
    else:
        feedback = "Needs improvement. Study this topic more."
    
    return score, feedback
```

---

### Understanding TF-IDF

**TF (Term Frequency):**
- Measures how often a term appears in a document
- Formula: `TF(t, d) = count(t in d) / total_terms(d)`
- Higher frequency → higher weight for that document

**IDF (Inverse Document Frequency):**
- Measures how rare or common a term is across all documents
- Formula: `IDF(t) = log(N / count(documents containing t))`
- Common words ("the", "is", "a") get low IDF weights
- Rare, specific words get high IDF weights

**TF-IDF = TF × IDF:**
- Words that appear frequently in the answer but rarely in general → high score
- Stop words like "the", "and" → low scores (naturally filtered)
- Technical terms unique to the topic → high scores

**In this application:**
- The "corpus" is just 2 documents: user_answer and ideal_answer
- The vectorizer learns vocabulary from both texts
- Each word becomes a feature dimension
- Each document becomes a vector of TF-IDF weights

---

### Understanding Cosine Similarity

Cosine similarity measures the angle between two vectors, not their magnitude:

```
                  A · B
similarity = ─────────────
              ||A|| × ||B||

Where:
  A · B = dot product of vectors A and B
  ||A|| = magnitude (length) of vector A
  ||B|| = magnitude (length) of vector B
```

**Why Cosine?**
- A longer answer isn't necessarily better — cosine normalizes for length
- Focuses on the direction (topic alignment) rather than quantity
- Range: 0 (completely different topics) to 1 (same words, same proportions)

**Example:**
- Ideal: "Python uses indentation for code blocks and is interpreted"
- User: "Python is interpreted and uses indentation"
- Result: ~0.85+ similarity (same keywords, same topic)

---

### Scoring Scale

| Cosine Similarity | Score (×10) | Feedback |
|------------------|-------------|---------|
| 0.70 – 1.00 | 7.0 – 10.0 | "Good answer! Well explained." |
| 0.40 – 0.69 | 4.0 – 6.9 | "Average answer. Try to add more detail." |
| 0.00 – 0.39 | 0.0 – 3.9 | "Needs improvement. Study this topic more." |
| Skipped | 0 | "Question skipped" |

---

### Results Interpretation on Dashboard

| Percentage (Total Score / Max Score × 100) | Rating | Color |
|---------------------------------------------|--------|-------|
| ≥ 70% | Excellent | Green |
| 40% – 69% | Average | Yellow/Orange |
| < 40% | Needs Work | Red |

**Example Calculation:**
- 8 questions, max possible = 80 (8 × 10)
- Total score = 45.5
- Percentage = 45.5 / 80 × 100 = 56.9% → "Average" rating

---

### Keyword Extraction: `extract_keywords(text)`

```python
def extract_keywords(text, top_n=15):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out().tolist()
```

- Uses TF-IDF to find the most distinctive words in any text
- Automatically removes English stop words
- Returns top 15 keywords by TF-IDF score
- **Note:** This function exists in the codebase but is not currently called in the main interview flow

---

### Evaluation Submission in `app.py` (`/submit` route)

```python
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    answer = request.form.get('answer', '').strip()
    questions = session.get('interview_questions', [])
    index = session.get('interview_index', 0)
    session_id = session.get('session_id')
    
    current_q = questions[index]
    question_text = current_q.get('q', '')
    ideal_answer = current_q.get('a', '')
    
    # Evaluate the answer
    score, feedback = evaluate_answer(answer, ideal_answer)
    
    # Store result in database
    db.execute('''
        INSERT INTO interviews (user_id, question, answer, score, feedback, session_id, ideal_answer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [current_user.id, question_text, answer or "SKIPPED", score, feedback, session_id, ideal_answer])
    
    # Move to next question
    session['interview_index'] = index + 1
    
    if index + 1 >= len(questions):
        return redirect(url_for('result'))
    return redirect(url_for('interview'))
```

---

## 11. SPEECH SERVICES (STT & TTS)

### Speech-to-Text (STT) — Deepgram API

**Route:** `POST /api/transcribe`

**Frontend Flow:**
1. User clicks "Speak Answer" button
2. `RecordRTC` starts recording audio from microphone
3. Audio is recorded as `audio/webm;codecs=opus` format
4. User clicks "Stop Recording"
5. JavaScript sends audio blob via `fetch()` to `/api/transcribe`
6. Transcribed text is inserted into the answer textarea

**Backend Implementation:**

```python
@app.route('/api/transcribe', methods=['POST'])
@login_required
def transcribe():
    audio_file = request.files.get('audio')
    audio_bytes = audio_file.read()
    
    # Validate audio is not empty/silent
    if len(audio_bytes) < 500:
        return jsonify({"transcript": "", "error": "Audio too short"}), 400
    
    # Send to Deepgram REST API
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/webm"
    }
    response = requests.post(
        "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true",
        headers=headers,
        data=audio_bytes
    )
    
    result = response.json()
    transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
    return jsonify({"transcript": transcript})
```

**Deepgram API Parameters:**
- `model=nova-2` — Deepgram's highest accuracy English model
- `smart_format=true` — Adds punctuation, capitalization, and formatting
- Audio format: `audio/webm` (browser native recording format)

**Real-time Alternative (WebSocket):**
The frontend also attempts Deepgram WebSocket connection for real-time streaming transcription. If WebSocket connection fails, it falls back to the REST API batch transcription.

---

### Text-to-Speech (TTS) — gTTS

**Route:** `GET /api/tts?text=<question_text>`

**Implementation:**

```python
@app.route('/api/tts')
@login_required  
def tts():
    text = request.args.get('text', '')
    
    # Generate speech with Google TTS
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save to in-memory buffer
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    
    return send_file(audio_buffer, mimetype='audio/mpeg')
```

**Frontend Usage:**
```javascript
// User clicks 🔊 speak button
async function speakQuestion(text) {
    const response = await fetch(`/api/tts?text=${encodeURIComponent(text)}`);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play();
}
```

- No caching of audio files — generated fresh per request
- `slow=False` — Normal speech speed
- `lang='en'` — English language
- Returns MP3 blob directly to browser

---

## 12. FACE DETECTION SYSTEM

**Page:** `interview_ready.html`

### Purpose
Ensures the candidate is physically present and visible before starting the interview. Simulates the requirement in real video interviews.

### Primary: FaceDetector API (Native Browser)

```javascript
if ('FaceDetector' in window) {
    const faceDetector = new FaceDetector({ fastMode: true });
    
    async function detectFace() {
        const faces = await faceDetector.detect(videoElement);
        if (faces.length > 0) {
            consecutiveDetections++;
            if (consecutiveDetections >= 3) {
                // Face confirmed! Enable start button.
                faceDetected = true;
            }
        } else {
            consecutiveDetections = 0;
        }
    }
    
    setInterval(detectFace, 1000); // Check every second
}
```

### Fallback: face-api.js

```javascript
// If FaceDetector API not available (Firefox, older Chrome):
await faceapi.nets.tinyFaceDetector.loadFromUri('/static/models');

async function detectFaceWithFaceAPI() {
    const detections = await faceapi.detectAllFaces(
        videoElement, 
        new faceapi.TinyFaceDetectorOptions()
    );
    // Same consecutive detection logic
}
```

### Detection Threshold Logic

```
Start camera
    │
    └── Check for face every 1 second
            │
            ├── Face detected?
            │       │
            │       └── YES → consecutiveDetections++
            │               │
            │               └── consecutiveDetections >= 3?
            │                       │
            │                       └── YES → Mark face as confirmed
            │                                 Enable "Start Interview" button
            │
            └── NO face → Reset consecutiveDetections = 0
```

**Why 3 consecutive detections?**
- Prevents false positives from a single frame
- Requires ~3 seconds of stable face presence
- Balances between quick verification and accuracy

### Camera Requirements Display

The page shows a checklist:
- ✅ / ❌ Camera is ON
- ✅ / ❌ Face detected

The "Start Interview" button remains **disabled** until BOTH requirements are met.

---

## 13. API ENDPOINTS REFERENCE

### Page Routes

| Route | Method | Auth Required | Description |
|-------|--------|--------------|-------------|
| `/` | GET | No | Login page display |
| `/` | POST | No | Login form submission |
| `/register` | GET | No | Registration page display |
| `/register` | POST | No | Registration form submission |
| `/logout` | GET | Yes | Logout and clear session |
| `/dashboard` | GET | Yes | Main dashboard |
| `/upload` | GET | Yes | Resume upload page |
| `/upload` | POST | Yes | Process uploaded PDF |
| `/interview-ready` | GET | Yes | Camera verification page |
| `/start` | GET | Yes | Initialize interview session |
| `/start` | POST | Yes | Submit topic selection, initialize interview |
| `/interview` | GET | Yes | Display current question |
| `/submit` | POST | Yes | Submit answer, evaluate, next question |
| `/cancel` | GET | Yes | Cancel interview, clear session |
| `/result` | GET | Yes | Display final results |

### API Routes

| Route | Method | Auth Required | Request | Response |
|-------|--------|--------------|---------|---------|
| `/api/transcribe` | POST | Yes | `multipart/form-data` with `audio` file | `{"transcript": "string"}` |
| `/api/tts` | GET | Yes | Query param `?text=` | `audio/mpeg` blob |

---

## 14. FRONTEND PAGES & COMPONENTS

### Page 1: Login (`login.html`)
**Purpose:** User authentication entry point

**Elements:**
- Username text input
- Password input (masked)
- Login button
- "Register here" link
- Flash messages for errors

**Behavior:**
- Form POST to `/`
- Errors shown via Flask flash messages

---

### Page 2: Register (`register.html`)
**Purpose:** New account creation

**Elements:**
- Username text input
- Password input
- Confirm Password input
- Register button
- "Login here" link

**Validation:**
- Both passwords must match (client-side)
- Username uniqueness checked server-side

---

### Page 3: Dashboard (`dashboard.html`)
**Purpose:** Central hub after login

**Sections:**

**Resume Banner:**
```
If resume uploaded:
  ✅ Resume Uploaded | Skills: Python, Java, SQL [+3 more] | [Re-upload]
Else:
  ⚠️ No resume uploaded | [Upload Resume]
```

**Start Interview Card:**
- "Start Resume Interview" button (visible only if resume uploaded)
- Topic dropdown (15+ topics)
- "Start Topic Interview" button

**Past Sessions Table:**
```
Date          | Questions | Avg Score | Action
Feb 15, 2025  |    8      |   6.5     | [View]
Feb 14, 2025  |    5      |   4.2     | [View]
```

**Tips Section:**
- Tip 1: Upload resume for personalized questions
- Tip 2: Use microphone for better experience
- Tip 3: 60 seconds per question
- Tip 4: Keep your face visible on camera

---

### Page 4: Upload Resume (`upload_resume.html`)
**Purpose:** PDF resume submission with feedback

**Upload Area:**
- Dashed border drag-and-drop zone
- Click to open file picker
- Only accepts `.pdf` files
- Shows selected filename and size after selection
- "Remove" button to deselect

**Loading Animation (during processing):**
```
Step 1: 📄 Reading your PDF...
Step 2: 🔍 Extracting your skills...
Step 3: 🤖 AI is generating personalized questions...
Step 4: ✅ Almost ready!
```

**JavaScript Features:**
```javascript
// Drag and Drop
dropZone.addEventListener('dragover', (e) => { e.preventDefault(); })
dropZone.addEventListener('drop', (e) => { handleFile(e.dataTransfer.files[0]); })

// File validation
function handleFile(file) {
    if (!file.name.endsWith('.pdf')) {
        alert('Only PDF files are accepted');
        return;
    }
    // Show file name and size
}

// Loading overlay during form submit
form.addEventListener('submit', () => {
    loadingOverlay.style.display = 'flex';
    startLoadingMessages(); // Animate through 4 steps
})
```

---

### Page 5: Interview Ready (`interview_ready.html`)
**Purpose:** Pre-interview checklist and camera verification

**Section 1 - Resume Info:**
- Skill badges (from session)
- Resume summary text
- OR topic name if topic-based

**Section 2 - Camera Check:**
```html
<video id="videoFeed" autoplay playsinline></video>
<div id="cameraStatus">Camera OFF</div>
<div id="faceStatus">Waiting...</div>
<button id="startCameraBtn">Turn On Camera</button>
```

**Section 3 - Checklist:**
```
[✅/❌] Camera is active
[✅/❌] Face detected
[Disabled until both ✅] Start Interview →
```

---

### Page 6: Interview (`interview.html`)
**Purpose:** Live interview question presentation and answer collection

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ Progress: Question 3 of 8 [████░░░░░░] 37%      │
└─────────────────────────────────────────────────┘

┌──────────────┐  ┌─────────────────────────────┐
│   ⏱️ Timer   │  │  Q3 [🔊]                     │
│              │  │  "What is a Python          │
│    00:45     │  │   decorator and when        │
│              │  │   would you use one?"       │
└──────────────┘  └─────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Your Answer                                      │
│ ┌─────────────────────────────────────────────┐ │
│ │ [Textarea for typing or transcribed text]   │ │
│ └─────────────────────────────────────────────┘ │
│ [🎤 Speak Answer]  [Status: Ready]  [125 chars] │
│                                                  │
│ [Skip]      [Clear]      [Next Question →]       │
└─────────────────────────────────────────────────┘

[📷 Camera Feed - corner widget]
```

**Timer Logic:**
```javascript
let timeLeft = 60;
const timer = setInterval(() => {
    timeLeft--;
    updateDisplay(timeLeft);
    
    if (timeLeft <= 10) {
        timerElement.classList.add('warning'); // Red color
    }
    
    if (timeLeft <= 0) {
        clearInterval(timer);
        submitForm(); // Auto-submit
    }
}, 1000);
```

**Speech Recording (RecordRTC):**
```javascript
navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    recorder = new RecordRTC(stream, { type: 'audio', mimeType: 'audio/webm' });
    
    speakBtn.onclick = () => {
        if (!recording) {
            recorder.startRecording();
            recording = true;
            speakBtn.textContent = '⏹ Stop Recording';
        } else {
            recorder.stopRecording(async () => {
                const blob = recorder.getBlob();
                const formData = new FormData();
                formData.append('audio', blob, 'audio.webm');
                
                const response = await fetch('/api/transcribe', { method: 'POST', body: formData });
                const data = await response.json();
                answerTextarea.value = data.transcript;
            });
            recording = false;
        }
    };
});
```

---

### Page 7: Results (`result.html`)
**Purpose:** Post-interview performance report

**Score Card:**
```
┌──────────────────────────────────────────┐
│   Your Interview Results                 │
│                                          │
│        ╭──────────╮                      │
│        │   72%    │  ← Color coded       │
│        ╰──────────╯    Green/Yellow/Red  │
│                                          │
│   Total: 57.5/80  |  8 Questions         │
│   Performance: Good                      │
└──────────────────────────────────────────┘
```

**Question Detail Cards:**
```
┌─────────────────────────────────────────────────┐
│  Q1                                     [7.5/10] │
│  "What is a decorator in Python?"                │
│                                                  │
│  Your Answer:                                    │
│  "A decorator is a function that wraps another  │
│   function to add functionality..."              │
│                                                  │
│  Ideal Answer: [Green Box]                       │
│  "Decorators are functions that modify other     │
│   functions using @syntax. They use closures..." │
│                                                  │
│  Feedback: Good answer! Well explained.          │
└─────────────────────────────────────────────────┘
```

**Actions:**
- "Try Again" → Redirects to `/start`
- "Dashboard" → Redirects to `/dashboard`

---

## 15. COMPLETE DATA FLOW

### Full User Journey

```
┌──────────────────────────────────────────────────────────────────────┐
│                    COMPLETE APPLICATION DATA FLOW                     │
└──────────────────────────────────────────────────────────────────────┘

PHASE 1: ONBOARDING
──────────────────
User → /register → 
  [username, password] → 
  hash(password) → 
  DB: INSERT users →
  Redirect to /login

User → / (login) →
  [username, password] →
  DB: SELECT users WHERE username=? →
  check_password_hash(stored, entered) →
  login_user() → Session cookie set →
  Redirect to /dashboard

PHASE 2: RESUME ANALYSIS
────────────────────────
User → /upload (POST) →
  [PDF file bytes] →
  PyPDF2.PdfReader → [raw text] →
  extract_skills(text) → [skills list] →
  generate_summary(text) → [3-line summary] →
  generate_questions_from_resume(text) →
    → Groq API (llama-3.1-8b-instant) →
    → JSON parse → [{q, a}, ...] →
  DB: DELETE resume_questions WHERE user_id=? →
  DB: INSERT resume_questions (user_id, q, a) × N →
  session['skills'] = skills →
  session['resume_summary'] = summary →
  Redirect to /dashboard

PHASE 3: INTERVIEW SETUP
────────────────────────
User → /dashboard → 
  "Start Resume Interview" OR select topic →
  
/start (resume-based):
  DB: SELECT resume_questions WHERE user_id=? →
  questions = [{q, a}, ...] →
  session['interview_questions'] = questions →
  session['interview_index'] = 0 →
  session['session_id'] = uuid4() →
  Redirect to /interview-ready

/start (topic-based):
  selected_topic = form.get('topic') →
  get_questions_for_topic(topic, 5) →
  questions = [{q, a}, ...] →
  [same session setup] →
  Redirect to /interview-ready

PHASE 4: CAMERA VERIFICATION
─────────────────────────────
/interview-ready →
  JavaScript: navigator.mediaDevices.getUserMedia({video: true}) →
  FaceDetector.detect(videoElement) every 1 second →
  consecutiveDetections >= 3 → 
  "Start Interview" button enabled →
  User clicks → Redirect to /interview

PHASE 5: INTERVIEW LOOP (repeats for each question)
────────────────────────────────────────────────────
/interview →
  questions = session['interview_questions'] →
  index = session['interview_index'] →
  current_question = questions[index] →
  Render interview.html with question text →

[Optional] User clicks 🔊 →
  GET /api/tts?text=<question> →
  gTTS(text, lang='en') → MP3 blob → Browser plays audio

[Optional] User clicks 🎤 →
  RecordRTC starts recording →
  User speaks →
  User stops →
  POST /api/transcribe [audio blob] →
  Deepgram API: POST api.deepgram.com/v1/listen →
  JSON response → transcript → Insert into textarea

User types/speaks answer → clicks "Next" OR timer hits 0 →

POST /submit →
  answer = form.get('answer') →
  questions[index] → question_text, ideal_answer →
  evaluate_answer(answer, ideal_answer) →
    TfidfVectorizer.fit_transform([answer, ideal]) →
    cosine_similarity(v1, v2) → similarity float →
    score = round(similarity × 10, 2) →
    feedback = "Good/Average/Needs improvement" →
  DB: INSERT interviews (user_id, question, answer, score, feedback, session_id, ideal_answer) →
  session['interview_index'] += 1 →
  
  if index + 1 >= total_questions:
    Redirect to /result
  else:
    Redirect to /interview (next question)

PHASE 6: RESULTS
────────────────
/result →
  session_id = session['session_id'] →
  DB: SELECT * FROM interviews WHERE session_id=? →
  total_score = SUM(score) →
  max_score = count × 10 →
  percentage = (total_score / max_score) × 100 →
  rating = "Excellent/Average/Needs Work" →
  Render result.html with all answers, ideal answers, scores
```

---

## 16. AI/LLM INTEGRATION DETAILS

### Groq API Configuration

```python
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
```

**Model:** `llama-3.1-8b-instant`
- A fast, efficient variant of Meta's LLaMA 3.1 model
- 8 billion parameters — optimized for speed on Groq's LPU hardware
- "instant" variant offers low latency (ideal for web applications)
- Supports JSON mode for structured output

---

### Prompt Engineering Strategy

The prompt is carefully engineered with multiple constraints to ensure quality output:

**System Message:**
```
"You are a JSON generating assistant that outputs only valid JSON."
```
- Sets clear role expectation
- Prevents the model from adding explanatory text outside JSON

**User Message Structure:**
```
1. Task definition ("Analyze this resume...")
2. IMPORTANT RULES (numbered constraints)
   - Questions must tie to resume content
   - No generic behavioral questions
   - Reference specific projects/skills
3. Input data (resume text, truncated to 5000 chars)
4. Output format specification (JSON schema example)
5. Example response to guide format
```

**API Parameters:**
```python
response_format={"type": "json_object"}  # Force JSON output
temperature=0.5                           # Balanced creativity
max_tokens=2000                           # Sufficient for 8 Q&A pairs
```

---

### Expected AI Response Format

```json
{
    "skills": ["Python", "Django", "PostgreSQL", "Docker"],
    "questions": [
        {
            "q": "In your Django project for inventory management, how did you handle database migrations when the schema changed?",
            "a": "Key points: use makemigrations and migrate commands, handle data migrations separately, test migrations in staging, version control migration files"
        },
        {
            "q": "You mentioned using Docker for containerization. How did you configure your Docker compose setup for the microservices you built?",
            "a": "Key points: docker-compose.yml structure, service definitions, networking between services, volume mounts for persistence, environment variables"
        }
    ]
}
```

---

### AI Response Validation

```python
data = json.loads(response.choices[0].message.content)
questions = data.get("questions", [])

# Validate structure of each question
valid_questions = [
    q for q in questions 
    if isinstance(q, dict) and 'q' in q and 'a' in q
]

# Minimum threshold check
if len(valid_questions) < 3:
    raise ValueError("Insufficient questions generated")
```

---

## 17. SESSION MANAGEMENT

### Flask Session Usage

Flask sessions use **signed cookies** (using the secret key) to store data client-side.

**Session Keys Used:**

| Key | Type | Set When | Used Where |
|-----|------|----------|-----------|
| `skills` | list | After resume upload | Dashboard, interview-ready |
| `resume_summary` | str | After resume upload | Interview-ready page |
| `interview_questions` | list | When interview starts | /interview, /submit |
| `interview_index` | int | When interview starts | /interview, /submit |
| `session_id` | str (UUID) | When interview starts | /submit, /result |
| `interview_topic` | str | When topic selected | Interview-ready page |

**Session Lifecycle:**
```
LOGIN → Session created
UPLOAD → skills, resume_summary added
START → interview_questions, interview_index, session_id added
SUBMIT (each) → interview_index incremented
RESULT → interview data read (session_id used to query DB)
LOGOUT → session.clear() called
CANCEL → interview session keys cleared
```

### Security Note
- Secret key should be cryptographically random in production
- Current key `'interview_ai_secret_2024'` is hardcoded (insecure for production)
- Session data signed but not encrypted (visible in browser dev tools)

---

## 18. ERROR HANDLING & FALLBACK MECHANISMS

### Resume Upload Errors
```python
# File type validation
if not file.filename.endswith('.pdf'):
    flash('Please upload a PDF file')
    return redirect(url_for('upload'))

# PDF parsing failure
try:
    resume_text = extract_text_from_pdf(file_bytes)
except Exception:
    resume_text = ""  # Empty text, graceful degradation
```

### Groq API Failures
```python
try:
    qa_pairs = generate_questions_from_resume(resume_text)
    if len(qa_pairs) < 3:
        raise ValueError("Too few questions")
except Exception:
    # Fallback: use static skill-based questions
    skills = extract_skills(resume_text)
    qa_pairs = get_questions_for_skills(skills)
```

### Deepgram STT Failures
```python
# Audio size validation
if len(audio_bytes) < 500:
    return jsonify({"transcript": "", "error": "Audio too short"}), 400

# API call failure
try:
    response = requests.post(DEEPGRAM_URL, headers=headers, data=audio_bytes)
    transcript = response.json()['results']['channels'][0]['alternatives'][0]['transcript']
except Exception:
    return jsonify({"transcript": "", "error": "Transcription failed"}), 500
```

### Face Detection Fallbacks

```
FaceDetector API (native browser)
    │
    ├── Not supported? → face-api.js (TensorFlow.js)
    │
    └── face-api.js fails to load? → Manual override button
                                       ("Skip camera check")
```

### Empty Answer Handling
```python
def evaluate_answer(user_answer, ideal_answer):
    if not user_answer or user_answer.strip() == "" or user_answer == "SKIPPED":
        return 0, "Question skipped"
```

---

## 19. SECURITY CONSIDERATIONS

### Current Security Measures
1. **Password Hashing:** PBKDF2-SHA256 with salt via Werkzeug
2. **Authentication Required:** `@login_required` on all protected routes
3. **CSRF Protection:** Flask's session signing provides basic CSRF resistance
4. **File Type Validation:** Only `.pdf` files accepted for upload
5. **Audio Size Validation:** Minimum byte check prevents empty submissions

### Known Security Weaknesses (for production improvement)
1. **Hardcoded Secret Key:** `app.secret_key = 'interview_ai_secret_2024'` — should use `os.urandom(24)` or environment variable
2. **API Keys in .env:** Fine for development, but .env should never be committed to version control
3. **No File Size Limit:** Large PDF uploads not size-restricted
4. **No Rate Limiting:** API endpoints can be called repeatedly
5. **SQLite:** Not suitable for production multi-user load; should use PostgreSQL/MySQL
6. **No Input Sanitization on Questions:** User answers stored directly (though parameterized queries prevent SQL injection)
7. **Admin Default Credentials:** `admin/admin123` — must be changed immediately in production

### SQL Injection Prevention
All database queries use parameterized statements:
```python
# Safe: uses ? placeholders
db.execute('SELECT * FROM users WHERE username = ?', [username])

# Never done (unsafe):
db.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

---

## 20. DEPLOYMENT & CONFIGURATION

### Environment Variables (`.env`)
```env
DEEPGRAM_API_KEY=<your_deepgram_api_key>
GROQ_API_KEY=<your_groq_api_key>
```

### Installation & Setup
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Create .env file with API keys
echo "DEEPGRAM_API_KEY=your_key" > .env
echo "GROQ_API_KEY=your_key" >> .env

# 3. Run the application
python app.py
```

### Application Startup (`app.py`)
```python
if __name__ == '__main__':
    init_db()          # Create tables if not exist
    app.run(debug=True) # Start Flask dev server on port 5000
```

### Requirements (`requirements.txt`)
```
flask
flask-login
werkzeug
scikit-learn
PyPDF2
requests
gTTS
python-dotenv
groq
```

### Database Initialization (`utils/db.py`)
```python
def init_db():
    conn = get_db_connection()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (...);
        CREATE TABLE IF NOT EXISTS interviews (...);
        CREATE TABLE IF NOT EXISTS resume_questions (...);
    ''')
    
    # Create default admin user
    existing = conn.execute('SELECT id FROM users WHERE username = ?', ['admin']).fetchone()
    if not existing:
        hashed_pw = generate_password_hash('admin123')
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', ['admin', hashed_pw])
    
    conn.commit()
    conn.close()
```

### Access
- URL: `http://localhost:5000`
- Default admin login: `admin` / `admin123`

---

## APPENDIX A: External Service Documentation

| Service | Documentation URL | Used For |
|---------|------------------|---------|
| Groq API | console.groq.com | LLaMA question generation |
| Deepgram | developers.deepgram.com | Speech-to-text transcription |
| Google TTS (gTTS) | pypi.org/project/gTTS | Text-to-speech output |
| face-api.js | github.com/justadudewhohacks/face-api.js | Face detection fallback |

---

## APPENDIX B: Glossary

| Term | Definition |
|------|-----------|
| TF-IDF | Term Frequency-Inverse Document Frequency — a numerical statistic reflecting word importance in a document |
| Cosine Similarity | A measure of similarity between two non-zero vectors based on the cosine of the angle between them |
| LLM | Large Language Model — AI model trained on vast text data for language understanding and generation |
| LLaMA | Large Language Model Meta AI — open-source LLM by Meta |
| STT | Speech-to-Text — converting spoken audio to written text |
| TTS | Text-to-Speech — converting written text to spoken audio |
| Flask | A lightweight Python web framework |
| Jinja2 | Python templating engine used by Flask |
| RecordRTC | JavaScript library for recording audio/video in browsers |
| WebSocket | Protocol for full-duplex communication over a single TCP connection |
| Session | Server-side or client-side state storage across HTTP requests |
| UUID | Universally Unique Identifier — 128-bit unique string used as session ID |
| PBKDF2 | Password-Based Key Derivation Function 2 — password hashing algorithm |
| MVC | Model-View-Controller — software architectural pattern |
| CRUD | Create, Read, Update, Delete — basic database operations |

---

*Documentation generated: April 30, 2026*
*Project: AI Virtual Interview Preparation Platform*
*Tech Stack: Flask + Python + SQLite + Groq LLaMA + Deepgram + face-api.js*
