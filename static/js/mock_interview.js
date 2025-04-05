let questions = [];
let currentQuestionIndex = 0;
let responses = [];

async function startInterview() {
    const jobRole = document.getElementById("job_role").value;
    const companyName = document.getElementById("company_name").value;

    if (!jobRole || !companyName) {
        alert("Please enter both job role and company name.");
        return;
    }

    const response = await fetch("generate_questions/", {
        // const response = await fetch("{% url 'get_questions'%}", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_role: jobRole, company_name: companyName })
    });

    const data = await response.json();
    questions = data.questions;
    console.log
    if (questions.length === 0 || questions[0] === "No questions generated. Please try again.") {
        alert("No questions generated. Please try again.");
        return;
    }

    document.getElementById("input-section").style.display = "none";
    document.getElementById("interview-section").style.display = "block";
    showNextQuestion();
}

function showNextQuestion() {
    if (currentQuestionIndex < questions.length) {
        document.getElementById("question").innerText = questions[currentQuestionIndex];
        document.getElementById("answer").value = "";
    } else {
        finishInterview();
    }
}

function submitAnswer() {
    const answer = document.getElementById("answer").value;
    responses.push({ question: questions[currentQuestionIndex], answer });

    currentQuestionIndex++;
    showNextQuestion();
}

function skipQuestion() {
    responses.push({ question: questions[currentQuestionIndex], answer: "Skipped" });

    currentQuestionIndex++;
    showNextQuestion();
}

async function finishInterview() {
    document.getElementById("interview-section").style.display = "none";

    const response = await fetch("evaluate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ responses })
    });

    const data = await response.json();

    // Directly setting the evaluation text (since it's a string, not JSON array)
    document.getElementById("evaluation-result").innerHTML = `<p>${data.evaluation.replace(/\n/g, "<br>")}</p>`;
    document.getElementById("evaluation-section").style.display = "block";
}