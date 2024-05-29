// fetch data from flask server
// async function fetchData() {
//     try {
//         const response = await fetch('redis://localhost:6379/request_data');
//         const data = await response.json();
//         // console.log(data);  // Logging the entire dictionary
//         return data;
//     } catch (error) {
//         console.error('Error fetching game info:', error);
//         return 'inactive'; // Default to 'inactive' on error
//     }
// }

// // PAGINA WEB --> API.PY
// function sendInteger(vote_id) {
  
//     fetch('redis://localhost:6379/submit_integer', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ integer: vote_id })
//     })
//     .then(response => {
//         console.log('riposta',response);
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log('Success:', data);
//         alert(`Server response: ${data.status}`);
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//         alert('An error occurred. Please try again.');
//     });
//   }



  //PROVA
  // Function to fetch initial data from the Flask server
async function fetchData() {
    try {
        const response = await fetch('http://192.168.60.17:5000/request_data');  // Flask server URL
        const data = await response.json();
        console.log(data);  // Logging the entire dictionary
        updatePage(data);
    } catch (error) {
        console.error('Error fetching game info:', error);
        updatePage('inactive');  // Default to 'inactive' on error
    }
}

// Function to send integer vote to the Flask server
function sendInteger(vote_id) {
    fetch('http://192.168.60.17:5000/submit_integer', {  // Flask server URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ integer: vote_id })
    })
    .then(response => {
        console.log('response', response);
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

// Function to update the page with new data
function updatePage(data) {
    // Implement your logic to update the page with the fetched data
    document.getElementById('gameInfo').textContent = JSON.stringify(data, null, 2);
}

// Set up an EventSource to listen for updates from the server
const eventSource = new EventSource('http://192.168.60.17:5000/stream');  // Flask server URL

eventSource.onmessage = function(event) {
    const gameInfo = JSON.parse(event.data);
    updatePage(gameInfo);
};

eventSource.onerror = function(err) {
    console.error("EventSource failed:", err);
};

// Fetch initial data when the page loads
fetchData();

