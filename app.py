import os
from dotenv import load_dotenv
load_dotenv()

import io
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from utils.db import init_db, get_db
from utils.auth import User, get_user_by_id, get_user_by_username
from utils.resume_parser import extract_text_from_pdf, extract_skills, generate_summary
from utils.ml_model import evaluate_answer
from utils.question_generator import get_questions_for_topic, get_questions_for_skills, get_available_topics, generate_questions_from_resume

app = Flask(__name__)
app.secret_key = 'interview_ai_secret_2024'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


# ─── AUTH ROUTES ───────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        row = get_user_by_username(username)
        if row and check_password_hash(row['password'], password):
            user = User(row['id'], row['username'])
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('register.html')
        if get_user_by_username(username):
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        hashed = generate_password_hash(password)
        conn = get_db()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


# ─── DASHBOARD ─────────────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    sessions = conn.execute(
        "SELECT session_id, MAX(created_at) as date, COUNT(*) as total, AVG(score) as avg_score "
        "FROM interviews WHERE user_id = ? GROUP BY session_id ORDER BY date DESC LIMIT 5",
        (current_user.id,)
    ).fetchall()
    conn.close()
    topics = get_available_topics()
    has_resume = session.get('has_resume', False)
    resume_skills = session.get('resume_skills', [])
    return render_template('dashboard.html', sessions=sessions, topics=topics,
                           username=current_user.username, has_resume=has_resume,
                           resume_skills=resume_skills)


# ─── RESUME UPLOAD ─────────────────────────────────────────────────────────────

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('resume')
        if not file or file.filename == '':
            flash('Please select a PDF file.', 'danger')
            return render_template('upload_resume.html')
        if not file.filename.lower().endswith('.pdf'):
            flash('Only PDF files are supported.', 'danger')
            return render_template('upload_resume.html')
        file_bytes = file.read()
        text = extract_text_from_pdf(file_bytes)
        if not text:
            flash('Could not read text from PDF. Try a different file.', 'danger')
            return render_template('upload_resume.html')
        skills = extract_skills(text)
        summary = generate_summary(text)
        session['resume_skills'] = skills
        session['resume_summary'] = summary
        session['has_resume'] = True
        
        # Generate questions from AI and store in database
        import random
        num_q = random.randint(5, 10)
        ai_result = generate_questions_from_resume(text, num_questions=num_q)
        if ai_result:
            # Overwrite static skills with the smart AI-detected skills
            if ai_result.get('skills'):
                session['resume_skills'] = ai_result['skills']
                
            conn = get_db()
            conn.execute("DELETE FROM resume_questions WHERE user_id = ?", (current_user.id,))
            for q in ai_result.get('questions', []):
                conn.execute(
                    "INSERT INTO resume_questions (user_id, question, ideal_answer) VALUES (?, ?, ?)",
                    (current_user.id, q['q'], q['a'])
                )
            conn.commit()
            conn.close()
            session['ai_questions_ready'] = True
        else:
            session['ai_questions_ready'] = False
            
        return redirect(url_for('interview_ready'))
    return render_template('upload_resume.html')


# ─── INTERVIEW READY PAGE ──────────────────────────────────────────────────────

@app.route('/interview-ready')
@login_required
def interview_ready():
    # If the user selected a specific topic, override the resume flag for this view
    topic = request.args.get('topic')
    has_resume = False if topic else session.get('has_resume', False)
    
    skills = session.get('resume_skills', [])
    summary = session.get('resume_summary', '')
    topics = get_available_topics()
    return render_template('interview_ready.html', has_resume=has_resume,
                           skills=skills, summary=summary, topics=topics)


# ─── INTERVIEW ─────────────────────────────────────────────────────────────────

@app.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    topic = request.args.get('topic', '')
    has_resume = session.get('has_resume', False)

    if has_resume and not topic:
        if session.get('ai_questions_ready'):
            conn = get_db()
            rows = conn.execute("SELECT question, ideal_answer FROM resume_questions WHERE user_id = ?", (current_user.id,)).fetchall()
            conn.close()
            if rows:
                questions = [{'q': row['question'], 'a': row['ideal_answer']} for row in rows]
            else:
                skills = session.get('resume_skills', [])
                questions = get_questions_for_skills(skills)
        else:
            skills = session.get('resume_skills', [])
            questions = get_questions_for_skills(skills)
    elif topic:
        questions = get_questions_for_topic(topic)
    else:
        questions = get_questions_for_topic('hr')

    # Normalize format (AI returns dicts, static returns tuples)
    normalized_questions = []
    for item in questions:
        if isinstance(item, dict):
            normalized_questions.append(item)
        else:
            normalized_questions.append({'q': item[0], 'a': item[1]})

    session['interview_questions'] = normalized_questions
    session['interview_index'] = 0
    session['session_id'] = str(uuid.uuid4())
    session['interview_topic'] = topic or ('resume' if has_resume else 'hr')

    return redirect(url_for('interview'))


@app.route('/interview')
@login_required
def interview():
    questions = session.get('interview_questions', [])
    index = session.get('interview_index', 0)

    if not questions or index >= len(questions):
        return redirect(url_for('result'))

    question = questions[index]['q']
    total = len(questions)
    api_key = os.environ.get('DEEPGRAM_API_KEY', '')
    return render_template('interview.html', question=question, index=index, total=total, dg_key=api_key)


@app.route('/submit', methods=['POST'])
@login_required
def submit():
    questions = session.get('interview_questions', [])
    index = session.get('interview_index', 0)
    session_id = session.get('session_id', '')

    if not questions or index >= len(questions):
        return redirect(url_for('result'))

    user_answer = request.form.get('answer', '').strip()
    skipped = request.form.get('skipped', 'false') == 'true'

    if skipped or not user_answer:
        user_answer = 'SKIPPED'
        score = 0
        feedback = 'Question skipped'
    else:
        ideal_answer = questions[index]['a']
        score, feedback = evaluate_answer(user_answer, ideal_answer)

    conn = get_db()
    ideal_ans = questions[index]['a'] if not skipped else ''
    conn.execute(
        "INSERT INTO interviews (user_id, question, ideal_answer, answer, score, feedback, session_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (current_user.id, questions[index]['q'], ideal_ans, user_answer, score, feedback, session_id)
    )
    conn.commit()
    conn.close()

    session['interview_index'] = index + 1
    return redirect(url_for('interview'))


@app.route('/cancel')
@login_required
def cancel_interview():
    session.pop('interview_questions', None)
    session.pop('interview_index', None)
    session.pop('session_id', None)
    flash('Interview cancelled successfully.', 'info')
    return redirect(url_for('dashboard'))


# ─── RESULT ────────────────────────────────────────────────────────────────────

@app.route('/result')
@login_required
def result():
    session_id = session.get('session_id', '')
    conn = get_db()
    rows = conn.execute(
        "SELECT question, ideal_answer, answer, score, feedback FROM interviews WHERE user_id = ? AND session_id = ?",
        (current_user.id, session_id)
    ).fetchall()
    conn.close()

    total_score = sum(r['score'] for r in rows)
    max_score = len(rows) * 10
    percentage = round((total_score / max_score * 100), 1) if max_score > 0 else 0

    session.pop('interview_questions', None)
    session.pop('interview_index', None)
    session.pop('session_id', None)

    return render_template('result.html', rows=rows, total_score=round(total_score, 2),
                           max_score=max_score, percentage=percentage)


# ─── SPEECH TO TEXT (backend) ─────────────────────────────────────────────────

@app.route('/api/transcribe', methods=['POST'])
@login_required
def transcribe():
    import requests

    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'transcript': '', 'error': 'No audio received'})

    raw = audio_file.read()
    if len(raw) < 500:
        return jsonify({'transcript': '', 'error': f'Audio too short ({len(raw)} bytes). Hold mic button and speak for at least 2 seconds.'})

    api_key = os.environ.get('DEEPGRAM_API_KEY')
    if not api_key:
        return jsonify({'transcript': '', 'error': 'DEEPGRAM_API_KEY environment variable not set. Please configure it to use speech-to-text.'})

    try:
        # Simplified URL. Deepgram's auto-detect is very powerful.
        url = "https://api.deepgram.com/v1/listen?punctuate=true"
        
        headers = {
            "Authorization": f"Token {api_key}"
            # Omitting Content-Type entirely forces Deepgram to auto-detect from file signature
        }
        
        response = requests.post(url, headers=headers, data=raw)
        response.raise_for_status()
        data = response.json()
        
        try:
            transcript = data['results']['channels'][0]['alternatives'][0]['transcript']
            if transcript:
                return jsonify({'transcript': transcript, 'error': ''})
            else:
                return jsonify({'transcript': '', 'error': 'Could not understand speech. Please speak louder and more clearly.'})
        except (KeyError, IndexError):
            return jsonify({'transcript': '', 'error': 'Could not parse Deepgram response.'})

    except requests.exceptions.RequestException as e:
        return jsonify({'transcript': '', 'error': 'Deepgram service error. Check internet connection. ' + str(e)})
    except Exception as e:
        return jsonify({'transcript': '', 'error': 'Server error: ' + str(e)})


# ─── TEXT TO SPEECH (backend) ──────────────────────────────────────────────────

@app.route('/api/tts', methods=['GET'])
@login_required
def text_to_speech():
    text = request.args.get('text', '').strip()
    if not text:
        return '', 400
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return send_file(buf, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
