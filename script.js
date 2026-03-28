let performanceChart = null;

// Initialize Chart.js Radar
function initChart() {
    const canvas = document.getElementById('performanceChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    performanceChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Study Hours', 'Attendance', 'Assignments', 'Exams', 'Motivation', 'Stress'],
            datasets: [{
                label: 'Student Metrics',
                data: [0, 0, 0, 0, 0, 0],
                fill: true,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgb(59, 130, 246)',
                pointBackgroundColor: 'rgb(59, 130, 246)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(59, 130, 246)'
            }, {
                label: 'Success Benchmark',
                data: [7, 85, 80, 75, 2, 1], 
                fill: true,
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderColor: 'rgba(16, 185, 129, 0.5)',
                borderDash: [5, 5],
                pointRadius: 0
            }]
        },
        options: {
            elements: { line: { borderWidth: 3 } },
            scales: {
                r: {
                    angleLines: { color: '#334155' },
                    grid: { color: '#334155' },
                    pointLabels: { color: '#94a3b8', font: { size: 12 } },
                    ticks: { display: false },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: { legend: { labels: { color: '#f8fafc' } } }
        }
    });
}

function updateChart(data) {
    if (!performanceChart) initChart();
    
    const normalizedData = [
        (data.StudyHours / 12) * 100, 
        data.Attendance,
        data.AssignmentCompletion,
        data.ExamScore,
        (data.Motivation / 3) * 100,
        (data.StressLevel / 3) * 100
    ];
    
    performanceChart.data.datasets[0].data = normalizedData;
    performanceChart.update();
}

async function loadHistory() {
    try {
        const response = await fetch('/history');
        if (!response.ok) return;
        const records = await response.json();
        
        const historyBody = document.getElementById('history-body');
        if (!historyBody) return;
        historyBody.innerHTML = ''; 
        
        records.forEach(record => {
            const row = document.createElement('tr');
            const statusClass = record.at_risk ? 'badge-fail' : 'badge-pass';
            const statusText = record.at_risk ? 'At Risk' : 'Healthy';
            
            row.innerHTML = `
                <td>${record.timestamp}</td>
                <td><strong>${record.student_name}</strong></td>
                <td>Avg Grade: ${record.exam_score}%</td>
                <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                <td><strong>${Math.round(record.risk_probability * 100)}%</strong></td>
            `;
            historyBody.appendChild(row);
        });
    } catch (e) {
        console.error("History load error:", e);
    }
}

document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('span');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-container');
    const riskBadge = document.getElementById('risk-badge');
    const riskProb = document.getElementById('risk-prob');
    const recList = document.getElementById('recommendation-list');

    btnText.style.display = 'none';
    loader.style.display = 'block';
    submitBtn.disabled = true;

    const formData = new FormData(e.target);
    const payload = {};
    for (let [key, value] of formData.entries()) {
        payload[key] = (key === 'StudentName') ? value : Number(value);
    }

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('API error');

        const result = await response.json();
        
        if (result.at_risk) {
            riskBadge.textContent = "At Risk (Fail)";
            riskBadge.className = "risk-badge badge-risk";
        } else {
            riskBadge.textContent = "Not At Risk (Pass)";
            riskBadge.className = "risk-badge badge-safe";
        }

        riskProb.textContent = Math.round(result.risk_probability * 100) + '%';

        recList.innerHTML = '';
        result.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });

        const insightsContainer = document.getElementById('llm-insights-container');
        const insightsText = document.getElementById('llm-insights-text');
        
        if (result.llm_insights) {
            insightsText.innerHTML = result.llm_insights.replace(/\n/g, '<br>');
            insightsContainer.style.display = 'block';
            window.currentStudentContext = JSON.stringify(payload) + " | LLM Feedback: " + result.llm_insights;
        }

        updateChart(payload);
        loadHistory(); 

        resultContainer.style.display = 'block';
        setTimeout(() => resultContainer.classList.add('animate-fade-in'), 10);
        setTimeout(() => resultContainer.scrollIntoView({ behavior: 'smooth', block: 'end' }), 100);

    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        btnText.style.display = 'block';
        loader.style.display = 'none';
        submitBtn.disabled = false;
    }
});

window.onload = () => {
    initChart();
    loadHistory();
};
