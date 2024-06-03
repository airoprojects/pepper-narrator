
async function fetchData() {
    const response = await fetch('http://'+host_ip+':5000/request_data');  // Flask server URL
    const data = await response.json();
    console.log(data);  // Logging the entire dictionary
    return data
}

function generatePlayerButtons(players) {
    const playersListDiv = document.getElementById('playersList');
    playersListDiv.innerHTML = ''; // Clear previous content

    players.forEach((player, index) => {
        const button = document.createElement('button');
        button.textContent = player; // Set the button text to the player's name
        button.id = `player-${index}`; // Set the button id to the index of the player
        button.onclick = () => {
            window.location.href = `player.html?id=${index}`;
        };
        playersListDiv.appendChild(button);
    });
}

async function checkGameStatus() {
    let game_info = await fetchData();
    const game_status = game_info.status;
    const players = game_info.players;
    console.log('game Status:', game_status);
    
    if (game_status === 'active') {
        var element = document.getElementById('greetings');
        element.style.display = 'none';
        generatePlayerButtons(players);

    } else {
        // const welcome_text = document.getElementById('playersList');
        // welcome_text.innerHTML = ''; // Clear previous content
        // welcome_text.appendChild(document.createTextNode('Gratings peasants!!! \nWelcome to the joyful village of Tabula. \nThe sun is low and new exiting night is about to come! \nWhat will happen? \nYou are about to find out!'));
        let curr_ip = location.host;
        console.log(curr_ip)
    }
}

document.addEventListener('DOMContentLoaded', () => {
    checkGameStatus(); // Check the status immediately when the page loads
    setInterval(checkGameStatus, 5000); // Check the status every 5 seconds
});