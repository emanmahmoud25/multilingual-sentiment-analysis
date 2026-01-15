/* ================= ELEMENTS ================= */
const home = document.getElementById("home");
const textSection = document.getElementById("textSection");
const fileSection = document.getElementById("fileSection");

const fileInput = document.getElementById("fileInput");
const analyzeBtn = document.getElementById("analyzeBtn");

const status = document.getElementById("status");
const loader = document.getElementById("loader");

const summaryDiv = document.getElementById("summary");
const pieChart = document.getElementById("pieChart");

const langFilter = document.getElementById("langFilter");
const labelFilter = document.getElementById("labelFilter");

/* ================= TEXT ELEMENTS ================= */
const textInput = document.getElementById("textInput");
// textInput.addEventListener("input", () => {
//     const value = textInput.value.trim();
//     if (!value) return;

//     const firstChar = value[0];

//     if (/[\u0600-\u06FF]/.test(firstChar)) {
//         textInput.style.direction = "rtl";
//         textInput.style.textAlign = "right";
//     } else {
//         textInput.style.direction = "ltr";
//         textInput.style.textAlign = "left";
//     }
// });

const textLoader = document.getElementById("textLoader");
const textResults = document.getElementById("textResults");

const posPerc = document.getElementById("posPerc");
const negPerc = document.getElementById("negPerc");
const neuPerc = document.getElementById("neuPerc");
const finalDecision = document.getElementById("finalDecision");


let allRows = [];
let chart = null;

/* ================= NAV ================= */
function openText() {
    home.classList.add("hidden");
    fileSection.classList.add("hidden");
    textSection.classList.remove("hidden");
}

function openFile() {
    home.classList.add("hidden");
    textSection.classList.add("hidden");
    fileSection.classList.remove("hidden");
}

function goBack() {
    location.reload();
}

/* ================= UPLOAD ================= */
async function uploadFile() {
    const file = fileInput.files[0];
    if (!file) {
        alert("Choose a file first");
        return;
    }

    analyzeBtn.disabled = true;
    status.innerText = "Processing...";
    loader.classList.remove("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/api/analyze-file", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        console.log("🆔 Task ID:", data.task_id);

        pollTask(data.task_id);

    } catch (err) {
        console.error("Upload error:", err);
        status.innerText = "Upload failed ❌";
        loader.classList.add("hidden");
        analyzeBtn.disabled = false;
    }
}

/* ================= POLL ================= */
function pollTask(taskId) {
    const interval = setInterval(async () => {
        try {
            const res = await fetch(`/api/task-result/${taskId}`);
            const data = await res.json();

            console.log("📦 Task response:", data);

            if (data.status === "PENDING" || data.status === "Processing") {
                return;
            }

            if (data.status === "FAILURE") {
                clearInterval(interval);
                status.innerText = "Failed ❌";
                loader.classList.add("hidden");
                analyzeBtn.disabled = false;
                return;
            }

            if (data.status === "SUCCESS") {
                clearInterval(interval);

                const result = data.result;

                console.log("✅ RESULT:", result);

                allRows = result.data || [];

                renderSummary(result.summary);
                renderPie(result.summary);
                renderWordClouds(result.wordclouds);
                renderTable(allRows);

                loader.classList.add("hidden");
                analyzeBtn.disabled = false;
                status.innerText = "Done ✅";
            }

        } catch (err) {
            clearInterval(interval);
            console.error("Polling error:", err);
            status.innerText = "Error ❌";
            loader.classList.add("hidden");
            analyzeBtn.disabled = false;
        }
    }, 1500);
}

/* ================= SUMMARY ================= */
function renderSummary(summary) {
    document.getElementById("totalReviews").innerText =
    Object.values(summary).reduce((a, b) => a + b, 0);

    summaryDiv.innerHTML = "";
    

    if (!summary) return;

    for (let k in summary) {
        summaryDiv.innerHTML += `
            <div class="card">
                <h3>${k}</h3>
                <p>${summary[k]}</p>
            </div>
        `;
    }
}

/* ================= PIE ================= */
function renderPie(summary) {
    if (!summary) return;

    if (chart) chart.destroy();

    const total = Object.values(summary).reduce((a, b) => a + b, 0);
    const perc = Object.values(summary).map(v =>
        ((v / total) * 100).toFixed(1)
    );

    chart = new Chart(pieChart, {
        type: "pie",
        data: {
            labels: Object.keys(summary),
            datasets: [{ data: perc }]
        },
        options: {
          plugins: {
    datalabels: {
        formatter: v => v + "%",
        color: "#3102D8",   // موف فاتح
        font: {
            weight: "bold",
            size: 14
        }
    }
}

        },
        plugins: [ChartDataLabels]
    });
}

/* ================= WORDCLOUD ================= */
function renderWordClouds(wc) {
    if (!wc) return;

    document.getElementById("wc-positive").src =
        wc.positive ? `data:image/png;base64,${wc.positive}` : "";

    document.getElementById("wc-negative").src =
        wc.negative ? `data:image/png;base64,${wc.negative}` : "";

    document.getElementById("wc-neutral").src =
        wc.neutral ? `data:image/png;base64,${wc.neutral}` : "";
}

/* ================= TABLE ================= */
function renderTable(rows) {
    const tbody = document.querySelector("#resultsTable tbody");
    tbody.innerHTML = "";

    if (!rows || rows.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3">No data</td></tr>`;
        return;
    }

    rows.forEach(r => {
        tbody.innerHTML += `
            <tr>
                <td>${r.text}</td>
                <td>${r.sentiment}</td>
                <td>${r.score}</td>
            </tr>
        `;
    });
}

/* ================= FILTERS ================= */
function applyFilters() {
    let filtered = [...allRows];

    if (langFilter.value !== "all") {
        filtered = filtered.filter(r => {
            const ar = (r.text.match(/[\u0600-\u06FF]/g) || []).length;
            const en = (r.text.match(/[A-Za-z]/g) || []).length;
            return langFilter.value === "ar" ? ar > en : en >= ar;
        });
    }

    if (labelFilter.value !== "all") {
        filtered = filtered.filter(
            r => r.sentiment.toLowerCase() === labelFilter.value
        );
    }

    renderTable(filtered);
}

/* ================= DOWNLOAD ================= */
function downloadTable() {
    let csv = "\uFEFFText;Sentiment;Score\n";

    allRows.forEach(r => {
        csv += `"${r.text.replace(/"/g, '""')}";${r.sentiment};${r.score}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "sentiment_results.csv";
    a.click();
}
// Text Section
// ================= TEXT ANALYZE =================
async function analyzeText() {
    const text = textInput.value.trim();

    if (!text) {
        alert("Please write some text");
        return;
    }

    textLoader.classList.remove("hidden");
    textResults.classList.add("hidden");

    try {
        const res = await fetch("/api/analyze-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await res.json();
        console.log("📝 TEXT RESULT:", data);

        const probs = data.probs;

        const total =
    probs.Positive + probs.Negative + probs.Neutral;

const posPercent = (probs.Positive / total) * 100;
const negPercent = (probs.Negative / total) * 100;
const neuPercent = (probs.Neutral  / total) * 100;

posPerc.innerText = `Positive: ${posPercent.toFixed(1)}%`;
negPerc.innerText = `Negative: ${negPercent.toFixed(1)}%`;
neuPerc.innerText = `Neutral: ${neuPercent.toFixed(1)}%`;


        const decisionMap = {
    Positive: "This text expresses a positive sentiment 😊",
    Negative: "This text expresses a negative sentiment 😞",
    Neutral:  "This text is neutral and does not show a clear opinion 😐"
};

finalDecision.innerText =
    decisionMap[data.decision] || "Sentiment could not be determined";


        textResults.classList.remove("hidden");

    } catch (err) {
        console.error(err);
        alert("Analysis failed ❌");
    } finally {
        textLoader.classList.add("hidden");
    }
}
