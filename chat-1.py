import socket
import sys
import select
import json
import ast

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[2])
if port != 0:
    address = ('127.0.0.1', port)
else:
    address = sys.argv[3].split(':')
    address[1] = int(address[1])
    address = tuple(address)
mode = sys.argv[1]

if mode == '-direct' and sys.argv[2] != '0':
    print('binding to', address)
    mySocket.bind(address)
    mySocket.listen(1)
    client_socket = None
    try:
        inputs = [mySocket, sys.stdin]
        while True:
            #print('>>', end='', flush=True)
            readable, writable, exceptional = select.select(inputs, [], [])
            if sys.stdin in readable:
                messageInput = input()
                message = '{"source": { "ip" : "127.0.0.1", "port" : "10000" }, "destination": { "ip" : "127.0.0.1", "port" : "port" }, "message": { "topic" : "null", "text" : "%s" } }' % messageInput
                client_socket.sendall(message.encode())
            elif mySocket in readable:
                client_socket, clientAddress = mySocket.accept()
                print('Connected to client')
                inputs.append(client_socket)
            else:
                assert(client_socket in readable)
                data = client_socket.recv(256)
                if data:
                    data = str(data)
                    data = data[2:-1]
                    jsonObj = json.loads(data)
                    dataText = jsonObj["message"]["text"]
                    print(dataText)
                else:
                    break
    finally:
        mySocket.close()

elif mode == '-direct' and sys.argv[2] == '0':
    addressAsList = sys.argv[3].split(':')
    port = addressAsList[1]
    address = ('127.0.0.1', int(port)) 
    print('connecting to', address)
    print('conencted to server at ', address)
    mySocket.connect(address)
    try:
        while True:
            readable, writable, exceptional = select.select([mySocket, sys.stdin], [], [])

            if sys.stdin in readable:
                messageInput = input()
                message = '{"source": { "ip": "127.0.0.1", "port": "10000" }, "destination": { "ip" : "127.0.0.1", "port" : "port" }, "message": { "topic": "null", "text": "%s" } }' % messageInput
                mySocket.sendall(message.encode())
            elif mySocket in readable:
                data = mySocket.recv(256)
                data = str(data)
                data = data[2:-1]
                jsonObj = json.loads(data)
                dataText = jsonObj["message"]["text"]
                print(dataText)
    finally:
        mySocket.close()

elif mode == '-topic':
    registered = False
    mySocket.connect(address)
    topic = sys.argv[3]
    message = '{"source": { "ip": "127.0.0.1", "port": "10000" }, "topics": { "topic": "%s" } }' % topic 
    mySocket.sendall(message.encode())
    try:
        while True:
            readable, writable, exceptional = select.select([mySocket, sys.stdin], [], [])
            #print('>>', end='', flush=True)
            if mySocket in readable:
                data = mySocket.recv(256)
                if data:
                    data = str(data)
                    data = data[2:-1]
                    jsonObj = json.loads(data)
                    jsonDict = ast.literal_eval(data)
                    if 'topics' in jsonDict.keys():
                        continue
                    else:
                        dataText = jsonObj["message"]["text"]
                        print(dataText)
                else: 
                    break
            elif sys.stdin in readable:
                messageInput = input()
                message = '{"source": { "ip" : "127.0.0.1", "port" : "10000" }, "destination": { "ip" : "127.0.0.1", "port" : "port" }, "message": { "topic" : "%s", "text" : "%s" } }' % (topic, messageInput)
                mySocket.sendall(message.encode())
    finally:
        mySocket.close()
