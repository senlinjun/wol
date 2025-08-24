import socket
s = socket.socket()
s.connect((input("ip: "),int(input("port: "))))
while True:
    command = input("Command: ")
    if command == "q":
        break
    s.send(("667866RUN"+command).encode("utf-8"))
    print(s.recv(1024).decode("utf-8"))