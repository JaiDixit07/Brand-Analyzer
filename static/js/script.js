let chart;

function analyzeBrand() {
    const brand = document.getElementById('brandInput').value;
    if (!brand) {
        showAlert('Please enter a brand name');
        return;
    }

    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({brand: brand}),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loader').classList.add('hidden');
        if (data.success) {
            displayResults(data.data);
        } else {
            showAlert('Error: ' + data.error);
        }
    })
    .catch(error => {
        document.getElementById('loader').classList.add('hidden');
        showAlert('Error: ' + error);
    });
}

function displayResults(data) {
    const resultsElement = document.getElementById('results');
    resultsElement.classList.remove('hidden');
    resultsElement.style.opacity = '0';
    
    // Display emotion chart
    const ctx = document.getElementById('emotionChart').getContext('2d');
    if (chart) {
        chart.destroy();
    }
    chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data.emo_dict),
            datasets: [{
                data: Object.values(data.emo_dict),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#dfe6e9'
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    // Display recommendations
    const recomDiv = document.getElementById('recommendationsList');
    recomDiv.innerHTML = '';
    for (const [key, value] of Object.entries(data.recom)) {
        const recomItem = document.createElement('div');
        recomItem.className = 'recommendation-item';
        recomItem.innerHTML = `
            <h3>${key}</h3>
            <p>${value}</p>
        `;
        recomDiv.appendChild(recomItem);
    }

    // Display sample tweet
    document.getElementById('sampleTweet').textContent = data.sample_tweet;

    // Fade in results
    setTimeout(() => {
        resultsElement.style.transition = 'opacity 0.5s ease-in-out';
        resultsElement.style.opacity = '1';
    }, 100);
}

function showAlert(message) {
    const alertElement = document.createElement('div');
    alertElement.className = 'alert';
    alertElement.textContent = message;
    document.body.appendChild(alertElement);

    setTimeout(() => {
        alertElement.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(alertElement);
        }, 500);
    }, 3000);
}
