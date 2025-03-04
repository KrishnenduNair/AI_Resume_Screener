import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pdfminer.high_level import extract_text
from docx import Document
from fastapi import FastAPI, UploadFile, File
from typing import List

nltk.download('punkt')
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))

skills_set = {
    "python", "java", "c++", "javascript", "typescript", "go", "rust", "kotlin", "swift", "ruby", "php",
    "machine learning", "deep learning", "nlp", "computer vision", "reinforcement learning",
    "data science", "big data", "data engineering", "data visualization",
    "sql", "postgresql", "mysql", "mongodb", "firebase", "cassandra", "neo4j",
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "lightgbm", "opencv", "spacy",
    "hadoop", "spark", "apache flink", "airflow",
    "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "terraform",
    "flask", "django", "fastapi", "express.js", "react", "next.js", "vue.js", "svelte",
    "git", "github", "gitlab", "bitbucket",
    "linux", "bash scripting", "network security", "ethical hacking", "penetration testing",
    "blockchain", "cryptography", "smart contracts", "solidity",
    "agile", "scrum", "software architecture", "microservices",
    "natural language processing", "transformers", "bert", "gpt", "llms",
    "feature engineering", "model deployment", "mle", "feature selection",
    "recommendation systems", "graph neural networks", "autoML", "hyperparameter tuning",
    "cloud computing", "edge computing", "serverless computing",
    "robotics", "autonomous systems", "embedded systems", "IoT", "sensor fusion"
}

def get_ext(file_path):
    ext = file_path.rsplit('.', 1)
    if len(ext) > 1 and ext[0]:  
        return ext[-1].lower()
    return None

def extract_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_pdf_file(pdf_path):
    text = extract_text(pdf_path)
    return text.strip()

def extract_docx_file(docx_path):
    doc = Document(docx_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text.strip()

def parse_resume(file_path):
    ext = get_ext(file_path)
    
    try:
        if ext == 'txt':
            parsed_text = extract_text_file(file_path)
        elif ext == 'pdf':
            parsed_text = extract_pdf_file(file_path)
        elif ext == 'docx':
            parsed_text = extract_docx_file(file_path)
        else:
            return None, None
        
        if not parsed_text.strip():
            return None, None

        skills = extract_skills(parsed_text)
        return parsed_text, skills
    except Exception as e:
        print(f"Error processing file: {e}")
        return None, None

def preprocess(text):
    text = text.lower()
    words = word_tokenize(text)
    words_filtered = [w for w in words if w in skills_set or (w not in stopwords and w.isalpha())]
    return words_filtered

def extract_skills(text):
    words = preprocess(text)
    matched_skills = set()

    for i in range(len(words)):
        if words[i] in skills_set:
            matched_skills.add(words[i].lower())

        if i < len(words) - 1:
            two_word = f"{words[i]} {words[i+1]}".lower()
            if two_word in skills_set:
                matched_skills.add(two_word)

        if i < len(words) - 2:
            three_word = f"{words[i]} {words[i+1]} {words[i+2]}".lower()
            if three_word in skills_set:
                matched_skills.add(three_word)

    return list(matched_skills)

app = FastAPI()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    allowed_exts = {"txt", "pdf", "docx"}
    ext = file.filename.split(".")[-1].lower()
    
    if ext not in allowed_exts:
        return {"error": "Unsupported file format"}
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text, skills = parse_resume(file_path)
    if text is None:
        return {"error": "Could not extract text, file may be empty or corrupt"}

    return {"extracted_text": text, "detected_skills": skills}