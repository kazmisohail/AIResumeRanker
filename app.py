from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

# Import your custom modules
from modules.file_parser import extract_text_from_docx
from modules.ranker import calculate_hybrid_score
from modules.nlp_processor import extract_skills

app = Flask(__name__)

# Configure a temporary upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def scale_scores_max_abs(results):
    """
    Top candidate will always be 100%...!!
    """
    if not results:
        return []

    # Find the maximum hybrid score in the list
    # Added a default of 0 to prevent error on empty list
    max_score = max([res['scores']['hybrid_score'] for res in results] or [0])
    
    if max_score == 0:
        # If all scores are 0, just set scaled_score to 0 for all
        for res in results:
            res['scaled_score'] = 0
            res['scores']['keyword_score'] = int(res['scores']['keyword_score'] * 100)
            res['scores']['semantic_score'] = int(res['scores']['semantic_score'] * 100)
        return results

    for res in results:
        # Scale the main score relative to the max score
        res['scaled_score'] = int((res['scores']['hybrid_score'] / max_score) * 100)
        # Convert component scores to percentage for display
        res['scores']['keyword_score'] = int(res['scores']['keyword_score'] * 100)
        res['scores']['semantic_score'] = int(res['scores']['semantic_score'] * 100)
        
    return results


@app.route('/')
def index():
    """ This route ONLY handles displaying the main upload form. """
    return render_template('index.html')


@app.route('/rank', methods=['POST'])
def rank_resumes():
    """ This route ONLY handles the form submission and processing. """
    if request.method == 'POST':
        jd_text = request.form.get('job_description')
        jd_file = request.files.get('jd_file')
        
        if jd_file and jd_file.filename != '':
            jd_text = extract_text_from_docx(jd_file)
        
        uploaded_files = request.files.getlist('resumes')

        if not jd_text or not uploaded_files[0].filename:
            return render_template('index.html', error="Please provide a job description and upload at least one resume...!!")

        jd_skills = set(extract_skills(jd_text))
        print(f"Skills extracted from JD: {list(jd_skills)}")

        raw_results = []
        total_files = len(uploaded_files)
        
        print(f"\n Received {total_files} resumes...! Starting processing...!!")

        for i, resume_file in enumerate(uploaded_files):
            if resume_file.filename == '':
                continue

            filename = secure_filename(resume_file.filename)
            resume_text = extract_text_from_docx(resume_file)
            
            if not resume_text.strip():
                print(f"[{i+1}/{total_files}] Skipping {filename} (could not read content or is empty).")
                continue
            
            scores = calculate_hybrid_score(resume_text, jd_text)
            resume_skills = set(extract_skills(resume_text))
            matched_skills = list(jd_skills.intersection(resume_skills))
            
            print(f"[{i+1}/{total_files}] Processing: {filename} -> Hybrid Score: {scores['hybrid_score']:.4f}")
            
            raw_results.append({
                'filename': filename,
                'scores': scores,
                'matched_skills': matched_skills
            })
            
        print("Processing complete! Scaling and ranking...!!")

        scaled_results = scale_scores_max_abs(raw_results)
        ranked_results = sorted(scaled_results, key=lambda x: x['scaled_score'], reverse=True)

        print("Ranking complete! Sending response to browser...!!")

        return render_template('results.html', results=ranked_results)

if __name__ == '__main__':
    app.run(debug=True)