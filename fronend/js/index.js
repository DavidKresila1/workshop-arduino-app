document.addEventListener('DOMContentLoaded', function() {
    // Fetch temperature data from the Flask API
    fetch('http://127.0.0.1:3040/temperature')
        .then(response => response.json())
        .then(data => {
            // Update HTML elements with the temperature data and weather icon
            updateTemperature(data.temperature);
        })
        .catch(error => {
            console.error('Error fetching temperature data:', error);
            updateTemperatureError();
        });
});

function updateTemperature(temperature) {
    // Update the temperature element
    const temperatureElement = document.getElementById('temperature');
    temperatureElement.textContent = `${temperature} °C`;

    // Determine the weather icon based on temperature conditions
    const weatherIconElement = document.getElementById('weather-icon');
    if (temperature < 15) {
        weatherIconElement.className = 'weather-icon snow';
    } else if (temperature > 20) {
        weatherIconElement.className = 'weather-icon sun';
    } else {
        weatherIconElement.className = 'weather-icon cloud';
    }
}

function updateTemperatureError() {
    // Display an error message if fetching temperature data fails
    const temperatureElement = document.getElementById('temperature');
    temperatureElement.textContent = 'Failed to fetch temperature data';

    // Reset the weather icon to a default state or display an error icon
    const weatherIconElement = document.getElementById('weather-icon');
    weatherIconElement.className = 'error-icon';
}
