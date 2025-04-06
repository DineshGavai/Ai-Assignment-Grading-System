let questions = [];
let answers = [];
let userResponses = [];
let currentQuestionIndex = 0;


// Start Test
function startTest() {
    const subject = document.getElementById("subject").value;
    const topic = document.getElementById("topic").value;
    const year = document.getElementById("year").value;
    const semester = document.getElementById("semester").value;
    
    if (!subject || !topic || !year || !semester) {
        alert("Please fill all fields.");
        return;
    }

    document.getElementById("userInput").classList.add("hidden");
    document.getElementById("loading").classList.remove("hidden");

    fetch("start_test/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, topic, year, semester })
    })
        .then(response => {
            if (response.headers.get("content-type").includes("application/json")) {
                return response.json();
            } else {
                throw new Error("Expected JSON, got something else");
            }
        })
        // .then(response => response.json())
        .then(data => {
            questions = data.questions;
            answers = data.answers;
            document.getElementById("loading").classList.add("hidden");
            document.getElementById("testSection").classList.remove("hidden");
            showQuestion();
        });
}

// Display Next Question
function showQuestion() {
    if (currentQuestionIndex < questions.length) {
        document.getElementById("questionText").innerText = questions[currentQuestionIndex];
        document.getElementById("answerInput").value = "";
    } else {
        evaluateTest();
    }
}

// Submit Answer
function submitAnswer() {
    let answer = document.getElementById("answerInput").value.trim();
    userResponses.push(answer || "Skipped");
    currentQuestionIndex++;
    showQuestion();
}

// Skip Question
function skipQuestion() {
    userResponses.push("Skipped");
    currentQuestionIndex++;
    showQuestion();
}

// Evaluate Test
function evaluateTest() {
    document.getElementById("testSection").classList.add("hidden");
    document.getElementById("loading").classList.remove("hidden");

    fetch("evaluate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ responses: userResponses, correct_answers: answers })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").classList.add("hidden");
            document.getElementById("resultsSection").classList.remove("hidden");

            let resultsHTML = "<h2>Test Results</h2><table>";
            resultsHTML += "<tr><th>Question</th><th>Your Answer</th><th>Correct Answer</th><th>Status</th></tr>";

            data.evaluation.forEach(item => {
                let status = item.status === "Correct" ? "✅" : item.status === "Incorrect" ? "❌" : "⚠ Skipped";
                resultsHTML += `<tr>
                <td>${item.question}</td>
                <td>${item.user_answer || "Not Attempted"}</td>
                <td>${item.correct_answer}</td>
                <td>${status}</td>
            </tr>`;
            });

            resultsHTML += "</table>";
            document.getElementById("resultsSection").innerHTML = resultsHTML;
        });
}


