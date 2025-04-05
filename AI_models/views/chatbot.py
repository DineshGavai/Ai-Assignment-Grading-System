from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
import os
# Configure Gemini API
genai.configure(api_key=os.getenv("api_key"))

# Generate Socratic Response
def generate_socratic_response(user_question):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(user_question)
    return response.text if response else "Can you think about it in a different way?"

# Home page
def chatbot(request):
    return render(request, "chatbot.html")

# Chatbot interaction
@csrf_exempt
def chat(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_question = data.get("question", "")
        bot_response = generate_socratic_response(user_question)
        return JsonResponse({"response": bot_response})
    return JsonResponse({"error": "Invalid request"}, status=400)
