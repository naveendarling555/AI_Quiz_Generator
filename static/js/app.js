let currentQuiz = null;

const $ = (id) => document.getElementById(id);

const sampleText = `Artificial intelligence is a field of computer science.
Machine learning is a subset of artificial intelligence that enables systems to learn from data.
Natural language processing is a branch of artificial intelligence that helps computers process human language.
Tokenization is the process of breaking text into smaller units called tokens.
A stop word is a common word that may be removed during text preprocessing.
TF-IDF is a statistical technique used to estimate the importance of words in documents.
A Flask application is a Python web application that can expose routes and return web pages.
Information retrieval refers to finding relevant information from a collection of documents.`;

$("sampleBtn").addEventListener("click", () => {
    $("content").value = sampleText;
    updateCount();
});

$("content").addEventListener("input", updateCount);

function updateCount() {
    $("charCount").textContent = `${$("content").value.length} characters`;
}

function selectedTypes() {
    return [...document.querySelectorAll(".check input:checked")].map(x => x.value);
}

$("generateBtn").addEventListener("click", async () => {
    const text = $("content").value.trim();
    if (!text) return showMessage("Please enter educational content first.");

    const types = selectedTypes();
    if (!types.length) return showMessage("Select at least one question type.");

    setBusy(true);
    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                text,
                count: Number($("count").value),
                difficulty: $("difficulty").value,
                types
            })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Quiz generation failed.");
        currentQuiz = data;
        renderQuiz(data);
        $("quizSection").classList.remove("hidden");
        $("quizSection").scrollIntoView({behavior:"smooth"});
        showMessage("");
    } catch (error) {
        showMessage(error.message);
    } finally {
        setBusy(false);
    }
});

function renderQuiz(quiz) {
    $("analysis").innerHTML = `
        <b>${quiz.question_count} questions generated.</b>
        &nbsp; ${quiz.analysis.words} words · ${quiz.analysis.sentences} sentences ·
        ${quiz.analysis.keywords.length} keywords ·
        spaCy model: ${quiz.analysis.spacy_model_loaded ? "loaded" : "fallback mode"}
    `;

    const form = $("quizForm");
    form.innerHTML = "";

    quiz.questions.forEach((q, index) => {
        const wrapper = document.createElement("div");
        wrapper.className = "question";

        const meta = document.createElement("div");
        meta.className = "qmeta";
        meta.textContent = `Question ${index + 1} · ${q.type.replace("_", " ")} · ${q.difficulty}`;

        const title = document.createElement("h3");
        title.textContent = q.question;

        wrapper.appendChild(meta);
        wrapper.appendChild(title);

        if (q.type === "fill_blank") {
            const input = document.createElement("input");
            input.className = "text-answer";
            input.name = q.id;
            input.placeholder = "Type your answer";
            wrapper.appendChild(input);
        } else {
            q.options.forEach((option, i) => {
                const label = document.createElement("label");
                label.className = "option";
                const input = document.createElement("input");
                input.type = "radio";
                input.name = q.id;
                input.value = option;
                if (i === 0) input.autocomplete = "off";
                label.appendChild(input);
                const span = document.createElement("span");
                span.textContent = option;
                label.appendChild(span);
                wrapper.appendChild(label);
            });
        }

        form.appendChild(wrapper);
    });

    $("result").classList.add("hidden");
}

$("submitBtn").addEventListener("click", async () => {
    if (!currentQuiz) return;
    const responses = {};

    currentQuiz.questions.forEach(q => {
        const field = document.querySelector(`[name="${q.id}"]`);
        responses[q.id] = field ? field.value : "";
    });

    const response = await fetch("/api/evaluate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({quiz: currentQuiz, responses})
    });
    const result = await response.json();

    $("result").innerHTML = `
        <div class="score">${result.percentage}%</div>
        <p><b>${result.correct}</b> correct out of <b>${result.total}</b>.</p>
        <p>${result.recommendation}</p>
    `;
    $("result").classList.remove("hidden");
    $("result").scrollIntoView({behavior:"smooth", block:"center"});
});

$("exportBtn").addEventListener("click", async () => {
    if (!currentQuiz) return;
    const response = await fetch("/api/export", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({quiz: currentQuiz})
    });
    if (!response.ok) return showMessage("Could not export the quiz.");
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "generated_quiz.json";
    a.click();
    URL.revokeObjectURL(url);
});

function showMessage(message) {
    const el = $("message");
    el.textContent = message;
    el.classList.toggle("hidden", !message);
}

function setBusy(busy) {
    const btn = $("generateBtn");
    btn.disabled = busy;
    btn.innerHTML = busy ? "Generating quiz..." : "Generate AI Quiz <span>→</span>";
}
