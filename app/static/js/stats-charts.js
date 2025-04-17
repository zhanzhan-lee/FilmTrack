document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('monthlyChart').getContext('2d');

    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(66, 133, 244, 0.3)'); // soft blue
    gradient.addColorStop(1, 'rgba(66, 133, 244, 0)');   // fade

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Monthly Trend',
                data: [20, 30, 25, 40, 35, 50, 60],
                fill: true,
                backgroundColor: gradient,
                borderColor: '#4285F4',
                borderWidth: 3,
                tension: 0.4,
                pointRadius: 0,
            }]
        },
        options: {
            plugins: {
                legend: { display: false },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { drawTicks: false, color: '#eee' },
                    ticks: { color: '#666', font: { family: 'Roboto' } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#666', font: { family: 'Roboto' } }
                }
            }
        }
    });

    // Donut chart
    const donutCtx = document.getElementById('donut-chart').getContext('2d');
    const donutChart = new Chart(donutCtx, {
        type: 'doughnut',
        data: {
            labels: ['A', 'B', 'C', 'D', 'E'],
            datasets: [{
                data: [20, 15, 25, 10, 30],
                backgroundColor: [
                    '#4A90E2',
                    '#5AA3F2',
                    '#6AB5FF',
                    '#8BC6FF',
                    '#A3D4FF'
                ],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '40%',
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
});

