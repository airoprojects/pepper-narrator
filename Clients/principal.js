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