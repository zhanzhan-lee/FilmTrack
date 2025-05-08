document.addEventListener('DOMContentLoaded', function() {
    const tiles = document.querySelectorAll('.shared-stats-tile');
    
    tiles.forEach(tile => {
        const shareId = tile.dataset.shareId;
        fetchAndRenderCharts(shareId);
    });
});

function fetchAndRenderCharts(shareId) {
    fetch(`/api/shared_stats/${shareId}`)
        .then(response => response.json())
        .then(data => {
            if (data.exposure) {
                renderBarChart(`exposure-chart-${shareId}`, {
                    labels: data.exposure.labels,
                    datasets: [{
                        data: data.exposure.values,
                        backgroundColor: '#278661',
                        borderRadius: 5
                    }]
                });
            }

            if (data.aperture) {
                renderDoughnutChart(`aperture-chart-${shareId}`, {
                    labels: data.aperture.labels,
                    datasets: [{
                        data: data.aperture.values,
                        backgroundColor: ['#278661', '#3A9B74', '#4CAF88', '#6BC19C', '#8CD4B0']
                    }]
                });
            }

            if (data.cameras) {
                renderBarChart(`camera-chart-${shareId}`, {
                    labels: data.cameras.labels,
                    datasets: [{
                        data: data.cameras.values,
                        backgroundColor: '#278661',
                        borderRadius: 5
                    }]
                });
            }

            // Add lens usage chart
            if (data.lenses) {
                renderBarChart(`lens-chart-${shareId}`, {
                    labels: data.lenses.labels,
                    datasets: [{
                        data: data.lenses.values,
                        backgroundColor: '#3A9B74', // Slightly different shade for distinction
                        borderRadius: 5
                    }]
                });
            }

            if (data.monthly_trend) {
                renderLineChart(`monthly-chart-${shareId}`, {
                    labels: data.monthly_trend.labels,
                    datasets: [{
                        data: data.monthly_trend.values,
                        borderColor: '#278661',
                        backgroundColor: 'rgba(39, 134, 97, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                });
            }
        })
        .catch(error => console.error('Error fetching shared stats:', error));
}

function renderBarChart(canvasId, data) {
    new Chart(document.getElementById(canvasId), {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderDoughnutChart(canvasId, data) {
    new Chart(document.getElementById(canvasId), {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%'
        }
    });
}

function renderLineChart(canvasId, data) {
    new Chart(document.getElementById(canvasId), {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            elements: {
                line: {
                    tension: 0.6 // Increased from 0.4 for smoother curves
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMin: Math.min(...data.datasets[0].data) * 0.8, // Add 20% padding at bottom
                    suggestedMax: Math.max(...data.datasets[0].data) * 1.2  // Add 20% padding at top
                }
            }
        }
    });
}