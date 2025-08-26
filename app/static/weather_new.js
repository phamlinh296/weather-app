document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("tempChart");
    if (!canvas) return;

    const labels = JSON.parse(canvas.dataset.labels);
    const temps = JSON.parse(canvas.dataset.temps);

    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Nhiệt độ (°C)',
                data: temps,
                fill: true,
                backgroundColor: 'rgba(3,169,244,0.2)',
                borderColor: '#03a9f4',
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: { mode: 'index', intersect: false }
            },
            interaction: { mode: 'nearest', axis: 'x', intersect: false },
            scales: {
                y: { beginAtZero: false },
                x: { ticks: { autoSkip: true, maxTicksLimit: 12 } }
            }
        }
    });
});
