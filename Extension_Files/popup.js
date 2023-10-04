document.addEventListener('DOMContentLoaded', function () {
    const cityInput = document.getElementById('cityInput');
    const getWeatherButton = document.getElementById('getWeatherButton');
    const weatherResult = document.getElementById('weatherResult');
  
    getWeatherButton.addEventListener('click', function () {
      const city = cityInput.value;
      if (city == undefined) {
        fetch(`http://localhost:8000/weather`)
          .then(response => response.json())
          .then(data => {
            weatherResult.textContent = JSON.stringify(data, null, 2);
          });
      }
      else {
        fetch(`http://localhost:8000/weather/${city}`)
          .then(response => response.json())
          .then(data => {
            weatherResult.textContent = JSON.stringify(data, null, 2);
          });
      }
    });
  });
  