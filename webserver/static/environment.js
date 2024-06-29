async function fetchData() {
    const response = await fetch('http://'+host_ip+':5000/request_data');  // Flask server URL
    const data = await response.json();
    console.log(data);  // Logging the entire dictionary
    return data
}

let game_info = await fetchData();
const players = game_info.players;

const playersListDiv = document.getElementById('buttons_eyes_opened');
players.forEach((player, index) => {
    const button = document.createElement('button');
    button.textContent = player; // Set the button text to the player's name
    button.id = `player-${index}`; // Set the button id to the index of the player
    button.onclick = () => {
        // window.location.href = `player.html?id=${index}`
        console.log('player selected:', player);
    };
    playersListDiv.appendChild(button);
});