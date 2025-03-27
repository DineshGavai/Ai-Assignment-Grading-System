from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from dotenv import load_dotenv
import os
from django.http import JsonResponse
import json

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("api_key"))


def resume_builder(request):
    return render(request,"resume_builder.html")

@csrf_exempt
def generate_resume(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_data = data.get("user_data", {})
            job_desc = data.get("job_description", "")

            if not user_data or not job_desc:
                return JsonResponse({"error": "Missing user data or job description"}, status=400)

            prompt = f"Create a professional resume for {user_data.get('name', 'Unnamed')} with education in {user_data.get('education', 'N/A')}, experience in {user_data.get('experience', 'N/A')}, skills: {user_data.get('skills', 'N/A')}, tailored for the job: {job_desc}."

            model = genai.GenerativeModel("gemini-1.5-pro")  
            response = model.generate_content(prompt)

            resume_content = response.text if hasattr(response, "text") else "Resume generation failed."

            return JsonResponse({"resume_content": resume_content})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)