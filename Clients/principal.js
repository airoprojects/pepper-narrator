const switchButton = document.getElementById('switchButton');
const body = document.body;

switchButton.addEventListener('click', () => {
  if (body.classList.contains('day')) {
    body.classList.remove('day');
    body.classList.add('night');
    switchButton.textContent = 'Switch to Day Mode';
  } else {
    body.classList.remove('night');
    body.classList.add('day');
    switchButton.textContent = 'Switch to Night Mode';
  }
});


document.addEventListener('DOMContentLoaded', () => {
  const addPlayerForm = document.getElementById('addPlayerForm');

  addPlayerForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const playerName = document.getElementById('playerName').value;
    //TODO the role must be selected with a specific logic 
    const playerRole = document.getElementById('playerRole').value;


    // TODO how to take the address?
    const response = await fetch('http://127.0.0.1:5000/api/player', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: playerName, role: playerRole }),
    });

    if (response.ok) {
      const result = await response.json();
      console.log(result.message);
      // Optionally, refresh the player list or update the UI
      alert('Player added successfully!');
      addPlayerForm.reset();
    } else {
      console.error('Error adding player');
      alert('Failed to add player');
    }
  });
});
