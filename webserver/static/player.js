async function fetchData() {
    const response = await fetch(('http://'+host_ip+':5000/request_data'));  // Flask server URL
    const data = await response.json();
    console.log(data);  // Logging the entire dictionary
    return data
}

// Function to send integer vote to the Flask server
function sendVotation(vote_id, voter_id) {
    fetch('http://'+host_ip+':5000/submit_votes', {  // Flask server URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vote: vote_id, voter: voter_id})
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
        // alert(`Server response: ${data.status}`);
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

// Generate a list of player to vote
function generatePlayersList(players, playerId, alive, roles, night) {
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
    select.className = 'custom-select';
    console.log('night: ', night)
    if (night) {
        players.forEach((player, index) => {
            if (index != playerId && alive[index] && roles[index] != 'wolf') {
                console.log('role', roles[index])
                const option = document.createElement('option');
                option.value = index;
                option.text = player;
                select.appendChild(option);
            }
        });
    }
    else {
        players.forEach((player, index) => {
            if (index != playerId && alive[index]) {
                const option = document.createElement('option');
                option.value = index;
                option.text = player;
                select.appendChild(option);
            }
        });
    }
    playerList.appendChild(select);

    // Log the initially selected value
    console.log("Initial option value: ", select.value);

    // Create vote button
    const button = document.createElement('button');
    button.textContent = "Vote Now";
    button.className = 'modern-button'; // Apply the CSS class for styling
    button.onclick = () => {
        const selectedValue = document.getElementById('playerVotes').value;
        console.log("Selected option value: ", selectedValue);
        sendVotation(selectedValue, playerId);
        button.disabled = "disabled";
    };
    playerList.appendChild(button);
}

function showPlayer(playerId, players, vote, alive, roles, night) {
    if (playerId) {
        console.log("show players info");
        console.log("players: ", players);
        console.log("player id: ", playerId);
        console.log("vote: ", vote[playerId]);
        console.log("night inside: ", night);
        const player = players[playerId];
        const role = roles[playerId];
        const player_alive = alive[playerId];
        if (player) {
            const playerInfoDiv = document.getElementById('playerInfo');
            playerInfoDiv.innerHTML = `
                <p>Name: ${player}</p>
                <p>Role: ${role}</p>
                <p>Alive: ${player_alive}</p>
            `;
            if (vote[playerId]) {
                generatePlayersList(players, playerId, alive, roles, night);
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
    const night = game_info.night;
    console.log('night outside', night)
    // Update background image based on night variable
    const bodyElement = document.body;
    if (night) {
        bodyElement.style.backgroundImage = "url('static/backgrounds/wolf_dark_background.webp')";
    } else {
        bodyElement.style.backgroundImage = "url('static/backgrounds/artistic_background.webp')";
    }
    
    console.log("info:", game_info);
    showPlayer(playerId, players, vote, alive, roles, night);
}

document.addEventListener('DOMContentLoaded', () => {
    updateState()
    setInterval(updateState, 5000); 
});