const ctx = document.getElementById('myChart');

  new Chart(myChart, {
    type: 'doughnut',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: 'Stats de satisfaction',
        data: [1, 1, 1, 1, 1, 1],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        
      }
    }
  });