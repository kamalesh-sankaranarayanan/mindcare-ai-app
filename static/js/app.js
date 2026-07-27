(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem("mindcare-theme");
  if (saved) root.dataset.theme = saved;
  document.getElementById("themeToggle")?.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    localStorage.setItem("mindcare-theme", next);
  });
})();

async function saveGame(game, score) {
  try {
    const response = await fetch("/api/game-session", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({game, score})
    });
    return await response.json();
  } catch (_) {
    return {message: "Session complete"};
  }
}
