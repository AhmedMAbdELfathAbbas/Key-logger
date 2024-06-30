import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 1234))  

try:
    while True:
        msg = s.recv(1024)
        if not msg:
            break
        print(msg.decode("utf-8") , end='\n')
except KeyboardInterrupt:
    print("closed")
finally:
    s.close()
