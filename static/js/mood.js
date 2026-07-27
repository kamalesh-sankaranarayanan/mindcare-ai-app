async function saveMood() {
    const selected = document.querySelector("#moodPicker button.selected");
    const mood = selected?.dataset.mood;
    const note = document.getElementById("moodNote").value;
    const status = document.getElementById("moodStatus");

    if (!mood) { status.innerText = "Choose the feeling that fits best."; return; }
    const response = await fetch("/save_mood", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({mood, note})
    });

    const data = await response.json();
    status.innerText = data.message;
    document.getElementById("moodNote").value = "";
}

document.querySelectorAll("#moodPicker button").forEach(button => {
    button.addEventListener("click", () => {
        document.querySelectorAll("#moodPicker button").forEach(item => item.classList.remove("selected"));
        button.classList.add("selected");
    });
});
