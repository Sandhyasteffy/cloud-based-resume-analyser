import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from config import Config
from database import init_db, save_analysis, get_all_results
from utils import (
    allowed_file,
    extract_text,
    extract_skills,
    get_required_skills,
    calculate_match,
    ats_checks,
    generate_suggestions,
    generate_roadmap,
    generate_interview_questions
)

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]), exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return "Resume file is missing."

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()
    role = request.form.get("role", "").strip()

    if resume_file.filename == "":
        return "Please upload a resume file."

    if not allowed_file(resume_file.filename, app.config["ALLOWED_EXTENSIONS"]):
        return "Only PDF and DOCX files are allowed."

    filename = secure_filename(resume_file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume_file.save(file_path)

    resume_text = extract_text(file_path)
    resume_skills = extract_skills(resume_text)
    required_skills = get_required_skills(role, job_description)

    match_score, matched_skills, missing_skills, extra_skills = calculate_match(
        resume_skills, required_skills
    )

    checks = ats_checks(resume_text)
    suggestions = generate_suggestions(missing_skills)
    roadmap = generate_roadmap(missing_skills)
    interview_questions = generate_interview_questions(role, missing_skills)

    if match_score >= 80:
        level = "Strong Match"
    elif match_score >= 60:
        level = "Moderate Match"
    else:
        level = "Needs Improvement"

    save_analysis(
        filename,
        role,
        match_score,
        matched_skills,
        missing_skills,
        extra_skills
    )

    return render_template(
        "result.html",
        file_name=filename,
        role=role,
        match_score=match_score,
        level=level,
        resume_skills=resume_skills,
        required_skills=required_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        extra_skills=extra_skills,
        checks=checks,
        suggestions=suggestions,
        roadmap=roadmap,
        interview_questions=interview_questions
    )


@app.route("/dashboard")
def dashboard():
    results = get_all_results()
    return render_template("dashboard.html", results=results)


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0',port=5000, debug=True)