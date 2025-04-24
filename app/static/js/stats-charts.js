function monthlyTrendChart() {
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
          responsive: true,
          cutout: '40%',
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
    })
  .catch(error => console.error('Error fetching aperture distribution data:', error));
}

function gearChart(elementID) {
  fetch('/api/' + elementID + '-preference')
    .then(response => response.json())
    .then(data => {
      const ctx = document.getElementById(elementID).getContext('2d');
      const bg = ctx.createLinearGradient(0, 0, 0, 300);
      bg.addColorStop(0, '#5eb3f4');
      bg.addColorStop(1, '#9ccdf1');

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

function horizontalBarChart(data) {
  const chart = document.querySelector("#shutter-speed");

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

function shutterSpeedDistributionChart() {
  fetch('/api/shutter-speed-distribution')
    .then(response => response.json())
    .then(data => {
      horizontalBarChart(data);
    })
  .catch(error => console.error('Error fetching shutter speeds: ', error));
}

document.addEventListener('DOMContentLoaded', () => {
  shutterSpeedDistributionChart();

  monthlyTrendChart();
  apertureDistributionChart();

  gearChart('lenses-chart');
  gearChart('film-chart');
  gearChart('cameras-chart');

  locationMap();
});