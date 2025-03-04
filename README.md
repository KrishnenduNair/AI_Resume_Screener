# AI_Resume_Screener

A simple AI-powered resume screening tool that extracts and analyzes text from **PDF, DOCX, and TXT** resumes.  

## **Features**  
- Upload and extract text from resumes (**PDF, DOCX, TXT**)  
- Basic resume parsing and analysis  
- FastAPI-based backend  
- React Native frontend (if applicable)  

## **Installation**  

### **1. Clone the Repository**  
```sh
git clone https://github.com/KrishnenduNair/AI_Resume_Screener.git
cd AI_Resume_Screener
```

### **2. Set Up a Virtual Environment**  
```sh
python3 -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows (cmd)
```

### **3. Install Dependencies**  
```sh
pip install fastapi uvicorn pdfminer.six python-docx
```

### **4. Run the Backend Server**  
```sh
uvicorn backend.app:app --reload
```
The server will run on **http://127.0.0.1:8000/**  

## **API Endpoints**  

| Method | Endpoint | Description |
|--------|---------|-------------|
| **POST** | `/upload` | Uploads a resume (**PDF, DOCX, or TXT**) and extracts text |

## **Usage**  
- Open **http://127.0.0.1:8000/docs** in a browser to test the API.  

## **Requirements**  
The following Python packages are required:  
- `fastapi`  
- `uvicorn`  
- `pdfminer.six`  
- `python-docx`  

## **Contributing**  
Feel free to fork and contribute by submitting pull requests.  

## **License**  
MIT License  

---

You can save this as **README.md** and commit it. Let me know if you need more modifications!
