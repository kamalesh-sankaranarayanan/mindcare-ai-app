function setupFocusFlow() {
  const arena = document.getElementById("flowArena"), target = document.getElementById("flowTarget");
  const overlay = document.getElementById("gameOverlay"), scoreEl = document.getElementById("score");
  const timeEl = document.getElementById("time"), comboEl = document.getElementById("combo");
  let score = 0, combo = 0, time = 30, timer, active = false;
  function move() {
    const pad = 45;
    target.style.left = `${pad + Math.random() * (arena.clientWidth - pad * 2)}px`;
    target.style.top = `${pad + Math.random() * (arena.clientHeight - pad * 2)}px`;
    target.classList.remove("pop"); void target.offsetWidth; target.classList.add("pop");
  }
  function finish() {
    active = false; clearInterval(timer); target.style.display = "none";
    saveGame("Focus Flow", score).then(data => {
      overlay.innerHTML = `<span class="result-spark">✦</span><h2>Flow complete</h2><p>You scored <b>${score}</b> points and earned ${data.xp_earned || 0} XP.</p><button class="btn btn-primary" onclick="location.reload()">Play again</button> <a class="btn secondary-btn" href="/hub">Mind Lab</a>`;
      overlay.classList.remove("hidden");
    });
  }
  document.getElementById("startGame").onclick = () => {
    score = combo = 0; time = 30; active = true; overlay.classList.add("hidden"); target.style.display = "grid"; move();
    timer = setInterval(() => { time--; timeEl.textContent = time; if (!time) finish(); }, 1000);
  };
  target.onclick = e => { e.stopPropagation(); if (!active) return; combo++; score += 10 + Math.min(combo, 10); scoreEl.textContent = score; comboEl.textContent = combo; move(); };
  arena.onclick = () => { if (active) { combo = 0; comboEl.textContent = 0; } };
}

function setupReactionGame() {
  const zone = document.getElementById("reactionZone"), text = document.getElementById("reactionText");
  const sub = document.getElementById("reactionSub"), start = document.getElementById("reactionStart");
  let round = 0, ready = false, started = 0, timeout, results = [];
  function next() {
    ready = false; zone.className = "reaction-zone waiting"; text.textContent = "Breathe and wait…"; sub.textContent = "Tap only when the space glows"; start.hidden = true;
    timeout = setTimeout(() => { ready = true; started = performance.now(); zone.className = "reaction-zone go"; text.textContent = "Tap now"; sub.textContent = "Respond with calm attention"; }, 1500 + Math.random() * 2500);
  }
  function finish() {
    const avg = Math.round(results.reduce((a,b)=>a+b,0)/results.length), best = Math.min(...results);
    document.getElementById("average").textContent = `${avg} ms`; document.getElementById("best").textContent = `${best} ms`;
    zone.className = "reaction-zone complete"; text.textContent = "Reset complete"; sub.textContent = `Average response: ${avg} ms`;
    saveGame("Reaction Reset", Math.max(0, 1000-avg)); start.textContent = "Play again"; start.hidden = false; round = 0; results = [];
  }
  start.onclick = e => { e.stopPropagation(); next(); };
  zone.onclick = () => {
    if (!start.hidden) return;
    if (!ready) { clearTimeout(timeout); text.textContent = "A little early"; sub.textContent = "Pause. Exhale. Let's try again."; setTimeout(next, 1000); return; }
    results.push(Math.round(performance.now()-started)); round++; document.getElementById("round").textContent = round;
    if (round === 5) finish(); else setTimeout(next, 700);
  };
}

function setupGroundingGame() {
  const steps = [
    [5,"◉","things you can see","Notice colors, shapes, light, and movement."],
    [4,"◇","things you can feel","Notice the chair, your clothes, air, or temperature."],
    [3,"⌁","things you can hear","Listen near, then farther away."],
    [2,"◌","things you can smell","Notice subtle scents or imagine two calming ones."],
    [1,"●","thing you can taste","Notice a current taste or take a sip of water."]
  ];
  let step = 0, checked = 0;
  const next = document.getElementById("groundNext"), checks = document.getElementById("senseChecks");
  function draw() {
    const [count,icon,title,hint] = steps[step]; checked = 0;
    document.getElementById("senseCount").textContent=count; document.getElementById("senseIcon").textContent=icon;
    document.getElementById("senseTitle").textContent=title; document.getElementById("senseHint").textContent=hint;
    document.getElementById("groundProgress").style.width=`${step*25}%`; next.disabled=true;
    checks.innerHTML = Array.from({length:count},(_,i)=>`<button aria-label="Mark item ${i+1}">${i+1}</button>`).join("");
    checks.querySelectorAll("button").forEach(b=>b.onclick=()=>{ if(!b.classList.contains("done")){b.classList.add("done");b.textContent="✓";checked++;next.disabled=checked<count;}});
  }
  next.onclick = () => {
    if (++step < steps.length) draw();
    else { document.getElementById("groundProgress").style.width="100%"; document.querySelector(".ground-card").innerHTML='<span class="result-spark">✦</span><h2>You are here.</h2><p>Take one slow breath. Notice how the present moment feels now.</p><a class="btn btn-primary" href="/hub">Finish quest</a>'; saveGame("Grounding Quest",100); }
  }; draw();
}
