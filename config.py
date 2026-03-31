import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "resume-analyzer-secret-key"
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    DATABASE_PATH = os.path.join(BASE_DIR, "instance", "database.db")
    ALLOWED_EXTENSIONS = {"pdf", "docx"}