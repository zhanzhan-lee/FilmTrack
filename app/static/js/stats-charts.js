Chart.register(ChartDataLabels);

function monthlyTrendChart() {
  // Everything in these functions follows the same structure 
  fetch('/api/monthly-trend')
    .then(response => response.json())
    .then(data => {
      const ctx = document.getElementById('monthly-trend').getContext('2d');

      const gradient = ctx.createLinearGradient(0, 0, 0, 300);
      gradient.addColorStop(0, 'rgba(39, 134, 97, 0.3)');
      gradient.addColorStop(1, 'rgba(39, 134, 97, 0)');

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Monthly Trend',
            data: data.data,
            fill: true,
            backgroundColor: gradient,
            borderColor: '#278661',
            borderWidth: 3,
            tension: 0.4,
            pointRadius: 0,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
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
            legend: { display: false },
          },
          scales: {
            y: {
              beginAtZero: true,
              suggestedMax: Math.max(...data.data) + 2, // Dynamically adjust the max scale
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
    })
    .catch(error => console.error('Error fetching monthly trend data:', error));
}

function apertureDistributionChart() {
  fetch('/api/aperture-distribution')
    .then(response => response.json())
    .then(data => {
      const ctx = document.getElementById('donut-chart').getContext('2d');
      console.log(Chart.registry.plugins);

      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: data.labels,
          datasets: [{
            data: data.data,
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
          hover: {
            mode: 'nearest', // Highlight the nearest segment
            intersect: true
          },
          responsive: true,
          cutout: '40%',
          plugins: {
            datalabels: {
              color: '#eee', // Text color
              font: {
                size: 12,
                weight: 'bold'
              },
              formatter: function(value, context) {
                return context.chart.data.labels[context.dataIndex]; // Use the label instead of the value
              }
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw || 0;
                  return ` ${value} photos`; // TODO: Make singular when only 1 photo
                }
              }
            },
            legend: {
              display: false
            }
          },
        }
      });
    })
  .catch(error => console.error('Error fetching aperture distribution data:', error));
}

function updateFilmLeaderboard() {
  fetch('/api/film-chart-preference')
    .then(response => response.json())
    .then(data => {
      const leaderboard = document.querySelector('#favourite-film .chart-container');

      console.log(data);

      data.labels.forEach((filmName, index) => {
        const position = document.createElement('div');
        position.className = 'film-leaderboard';
        if (index == 0)
        {
          position.innerHTML = `
          <div class="film-leaderboard-position">
            <img src="${data.images[index]}" id="favourite-film-img">
              <h1>#1</h1>
              <p>${filmName}</p>
            </div>
          </div>
          `;
        }
        else {
          position.innerHTML = `
          <div class="film-leaderboard-position">
            <h3>#${index+1} ${filmName}</h3>
          </div>
        `;
        }

        leaderboard.append(position)
      });
    })
    .catch(error => console.error('Error fetching film leaderboard:', error));
}

function gearChart(elementID) {
  fetch('/api/' + elementID + '-preference')
    .then(response => response.json())
    .then(data => {
      const ctx = document.getElementById(elementID).getContext('2d');
      const bg = ctx.createLinearGradient(0, 0, 0, 300);
      bg.addColorStop(0, '#2c5282');  // Changed to darker blue
      bg.addColorStop(1, '#4299e1');  // Changed to medium blue

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            data: data.data,
            backgroundColor: bg,
            borderRadius: 5,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          animation: {
            duration: 1000,
            easing: 'easeOutQuart'
          },
          plugins: {
            legend: {
              display: false
            },
            datalabels: {
              color: '#eee', // Text color
              font: {
                size: 12,
                weight: 'bold'
              },
              formatter: function(value) {
                return value;
              }
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw || 0;
                  return ` ${value} photos`; // TODO: Make singular when only 1 photo
                }
              }
            },
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
    })
  .catch(error => console.error('Error fetching aperture distribution data:', error));
}

function locationMap() {
  const map = L.map('map').setView([-25.2744, 133.7751], 4); // Australia, baby

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
}

function horizontalBarChart(data, chartClass) {
  const chart = document.querySelector(chartClass);

  data.labels.forEach((label, index) => {
    const bar = document.createElement('div');
    bar.className = 'bar';

    bar.innerHTML = `
      <div class="bar-label">${label}</div>
      <div class="bar-wrapper">
        <div class="bar-fill" data-value="${data.data[index]}"></div>
      </div>
    `;

    // Slightly delay the animation to ensure it plays
    setTimeout(() => {
      barFill = bar.querySelector('.bar-fill');
      barFill.style.width = (data.data[index] / data.total * 100) + '%'; // As a percentage of the total
    }, 100);
    chart.append(bar);
  })
}

document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/shutter-speed-distribution')
    .then(response => response.json())
    .then(data => {
      horizontalBarChart(data, "#shutter-speed");
    })
  .catch(error => console.error('Error fetching shutter speeds: ', error));

  fetch('/api/top-locations')
    .then(response => response.json())
    .then(data => {
      horizontalBarChart(data, "#location-stats");
    })
  .catch(error => console.error('Error fetching location stats: ', error));

  monthlyTrendChart();
  apertureDistributionChart();
  updateFilmLeaderboard();

  gearChart('lenses-chart');
  gearChart('film-chart');
  gearChart('cameras-chart');

  locationMap();
});