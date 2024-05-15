import time
import fcntl
import threading

def check_key(stop_event):
    input("Press Enter to exit the loop.\n")
    stop_event.set()

stop_event = threading.Event()
key_thread = threading.Thread(target=check_key, args=(stop_event,))
key_thread.start()

semaphore_file = 'semaphore.txt'

def set_semaphore(status):
    with open(semaphore_file, 'w') as file:
        fcntl.flock(file, fcntl.LOCK_EX)  # Acquire exclusive lock
        file.write(status)
        fcntl.flock(file, fcntl.LOCK_UN)  # Release lock

# Example: Set the semaphore to green after 10 seconds
while not stop_event.is_set():
  set_semaphore('green')
  print('Semaphore set to green')
  time.sleep(10)

  set_semaphore('red')
  print('Semaphore set to red')
  time.sleep(10)


  
set_semaphore('red')