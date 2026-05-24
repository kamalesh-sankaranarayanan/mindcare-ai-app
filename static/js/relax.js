function startActivity(type){

    let box = document.getElementById("activityBox");

    // MEDITATION
    if(type === "meditation"){

        box.innerHTML = `

        <div class="interactive-section">

            <h2>🧘 Meditation Zone</h2>

            <p>Relax your mind and breathe slowly.</p>

            <audio controls autoplay loop>
                <source src="/static/audio/meditation.mp3" type="audio/mp3">
            </audio>
            <audio controls autoplay loop>
                <source src="/static/audio/relax.mp3" type="audio/mp3">
            </audio>

            <br><br>

            <video width="500" controls autoplay loop>
                <source src="/static/videos/hill.mp4" type="video/mp4">
            </video>
            <video width="500" controls autoplay loop>
                <source src="/static/videos/rain.mp4" type="video/mp4">
            </video>

        </div>
        `;
    }

    // BREATHING
    else if(type === "breathing"){

        box.innerHTML = `

        <div class="interactive-section">

            <h2>🌿 Breathing Exercise</h2>

            <div class="breathing-circle"></div>

            <h3>Inhale... Exhale...</h3>

        </div>
        `;
    }

    // JOURNAL
    else if(type === "journal"){

        box.innerHTML = `

        <div class="interactive-section">

            <h2>📝 Journal</h2>

            <textarea
                placeholder="Write your thoughts here..."
                class="journal-box"
            ></textarea>

            <br>

            <button class="save-btn">
                Save Journal
            </button>

        </div>
        `;
    }

    // MEMORY GAME
    else if(type === "memory"){

        box.innerHTML = `

        <div class="interactive-section">

            <h2>🎮 Memory Game</h2>

            <div class="memory-grid" id="memoryGrid"></div>

        </div>
        `;

        startMemoryGame();
    }

    // STRESS GUIDE
    else if(type === "placement"){

        box.innerHTML = `

        <div class="interactive-section">

            <h2>🎯 Placement Stress Guide</h2>

            <ul class="tips">

                <li>Take short breaks while studying</li>

                <li>Do not compare yourself constantly</li>

                <li>Practice aptitude daily</li>

                <li>Sleep properly before interviews</li>

                <li>One rejection does not define you</li>

            </ul>

        </div>
        `;
    }
    else if(type === "reaction"){

    box.innerHTML = `

    <div class="interactive-section">

        <h2>⚡ Reaction Game</h2>

        <button id="reactionBtn">
            Wait for Green...
        </button>

    </div>
    `;

    let btn = document.getElementById("reactionBtn");

    setTimeout(()=>{

        btn.style.background = "green";

        btn.innerHTML = "CLICK NOW!";

        let start = Date.now();

        btn.onclick = ()=>{

            let time = Date.now() - start;

            alert("Reaction Time: " + time + " ms");
        }

    }, 3000);
}
else if(type === "funny"){

    box.innerHTML = `

    <div class="interactive-section">

        <h2>😂 Relaxing Video</h2>

        <video width="500" controls autoplay>

            <source src="/static/videos/cat.mp4" type="video/mp4">

        </video>
        <video width="500" controls autoplay>

            <source src="/static/videos/dog.mp4" type="video/mp4">

        </video>
        <video width="500" controls autoplay>

            <source src="/static/videos/cute.mp4" type="video/mp4">

        </video>

    </div>
    `;
}
}


// ================= MEMORY GAME =================

function startMemoryGame(){

    const emojis = [
        "😀","😀",
        "🔥","🔥",
        "🎮","🎮",
        "🌟","🌟"
    ];

    let shuffled = emojis.sort(() => Math.random() - 0.5);

    let grid = document.getElementById("memoryGrid");

    shuffled.forEach(emoji => {

        let card = document.createElement("div");

        card.className = "memory-card";

        card.innerHTML = "?";

        card.onclick = () => {

            card.innerHTML = emoji;
        };

        grid.appendChild(card);
    });
}