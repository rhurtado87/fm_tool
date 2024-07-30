// static/js/charts.js

document.addEventListener('DOMContentLoaded', function() {
  // Data for the chart
  const historicalData = JSON.parse(document.getElementById('historicalData').textContent);

  // Prepare datasets for Chart.js
  const datasets = Object.keys(historicalData).map(symbol => {
      return {
          label: symbol,
          data: historicalData[symbol].map((price, index) => ({
              x: new Date(new Date().setDate(new Date().getDate() - (historicalData[symbol].length - 1 - index))),
              y: price
          })),
          fill: false,
          borderColor: getRandomColor(), // Function to generate random color
          tension: 0.1
      };
  });

  // Chart.js config
  const ctx = document.getElementById('stockChart').getContext('2d');
  const stockChart = new Chart(ctx, {
      type: 'line',
      data: {
          datasets: datasets
      },
      options: {
          scales: {
              x: {
                  type: 'time',
                  time: {
                      unit: 'day'
                  }
              },
              y: {
                  beginAtZero: false
              }
          }
      }
  });

  // Function to generate random colors
  function getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
  }
});
