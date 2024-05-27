// fetch data from flask server
async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/request_data');
        const data = await response.json();
        // console.log(data);  // Logging the entire dictionary
        return data;
    } catch (error) {
        console.error('Error fetching game info:', error);
        return 'inactive'; // Default to 'inactive' on error
    }
}

// PAGINA WEB --> API.PY
function sendInteger(vote_id) {
  
    fetch('http://127.0.0.1:5000/submit_integer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ integer: vote_id })
    })
    .then(response => {
        console.log('riposta',response);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert(`Server response: ${data.status}`);
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
  }
