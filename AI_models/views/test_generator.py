from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
import os
# Configure Gemini API
genai.configure(api_key=os.getenv("api_key"))

def generate_questions(subject, topic, year, semester):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""Generate 20 mixed difficulty questions (one-line, two-line, one-word) 
                 on {topic} in {subject} for Year {year} Semester {semester}. 
                 Provide correct answers after each question in the format:
                 Q: <question>
                 A: <answer>
              """
    response = model.generate_content(prompt)
    
    lines = response.text.split("\n")
    questions, answers = [], []

    for i in range(len(lines)):
        if lines[i].startswith("Q:"):
            question = lines[i][2:].strip()
            answer = lines[i + 1][2:].strip() if i + 1 < len(lines) and lines[i + 1].startswith("A:") else "N/A"
            questions.append(question)
            answers.append(answer)
    
    return questions[:20], answers[:20]

def test_generator(request):
    return render(request, "test_generator.html")
@csrf_exempt
def start_test(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        subject = data.get("subject")
        topic = data.get("topic")
        year = data.get("year")
        semester = data.get("semester")

        questions, answers = generate_questions(subject, topic, year, semester)
        return JsonResponse({"questions": questions, "answers": answers})
    return JsonResponse({"error": "Invalid request"}, status=400)
@csrf_exempt
def evaluate(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_responses = data["responses"]
        correct_answers = data["correct_answers"]

        evaluation = []
        correct_count, incorrect_count, skipped_count = 0, 0, 0

        for i in range(len(correct_answers)):
            user_answer = user_responses[i] if i < len(user_responses) else "Skipped"
            correct_answer = correct_answers[i]

            if user_answer.lower() == correct_answer.lower():
                status = "Correct"
                correct_count += 1
            elif user_answer == "Skipped":
                status = "Skipped"
                skipped_count += 1
            else:
                status = "Incorrect"
                incorrect_count += 1

            evaluation.append({
                "question": correct_answers[i],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "status": status
            })

        return JsonResponse({
            "evaluation": evaluation,
            "correct": correct_count,
            "incorrect": incorrect_count,
            "skipped": skipped_count
        })
    return JsonResponse({"error": "Invalid request"}, status=400)
