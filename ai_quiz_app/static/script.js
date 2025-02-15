let questions = [];
let quizSubmitted = false; // Track if the quiz has been submitted

async function loadQuiz() {
    console.log("Fetching quiz questions...");
    document.getElementById("quiz-container").innerHTML = "<p>Loading questions...</p>";

    try {
        const response = await fetch("/get_quiz");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        questions = await response.json();
        console.log("Received questions:", questions);
        displayQuestions();

        // Disable Restart button until Submit is clicked
        document.getElementById("restart-btn").disabled = true;
        quizSubmitted = false;

    } catch (error) {
        console.error("Error loading quiz:", error);
        document.getElementById("quiz-container").innerHTML = "<p>Failed to load quiz. Please try again.</p>";
    }
}

function displayQuestions() {
    let html = "";
    questions.forEach((q, index) => {
        html += `<div class="mb-3">
                    <p class="question">${index + 1}. ${q.question}</p>
                    <div class="options">
                        ${q.options.map(opt => `
                            <label class="option" id="label-${index}-${opt.charAt(0)}">
                                <input type="radio" name="q${index}" value="${opt.charAt(0)}" onclick="highlightSelected(${index}, '${opt.charAt(0)}')">
                                ${opt}
                            </label>
                        `).join('')}
                    </div>
                    <p id="result-${index}" class="result"></p>
                 </div>`;
    });
    document.getElementById("quiz-container").innerHTML = html;
}

// Highlight the selected option
function highlightSelected(index, selectedValue) {
    document.querySelectorAll(`input[name="q${index}"]`).forEach((input) => {
        let label = document.getElementById(`label-${index}-${input.value}`);
        label.style.backgroundColor = (input.value === selectedValue) ? "#d0eaff" : "#e9ecef";
    });
}

// Check answers and highlight correct/incorrect
function submitQuiz() {
    if (quizSubmitted) return; // Prevent multiple submissions
    quizSubmitted = true;

    let score = 0;

    questions.forEach((q, index) => {
        const selected = document.querySelector(`input[name="q${index}"]:checked`);
        const resultElement = document.getElementById(`result-${index}`);

        if (selected) {
            let selectedLabel = document.getElementById(`label-${index}-${selected.value}`);
            let correctLabel = document.getElementById(`label-${index}-${q.correct_answer}`);

            if (selected.value === q.correct_answer) {
                score++;
                resultElement.innerHTML = `<span style="color: green;">✅ Correct</span>`;
                selectedLabel.classList.add("correct");
            } else {
                resultElement.innerHTML = `<span style="color: red;">❌ Wrong. Correct: ${q.correct_answer}</span>`;
                selectedLabel.classList.add("wrong");
                correctLabel.classList.add("correct");
            }
        } else {
            resultElement.innerHTML = `<span style="color: red;">⚠️ Not answered. Correct: ${q.correct_answer}</span>`;
            let correctLabel = document.getElementById(`label-${index}-${q.correct_answer}`);
            correctLabel.classList.add("correct");
        }
    });

    // Highlight Scorecard based on Performance
    let scoreText = `Your Score: ${score} / ${questions.length}`;
    let scoreElement = document.getElementById("score");

    if (score === questions.length) {
        scoreElement.innerHTML = `🏆 <span style="color: green;">Perfect Score! ${scoreText}</span>`;
    } else if (score >= (questions.length * 0.7)) {
        scoreElement.innerHTML = `😊 <span style="color: blue;">Great Job! ${scoreText}</span>`;
    } else if (score >= (questions.length * 0.4)) {
        scoreElement.innerHTML = `😐 <span style="color: orange;">Keep Practicing! ${scoreText}</span>`;
    } else {
        scoreElement.innerHTML = `😞 <span style="color: red;">Try Again! ${scoreText}</span>`;
    }

    // Enable Restart button after submitting
    document.getElementById("restart-btn").disabled = false;
}

// Restart Quiz - Only works after submitting
function restartQuiz() {
    if (!quizSubmitted) return; // Prevent restart before submission
    document.getElementById("quiz-container").innerHTML = "<p>Restarting quiz...</p>";
    document.getElementById("score").innerHTML = "";
    loadQuiz();
}

loadQuiz();
