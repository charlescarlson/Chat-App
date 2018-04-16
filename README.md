# Chat-App
CS:3640 Into to Networks and their Applications
Homework 2
A chat application implemented with socket programming in Python

topic-server.py is a server that creates a server/client network connecting clients subscribes to the same topics.
chat-1.py are clients that can connect to a topic or direct message other clients via P2P

Address is assumed to be 127.0.0.1:PORT
Starting the server: $python topicserver-1.py PORT
Starting the client (subscribing to topic): chat-1.py -topic PORT topic
Starting the client (direct message): chat-1.py -direct PORT
      For direct message simply start two clients with the same port and parameter -direct
