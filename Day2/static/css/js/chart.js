const ctx = document.getElementById('chart');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Math","Science","English"],
        datasets: [{
            label: "Average Marks",
            data: [70,75,80]
        }]
    }
});