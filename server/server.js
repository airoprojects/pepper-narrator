const fs = require('fs');
const lockfile = require('lockfile');
const path = './semaphore.txt';
const lockPath = './semaphore.txt.lock';
const interval = 5000; // Check every 5 seconds

function checkSemaphore() {
  lockfile.lock(lockPath, { retries: 10, retryWait: 100 }, (err) => {
    if (err) {
      console.error('Error acquiring lock:', err);
      return;
    }

    fs.readFile(path, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading semaphore file:', err);
        lockfile.unlock(lockPath, (err) => {
          if (err) console.error('Error releasing lock:', err);
        });
        return;
      }

      if (data.trim() === 'green') {
        console.log('Semaphore is green, executing callback...');
        readDatabase();
      } else {
        console.log('Semaphore is not green, waiting...');
      }

      lockfile.unlock(lockPath, (err) => {
        if (err) console.error('Error releasing lock:', err);
      });
    });
  });
}

function readDatabase() {
  // Simulate reading from a JSON database
  const database = require('../../database.json');
  console.log('Reading from database:', database);
}

// Check the semaphore periodically
setInterval(checkSemaphore, interval);