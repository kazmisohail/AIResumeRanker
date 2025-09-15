import spacy # NLP library for advanced text processing
import re # Regular expressions for pattern matching

# Load the spaCy model once
try:
    nlp = spacy.load('en_core_web_lg') # downloaded model for English
except OSError:
    print("Downloading spaCy model 'en_core_web_lg'...")
    spacy.cli.download('en_core_web_lg')
    nlp = spacy.load('en_core_web_lg')

# A comprehensive list of skills to look for
SKILL_KEYWORDS = [
    'python', 'java', 'c++', 'c#', 'sql', 'javascript', 'typescript', 'html', 'css', 'react', 'angular', 'vue', 'node.js',
    'django', 'flask', 'spring', '.net', 'machine learning', 'deep learning', 'nlp', 'natural language processing',
    'data analysis', 'data science', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
    'project management', 'agile', 'scrum', 'jira', 'confluence', 'product management',
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'ci/cd', 'git', 'github', 'devops',
    'mysql', 'postgresql', 'mongodb', 'nosql', 'rest', 'graphql', 'api', 'microservices', 'big data', 'spark', 'hadoop',
    'business intelligence', 'tableau', 'power bi', 'communication', 'teamwork', 'leadership', 'problem-solving'
]

def extract_skills(text):
    """
    Extracts skills from text using spaCy's NER and an extensive keyword list.
    """
    skills = set()
    doc = nlp(text.lower())
    
    # Method 1: Keyword Matching
    for skill in SKILL_KEYWORDS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
            skills.add(skill)
            
    # Method 2: Named Entity Recognition
    for ent in doc.ents:
        if ent.label_.upper() in ['ORG', 'PRODUCT', 'WORK_OF_ART', 'TECH', 'LANGUAGE']:
            if len(ent.text.split()) <= 4:
                skills.add(ent.text.lower())
                
    return list(skills)