from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import json
from dotenv import load_dotenv
import os
from django.views.decorators.csrf import csrf_exempt


def mock_interview(request):
    return render(request,"mock_interview.html")

load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("api_key"))
@csrf_exempt
def generate_questions(job_role, company_name):
    prompt = f"Generate 10-15 interview questions for a {job_role} role at {company_name}. Include a mix of technical, soft skills, and aptitude questions. Return only the questions in a numbered list format."
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    questions = [q.strip() for q in response.text.split("\n") if q.strip()]
    return questions if questions else ["No questions generated. Please try again."]

@csrf_exempt
def evaluate_answers(responses):
    prompt = "Evaluate the following interview responses and provide a performance summary with strengths and improvement suggestions:\n"
    for r in responses:
        prompt += f"Q: {r['question']}\nA: {r['answer']}\n"
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    evaluation_text = response.candidates[0].content.parts[0].text if response.candidates else "No evaluation generated."

    return evaluation_text



# API to generate questions
@csrf_exempt
def get_questions(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            job_role = data.get("job_role")
            company_name = data.get("company_name")

            if not job_role or not company_name:
                return JsonResponse({"error": "Missing job role or company name"}, status=400)

            # 🔹 Correcting function call
            questions = generate_questions(job_role, company_name)  

            return JsonResponse({"questions": questions})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

# API to evaluate responses
@csrf_exempt
def evaluate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            responses = data.get("responses")

            if not responses:
                return JsonResponse({"error": "No responses provided"}, status=400)

            evaluation = evaluate_answers(responses)
            return JsonResponse({"evaluation": evaluation})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)