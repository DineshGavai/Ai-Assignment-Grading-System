from django.shortcuts import render
import os
import pdfplumber
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

load_dotenv()

def AGS(request):
    return render(request,"Assignment_Grading_System.html") 



# Configure Gemini API Key
genai.configure(api_key=os.getenv("api_key"))

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def grade_assignment(text, year, semester, subject):
    prompt = f"""
    You are an AI assignment grader. Grade the following handwritten assignment based on its correctness and provide a detailed evaluation:

    - Year: {year}
    - Semester: {semester}
    - Subject: {subject}

    Assignment Text:
    {text}

    Output the following:
    1. Accuracy Percentage
    2. List of Incorrect Answers and Corrections
    3. Suggestions for Improvement
    4. Plagiarism Detection Percentage
    5. Statistical Report (Grade and Remarks)
    """
    
    response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
    return response.text if response else "Error generating response."

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = default_storage.save(os.path.join('uploads', file.name), ContentFile(file.read()))
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        year = request.POST.get("year")
        semester = request.POST.get("semester")
        subject = request.POST.get("subject")
        
        assignment_text = extract_text_from_pdf(file_path)
        result = grade_assignment(assignment_text, year, semester, subject)
        
        return JsonResponse({"result": result})
    return JsonResponse({"error": "No file provided"}, status=400)
