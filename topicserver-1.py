import select
import socket
import sys
import json
import ast

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('127.0.0.1', 10000)
mySocket.bind(serverAddress)
mySocket.listen(20)

userDict = {}
topics = {}
topicList = []
connections = []
inputs = [mySocket]
outputs = []
exceptional = []

try:   
    while True:
        readable, writabele, exceptional = select.select(inputs, outputs, exceptional)
        for currentRead in readable:
            if currentRead is mySocket:
                clientSocket, clientAddress = mySocket.accept()
                print('new connection from ', clientAddress)
                clientSocket.setblocking(0)
                inputs.append(clientSocket)
            else:
                data = currentRead.recv(1024)
                if data:
                    data = str(data)
                    data = data[2:-1]
                    jsonObj = json.loads(data)
                    jsonDict = ast.literal_eval(data)
                    if 'message' not in jsonDict.keys():
                        topic = jsonObj["topics"]["topic"]
                        if topic not in topicList:
                            print('ADDING NEW TOPIC')
                            topicList.append(topic)
                            topics[topic] = []
                            topics[topic].append(clientSocket)
                        else:
                            topics[topic].append(clientSocket)
                    else:
                        topic = jsonObj["message"]["topic"]
                    for conn in topics[topic]:
                        if conn != currentRead:
                            conn.sendall(data.encode())
                else:
                    break
finally:
    mySocket.close()
            
