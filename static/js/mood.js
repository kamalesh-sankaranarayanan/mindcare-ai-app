async function saveMood() {
    const mood = document.getElementById("mood").value;
    const note = document.getElementById("moodNote").value;
    const status = document.getElementById("moodStatus");

    const response = await fetch("/save_mood", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({mood, note})
    });

    const data = await response.json();
    status.innerText = data.message;
    document.getElementById("moodNote").value = "";
}
