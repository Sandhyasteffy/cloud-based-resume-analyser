import re
import PyPDF2
from docx import Document
from skills_data import SKILLS, ROLE_SKILLS

def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return ""

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))

def get_required_skills(role, job_description):
    job_description = job_description.lower()
    jd_skills = []

    for skill in SKILLS:
        if skill.lower() in job_description:
            jd_skills.append(skill)

    role_skills = ROLE_SKILLS.get(role, [])
    return sorted(list(set(jd_skills + role_skills)))

def calculate_match(resume_skills, required_skills):
    matched = sorted(list(set(resume_skills) & set(required_skills)))
    missing = sorted(list(set(required_skills) - set(resume_skills)))
    extra = sorted(list(set(resume_skills) - set(required_skills)))

    if len(required_skills) == 0:
        score = 0
    else:
        score = int((len(matched) / len(required_skills)) * 100)

    return score, matched, missing, extra

def ats_checks(resume_text):
    text = resume_text.lower()

    checks = {
        "Email Present": bool(re.search(r"[\w\.-]+@[\w\.-]+", resume_text)),
        "Phone Present": bool(re.search(r"\b\d{10}\b", resume_text)),
        "Skills Section Present": "skills" in text,
        "Projects Section Present": "project" in text or "projects" in text,
        "Education Section Present": "education" in text,
        "Certifications Section Present": "certification" in text or "certifications" in text,
        "Experience Section Present": "experience" in text
    }

    return checks

def generate_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Try to build practical knowledge in {skill}.")
        suggestions.append(f"If you already know {skill}, mention it clearly in your resume.")
        suggestions.append(f"Add a project or achievement related to {skill}.")

    return suggestions[:9]

def generate_roadmap(missing_skills):
    roadmap = []
    day = 1

    for skill in missing_skills[:5]:
        roadmap.append(f"Day {day}-{day+1}: Learn basics of {skill}")
        day += 2
        roadmap.append(f"Day {day}: Practice one mini task using {skill}")
        day += 1

    return roadmap[:8]

def generate_interview_questions(role, missing_skills):
    question_bank = {
        "python": "What is the difference between list and tuple in Python?",
        "flask": "What is Flask and where is it used?",
        "sql": "What is the difference between WHERE and HAVING?",
        "rest api": "What is a REST API?",
        "html": "What is the difference between block and inline elements?",
        "css": "What is the CSS box model?",
        "javascript": "What is the difference between var, let, and const?",
        "react": "What is a component in React?",
        "aws": "What is EC2 in AWS?",
        "docker": "What is Docker and why is it used?",
        "linux": "What is the difference between ls and cd commands?",
        "networking": "What is the difference between public IP and private IP?",
        "excel": "What is a pivot table in Excel?",
        "pandas": "What is a DataFrame in pandas?",
        "power bi": "What is Power BI used for?"
    }

    questions = []

    for skill in missing_skills:
        if skill in question_bank:
            questions.append(question_bank[skill])

    if role == "Cloud Engineer":
        questions.append("What is the difference between S3 and EBS?")
        questions.append("What is the difference between public cloud and private cloud?")
    elif role == "Python Developer":
        questions.append("What is exception handling in Python?")
    elif role == "Frontend Developer":
        questions.append("What is DOM in JavaScript?")
    elif role == "Data Analyst":
        questions.append("What is data cleaning?")

    return questions[:8]