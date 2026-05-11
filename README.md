# AI Virtual Interview Preparation

## Synopsis
AI Virtual Interview Preparation is an intelligent, web-based platform designed to help job seekers practice for technical and behavioral interviews. It leverages cutting-edge Generative AI to dynamically tailor the interview experience directly to the candidate's actual qualifications.

Unlike static interview simulators, this platform analyzes a user's uploaded PDF resume, extracts their specific technical skills, and uses **Groq (Llama 3)** to instantly generate 5 to 10 highly personalized interview questions. These questions focus exclusively on the exact projects, tools, and experiences the candidate has claimed.

During the interview, the platform uses real-time computer vision (`face-api.js`) to ensure the user remains in front of the camera, simulating a proctored environment. As the user answers questions, they speak directly into their microphone, and the system uses **Deepgram's** lightning-fast speech-to-text API to transcribe their answers live.

Once the interview concludes, the platform's backend evaluates the candidate's spoken answers against the AI's generated "ideal answers" using TF-IDF cosine similarity. Finally, it provides a comprehensive dashboard detailing a question-by-question breakdown, including scores, the expected ideal answers, and constructive feedback for improvement.

## Key Features
* **Resume Parsing:** Upload a PDF resume to instantly extract core skills and generate a dynamic profile.
* **AI-Powered Question Generation:** Uses Groq's `llama-3.1-8b-instant` model to create custom technical and behavioral questions strictly derived from the uploaded resume.
* **Proctored Environment:** Integrates `face-api.js` to require a 3-second face detection lock before an interview can start, ensuring the candidate is present.
* **Real-time Transcription:** Utilizes Deepgram WebSockets to provide live transcription of spoken answers.
* **Answer Evaluation:** Compares the candidate's transcribed answer with an AI-generated ideal answer to provide a 0-10 score and constructive feedback.
* **Progress Tracking:** Saves all session data to an SQLite database, allowing users to track their average scores and historical performance via a clean dashboard.

## Tech Stack
* **Backend:** Python, Flask, SQLite
* **Frontend:** HTML, CSS, JavaScript (Vanilla)
* **AI & Machine Learning:** Groq API (Llama 3), scikit-learn (TF-IDF Vectorization)
* **Computer Vision:** face-api.js (Browser-based face detection)
* **Speech Services:** Deepgram API (STT), gTTS (TTS)

## Installation & Setup

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   DEEPGRAM_API_KEY=your_deepgram_api_key
   GROQ_API_KEY=your_groq_api_key
   ```
4. **Run the Application:**
   ```bash
   python app.py
   ```
5. **Access the Application:**
   Open your browser and navigate to `http://localhost:5000`. Create an account and upload your resume to get started!
