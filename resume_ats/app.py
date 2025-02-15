from flask import Flask, render_template, request
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

def get_gemini_response(input_text):
    """Get a response from Google Gemini AI."""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)

    print("\n🔹 Raw AI Response:\n", response.text)  # Debugging AI response
    return response.text

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text()) + "\n"
    return text.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    response_data = None  # Store AI response

    if request.method == "POST":
        job_description = request.form.get("job_description")
        uploaded_file = request.files.get("resume")

        if job_description and uploaded_file:
            # Extract text from the uploaded PDF
            resume_text = extract_text_from_pdf(uploaded_file)

            # AI Prompt
            input_prompt = f"""
            You are an advanced Applicant Tracking System (ATS) with expertise in software engineering, 
            data science, data analysis, and big data. Your job is to analyze resumes and provide feedback.

            1️⃣ Assign a **Job Description Match %** (e.g., "85%").
            2️⃣ List **missing keywords** (skills not mentioned in the resume).
            3️⃣ Provide a **profile summary** with suggestions for improvement.

            Return your response **EXACTLY** in this JSON format:
            {{"JD Match": "85%", "MissingKeywords": ["Python", "Machine Learning"], "Profile Summary": "Your resume is strong but lacks cloud computing experience."}}

            Resume:
            {resume_text}

            Job Description:
            {job_description}
            """

            # Get AI response
            ai_response = get_gemini_response(input_prompt)

            try:
                # Convert AI response to JSON
                response_data = json.loads(ai_response)
            except json.JSONDecodeError:
                print("❌ AI response is not in JSON format:\n", ai_response)  # Debugging print
                response_data = {"error": "AI response is not in the expected format.", "raw_response": ai_response}

    return render_template("index.html", response_data=response_data)

if __name__ == "__main__":
    app.run(debug=True)
