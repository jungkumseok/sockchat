# SockChat - Lightweight Python3 Chat Application

This is a lightweight Python3 chat application that can be used in intranet environments.
It includes a server.py script that is used to start the chat server, and a client.py that a chat user will use to chat with other users.

*There are absolutely no security measures for the message exchange; all the messages are regular unencrypted bytestrings*


##Usage Scenario

Sometimes I visit clients' worksites (usually factories) to provide services, and most such sites do not provide access to internet for security. Some clients even prohibit regular use of cellphones and these kind of restrictions make it quite difficult to communicate effectively with my teammates at the field. Often I'll be working at one end of a large factory while my teammate is working at the other end of the factory, and with such restrictions in effect, the most effective way of communicating was writing down notes and then sharing them during the breaks.
I wrote this so that my teammates and I can have conversations over the local network in such restrictive environments.


## How to use

Download the content of this repository or git clone it.

There are two files: [server.py, client.py]

### Run chat server

On one of the workstations that will act as the chat server, run the server.py script.
```
~$ python3 server.py
```
This will start the chat server. By default, it will start the server on localhost, on port 8100.
To customize the IP and port of the chat server, run the script with command-line arguments.
```
~$ python3 server.py 192.168.0.10:8200 
```

### Run chat client

On the workstations that the chat users will be using, run the client.py script.
```
~$ python3 client.py 192.168.0.10:8200
```
For running the client.py script, it's better to explicitly provide the IP and port of the chat server since the script will connect to localhost:8100 by default and will raise a ConnectionRefusedError in most cases.

## Dependencies and Requirements

* Python3 (used modules: socket, threading, sys)


## License

MIT License