<!-- <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Player Page</title>
</head>
<body>
    <h1>Player Info</h1>
    <div id="playerInfo"></div>
    <div id="voting"></div>
    <script src="client.js"></script>

    <script>

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

        function showPlayer(playerId, players, vote, alive) {
            if (playerId) {
                console.log("show players info");
                console.log("players: ", players);
                console.log("player id: ", playerId);
                console.log("vote: ", vote[playerId]);
                const player = players[playerId];
                if (player) {
                    const playerInfoDiv = document.getElementById('playerInfo');
                    playerInfoDiv.innerHTML = `
                        <p>Name: ${player}</p>
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
            game_info = await fetchData();
            console.log('set interval return:')
            console.log(game_info);
            const playerId = getQueryParam('id');
            const players = game_info.players;
            const vote = game_info.vote;
            const alive = game_info.alive;
            console.log("info:", game_info);
            showPlayer(playerId, players, vote, alive);
        }

        document.addEventListener('DOMContentLoaded', () => {
            updateState()
            setInterval(updateState, 5000); 
        });
    </script>
</body>
</html>
 -->





 <!DOCTYPE html>
 <html lang="en">
 <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Player Page</title>
 </head>
 <body>
     <h1>Player Info</h1>
     <div id="playerInfo"></div>
     <div id="voting"></div>
     <script src="client.js"></script>
 
     <script>
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
                 if (index !== parseInt(playerId) && alive[index]) {
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
 
         function showPlayer(playerId, players, vote, alive) {
             if (playerId) {
                 console.log("show players info");
                 console.log("players: ", players);
                 console.log("player id: ", playerId);
                 console.log("vote: ", vote[playerId]);
                 const player = players[playerId];
                 if (player) {
                     const playerInfoDiv = document.getElementById('playerInfo');
                     playerInfoDiv.innerHTML = `
                         <p>Name: ${player}</p>
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
 
         async function updateState() {
             try {
                 const game_info = await fetchData();
                 console.log('set interval return:');
                 console.log(game_info);
                 const playerId = getQueryParam('id');
                 const players = game_info.players;
                 const vote = game_info.vote;
                 const alive = game_info.alive;
                 console.log("info:", game_info);
                 showPlayer(playerId, players, vote, alive);
             } catch (error) {
                 console.error('Error fetching game info:', error);
             }
         }
 
        document.addEventListener('DOMContentLoaded', () => {
            updateState();
            setInterval(updateState, 5000); 
        });
     </script>
 </body>
 </html>
 
