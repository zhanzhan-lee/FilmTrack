document.addEventListener('DOMContentLoaded', function() {
    const tiles = document.querySelectorAll('.shared-stats-tile');
    
    tiles.forEach(tile => {
        const shareId = tile.dataset.shareId;
        fetchAndRenderCharts(shareId);
    });
});

// Define color palettes for different tiles
const colorPalettes = {
    0: { // Green palette
        primary: '#278661',
        shades: ['#278661', '#3A9B74', '#4CAF88', '#6BC19C', '#8CD4B0'],
        background: 'rgba(39, 134, 97, 0.1)'
    },
    1: { // Red palette
        primary: '#B54E4E',
        shades: ['#B54E4E', '#C66262', '#D67676', '#E78A8A', '#F89E9E'],
        background: 'rgba(181, 78, 78, 0.1)'
    },
    2: { // Purple palette
        primary: '#7C4E9E',
        shades: ['#7C4E9E', '#8F62B1', '#A276C4', '#B58AD7', '#C89EEA'],
        background: 'rgba(124, 78, 158, 0.1)'
    },
    3: { // Blue palette
        primary: '#4E77B5',
        shades: ['#4E77B5', '#628AC6', '#769DD7', '#8AB0E7', '#9EC3F8'],
        background: 'rgba(78, 119, 181, 0.1)'
    }
};

function fetchAndRenderCharts(shareId) {
    fetch(`/api/shared_stats/${shareId}`)
        .then(response => response.json())
        .then(data => {
            const tileIndex = Array.from(document.querySelectorAll('.shared-stats-tile'))
                                 .findIndex(tile => tile.dataset.shareId === shareId);
            const palette = colorPalettes[tileIndex % Object.keys(colorPalettes).length];

            if (data.exposure) {
                renderBarChart(`exposure-chart-${shareId}`, {
                    labels: data.exposure.labels,
                    datasets: [{
                        data: data.exposure.values,
                        backgroundColor: palette.shades[2], // Using middle shade
                        borderRadius: 5
                    }]
                });
            }

            if (data.aperture) {
                renderDoughnutChart(`aperture-chart-${shareId}`, {
                    labels: data.aperture.labels,
                    datasets: [{
                        data: data.aperture.values,
                        backgroundColor: palette.shades
                    }]
                });
            }

            if (data.cameras) {
                renderBarChart(`camera-chart-${shareId}`, {
                    labels: data.cameras.labels,
                    datasets: [{
                        data: data.cameras.values,
                        backgroundColor: palette.shades[0], // Using darkest shade
                        borderRadius: 5
                    }]
                });
            }

            if (data.lenses) {
                renderBarChart(`lens-chart-${shareId}`, {
                    labels: data.lenses.labels,
                    datasets: [{
                        data: data.lenses.values,
                        backgroundColor: palette.shades[1], // Using second shade
                        borderRadius: 5
                    }]
                });
            }

            if (data.monthly_trend) {
                const ctx = document.getElementById(`monthly-chart-${shareId}`).getContext('2d');
                const gradient = ctx.createLinearGradient(0, 0, 0, 300);
                gradient.addColorStop(0, palette.shades[3]);
                gradient.addColorStop(1, 'rgba(255, 255, 255, 0.4)');

                renderLineChart(`monthly-chart-${shareId}`, {
                    labels: data.monthly_trend.labels,
                    datasets: [{
                        data: data.monthly_trend.values,
                        borderColor: palette.primary,
                        backgroundColor: gradient,
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 0
                    },],
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
            layout: {
                padding: {
                    top: 20,
                    bottom: 25  // Increased bottom padding
                }
            },
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: { drawTicks: false },
                    ticks: {
                        padding: 10  // Add padding to axis ticks
                    }
                },
                x: { 
                    grid: { display: false },
                    ticks: { 
                        font: { size: 10 },
                        padding: 10  // Add padding to axis ticks
                    }
                }
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
            layout: {
                padding: {
                    top: 20,
                    bottom: 25  // Added bottom padding
                }
            },
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
            layout: {
                padding: {
                    top: 20,
                    bottom: 25
                }
            },
            plugins: {
                datalabels: false,
                tooltip: {
                    enabled: true,
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return `Photos: ${context.raw}`;
                        }
                    }
                },
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: Math.max(...data.datasets[0].data) + 2, // Dynamic max scale
                    grid: { drawTicks: false, color: '#eee' },
                    ticks: { display: false }
                },
                x: {
                    grid: { display: false },
                    ticks: { 
                        color: '#666',
                        font: { 
                            size: 10,
                            family: 'Roboto'
                        }
                    }
                }
            }
        }
    });
}