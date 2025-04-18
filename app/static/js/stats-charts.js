document.addEventListener('DOMContentLoaded', () => {
    // Monthly trend chart
    const ctx = document.getElementById('monthly-trend').getContext('2d');

    // TODO: Fix this
    document.getElementById('monthly-trend').height = 150;
    document.getElementById('monthly-trend').width = 600;

    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(39, 134, 97, 0.3)');
    gradient.addColorStop(1, 'rgba(39, 134, 97, 0)'); 


    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Monthly Trend',
                data: [20, 30, 25, 40, 35, 50, 60],
                fill: true,
                backgroundColor: gradient,
                borderColor: '#278661',
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
                    ticks: { display: false }
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
            labels: ['f/2.8', 'f/4', 'f/5.6', 'f/8', 'f/16'],
            datasets: [{
                data: [20, 15, 25, 10, 30],
                backgroundColor: [
                    '#278661',
                    '#3A9B74',
                    '#4CAF88', 
                    '#6BC19C',
                    '#8CD4B0'
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

    const lensCtx = document.getElementById('lenses-chart').getContext('2d');
    const bg = lensCtx.createLinearGradient(0, 0, 0, 300);
    bg.addColorStop(0, '#5eb3f4');
    bg.addColorStop(1, '#9ccdf1'); 

    new Chart(lensCtx, {
      type: 'bar',
      data: {
        labels: ['A', 'B', 'C'],
        datasets: [{
          data: [12, 19, 3],
          backgroundColor: bg,
          borderRadius: 5,
        }]
      },
      options: {
        responsive: true,
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: false
          }
        },
        scales: {
          x: {
            display: false
          },
          y: {
            display: false
          }
        }
      }
    });

    const filmCtx = document.getElementById('film-chart').getContext('2d');
    const bg2 = cameraCtx.createLinearGradient(0, 0, 0, 300);
    bg2.addColorStop(0, '#5eb3f4');
    bg2.addColorStop(1, '#9ccdf1'); 

    new Chart(filmCtx, {
      type: 'bar',
      data: {
        labels: ['A', 'B', 'C'],
        datasets: [{
          data: [12, 19, 3],
          backgroundColor: bg2,
          borderRadius: 5,
        }]
      },
      options: {
        responsive: true,
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: false
          }
        },
        scales: {
          x: {
            display: false
          },
          y: {
            display: false
          }
        }
      }
    });

    const cameraCtx = document.getElementById('cameras-chart').getContext('2d');
    const blueGradient = cameraCtx.createLinearGradient(0, 0, 0, 300);
    blueGradient.addColorStop(0, '#5eb3f4');
    blueGradient.addColorStop(1, '#9ccdf1'); 

    new Chart(cameraCtx, {
      type: 'bar',
      data: {
        labels: ['A', 'B', 'C'],
        datasets: [{
          data: [12, 19, 3],
          backgroundColor: blueGradient,
          borderRadius: 5,
        }]
      },
      options: {
        responsive: true,
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: false
          }
        },
        scales: {
          x: {
            display: false
          },
          y: {
            display: false
          }
        }
      }
    });

    var map = L.map('map').setView([-25.2744, 133.7751], 4); // Australia, baby

    // 🗺️ MINIMAL TILE LAYER
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap & Carto',
      maxZoom: 18
    }).addTo(map);

    // 📍 SPICY MAP PINS
    const locations = [
      { name: "Sydney", lat: -33.8688, lng: 151.2093 },
      { name: "Melbourne", lat: -37.8136, lng: 144.9631 },
      { name: "Perth", lat: -31.9505, lng: 115.8605 }
    ];

    locations.forEach(loc => {
      L.marker([loc.lat, loc.lng])
        .addTo(map)
        .bindPopup(`<b>${loc.name}</b> 🦘`); //TODO: Extend this to having photo preview?
    });


});

