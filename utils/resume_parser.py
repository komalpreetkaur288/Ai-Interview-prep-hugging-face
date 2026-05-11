import PyPDF2
import io

SKILL_KEYWORDS = [
    'python', 'java', 'javascript', 'c++', 'c#', 'sql', 'mysql', 'mongodb',
    'html', 'css', 'react', 'angular', 'node', 'django', 'flask', 'spring',
    'machine learning', 'deep learning', 'nlp', 'data science', 'tensorflow',
    'keras', 'scikit-learn', 'pandas', 'numpy', 'git', 'docker', 'kubernetes',
    'aws', 'azure', 'linux', 'agile', 'scrum', 'rest api', 'php', 'ruby',
    'swift', 'kotlin', 'android', 'ios', 'excel', 'tableau', 'power bi'
]

def extract_text_from_pdf(file_bytes):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text.strip()
    except Exception as e:
        return ''

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.append(skill.title())
    return list(set(found))

def generate_summary(text):
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 30]
    return ' '.join(lines[:3]) if lines else 'No summary available.'
