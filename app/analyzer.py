# analyzer.py
import re
import string
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return ' '.join(tokens)

def extract_keywords(text, top_k=15):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text])
    keywords = sorted(
        zip(vectorizer.get_feature_names_out(), tfidf.toarray()[0]),
        key=lambda x: x[1],
        reverse=True
    )
    return [kw for kw, _ in keywords[:top_k]]

def analyze_resume(resume_text, jd_text):
    clean_resume = preprocess(resume_text)
    clean_jd = preprocess(jd_text)

    resume_keywords = extract_keywords(clean_resume)
    jd_keywords = extract_keywords(clean_jd)

    missing = list(set(jd_keywords) - set(resume_keywords))

    vec = TfidfVectorizer()
    tfidf = vec.fit_transform([clean_resume, clean_jd])
    match_score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    return {
        "match_score": round(match_score * 100, 2),
        "resume_keywords": resume_keywords,
        "jd_keywords": jd_keywords,
        "missing_keywords": missing
    }
