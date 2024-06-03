async function fetchData() {
    const response = await fetch(('http://'+host_ip+':5000/request_data'));  // Flask server URL
    const data = await response.json();
    console.log(data);  // Logging the entire dictionary
    return data
}

// Function to send integer vote to the Flask server
function sendInteger(vote_id) {
    fetch('http://'+host_ip+':5000/submit_integer', {  // Flask server URL
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


// get current id
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Generate a list of player
function generatePlayersList(players, playerId, alive) {
    const playerList = document.getElementById('voting');
    if (!playerList) {
        console.error('Element with id "voting" not found');
        return;
    }
    playerList.innerHTML = '';

    // Create the select element
    const select = document.createElement('select');
    select.name = 'playerVotes';
    select.id = 'playerVotes';

    players.forEach((player, index) => {
        if (index !== playerId && alive[index]) {
            const option = document.createElement('option');
            option.value = index;
            option.text = player;
            select.appendChild(option);
        }
    });
    playerList.appendChild(select);

    // Log the initially selected value
    console.log("Initial option value: ", select.value);

    // Create vote button
    const button = document.createElement('button');
    button.textContent = "Vote Now";
    button.onclick = () => {
        const selectedValue = document.getElementById('playerVotes').value;
        console.log("Selected option value: ", selectedValue);
        sendInteger(selectedValue);
    };
    playerList.appendChild(button);
}

function showPlayer(playerId, players, vote, alive, roles) {
    if (playerId) {
        console.log("show players info");
        console.log("players: ", players);
        console.log("player id: ", playerId);
        console.log("vote: ", vote[playerId]);
        const player = players[playerId];
        const role = roles[playerId];
        if (player) {
            const playerInfoDiv = document.getElementById('playerInfo');
            playerInfoDiv.innerHTML = `
                <p>Name: ${player}</p>
                <p>Role: ${role}</p>
            `;
            if (vote[playerId]) {
                generatePlayersList(players, playerId, alive);
            }
            
        } else {
            document.getElementById('playerInfo').textContent = 'Player not found.';
        }
    } else {
        document.getElementById('playerInfo').textContent = 'No player selected.';
    }

    
}

async function updateState(){
    let game_info = await fetchData();
    console.log('set interval return:')
    console.log(game_info);
    const playerId = getQueryParam('id');
    const players = game_info.players;
    const vote = game_info.vote;
    const alive = game_info.alive;
    const roles = game_info.roles;
    console.log("info:", game_info);
    showPlayer(playerId, players, vote, alive, roles);
}

document.addEventListener('DOMContentLoaded', () => {
    updateState()
    setInterval(updateState, 5000); 
});