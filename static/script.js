let myChart;

document.getElementById('analyzeBtn').addEventListener('click', analyzeBrand);

function analyzeBrand() {
    const brand = document.getElementById('brandInput').value;
    if (!brand) {
        alert('Please enter a brand name');
        return;
    }

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ brand: brand }),
    })
    .then(response => response.json())
    .then(data => {
        updateChart(data.emo_dict);
        updateSampleTweet(data.sample_tweet);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function updateChart(emotions) {
    const ctx = document.getElementById('emotionChart').getContext('2d');
    
    if (myChart) {
        myChart.destroy();
    }
    
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(emotions),
            datasets: [{
                label: 'Emotion Percentage',
                data: Object.values(emotions),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(199, 199, 199, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Emotion Distribution'
                }
            }
        }
    });
}

function updateSampleTweet(tweet) {
    document.getElementById('tweetText').textContent = tweet;
}