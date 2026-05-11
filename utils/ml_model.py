from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_answer(user_answer, ideal_answer):
    if not user_answer or user_answer.strip().upper() == 'SKIPPED' or user_answer.strip() == '':
        return 0, 'Question skipped'

    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([user_answer, ideal_answer])
        score = cosine_similarity(vectors[0], vectors[1])[0][0]
        score_10 = round(score * 10, 2)

        if score_10 >= 7:
            feedback = 'Good answer! Well explained.'
        elif score_10 >= 4:
            feedback = 'Average answer. Try to add more detail.'
        else:
            feedback = 'Needs improvement. Study this topic more.'

        return score_10, feedback
    except Exception:
        return 0, 'Could not evaluate answer.'

def extract_keywords(text):
    if not text:
        return []
    try:
        vectorizer = TfidfVectorizer(max_features=15, stop_words='english')
        vectorizer.fit_transform([text])
        return list(vectorizer.get_feature_names_out())
    except Exception:
        return []
