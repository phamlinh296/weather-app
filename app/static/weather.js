document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('tempChart');
    if (!ctx) return; // Nếu không có chart, thôi

    const labels = JSON.parse(ctx.dataset.labels);
    const temps = JSON.parse(ctx.dataset.temps);

    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Nhiệt độ (°C)',
                data: temps,
                fill: true,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                tooltip: { mode: 'index', intersect: false }
            },
            interaction: { mode: 'nearest', intersect: false },
            scales: {
                y: { beginAtZero: false }
            }
        }
    });
});
