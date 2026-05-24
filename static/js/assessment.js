let currentQuestion = 0;

function showQuestion(index) {
    const pages = document.querySelectorAll(".question-page");

    pages.forEach((page, i) => {
        page.classList.toggle("active", i === index);
    });

    document.getElementById("progressText").innerText =
        `Question ${index + 1} of ${totalQuestions}`;

    document.getElementById("progressFill").style.width =
        `${((index + 1) / totalQuestions) * 100}%`;
}

function nextQuestion() {
    const pages = document.querySelectorAll(".question-page");
    const selected = pages[currentQuestion].querySelector("input[type='radio']:checked");

    if (!selected) {
        alert("Please select an answer before continuing.");
        return;
    }

    if (currentQuestion < totalQuestions - 1) {
        currentQuestion++;
        showQuestion(currentQuestion);
    }
}

function prevQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        showQuestion(currentQuestion);
    }
}

showQuestion(currentQuestion);
