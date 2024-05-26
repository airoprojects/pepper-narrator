
function fetchStatus() {
    fetch('http://127.0.0.1:5000/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('message').innerText = data.message;
            document.getElementById('number').innerText = data.number;
        })
        .catch(error => console.error('Error:', error));
  }