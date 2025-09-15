from sklearn.feature_extraction.text import TfidfVectorizer # for TF IDF Score
from sklearn.metrics.pairwise import cosine_similarity # for Cosine Similarity
import spacy # for Semantic Similarity
from typing import Dict # for type hinting

# Import weights from the configuration file
from config import HYBRID_SCORE_WEIGHTS

try:
    nlp = spacy.load('en_core_web_lg')
except OSError:
    print("Downloading spaCy model 'en_core_web_lg'...")
    spacy.cli.download('en_core_web_lg')
    nlp = spacy.load('en_core_web_lg')

def calculate_keyword_score(resume_text: str, jd_text: str) -> float:
    """Calculates TF-IDF cosine similarity. Focuses on exact keyword matches."""
    if not resume_text or not jd_text:
        return 0.0
    
    documents = [resume_text, jd_text]
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
    
    try:
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    except ValueError:
        return 0.0

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(similarity[0][0])

def calculate_semantic_score(resume_text: str, jd_text: str) -> float:
    """Calculates spaCy embedding similarity. Focuses on contextual meaning."""
    if not resume_text or not jd_text:
        return 0.0
    
    resume_doc = nlp(resume_text)
    jd_doc = nlp(jd_text)
    
    if not resume_doc or not resume_doc.vector_norm or not jd_doc or not jd_doc.vector_norm:
        return 0.0
        
    return float(resume_doc.similarity(jd_doc))

def calculate_hybrid_score(resume_text: str, jd_text: str) -> Dict[str, float]:
    """
    Calculates a weighted average of keyword and semantic scores.

    Args:
        resume_text (str): The text content of the resume.
        jd_text (str): The text content of the job description.

    Returns:
        Dict[str, float]: A dictionary containing the final hybrid score
                          and its individual components.
    """
    keyword_weight = HYBRID_SCORE_WEIGHTS.get("keyword", 0.6)
    semantic_weight = HYBRID_SCORE_WEIGHTS.get("semantic", 0.4)
    
    keyword_score = calculate_keyword_score(resume_text, jd_text)
    semantic_score = calculate_semantic_score(resume_text, jd_text)
    
    hybrid_score = (keyword_score * keyword_weight) + (semantic_score * semantic_weight)
    
    return {
        "hybrid_score": round(hybrid_score, 4),
        "keyword_score": round(keyword_score, 4),
        "semantic_score": round(semantic_score, 4)
    }