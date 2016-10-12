import socket, threading, sys

class ClientHandler(threading.Thread):
    def __init__(self, chatroom, client_socket, client_address):
        threading.Thread.__init__(self)
        self.chatroom = chatroom
        self.client = { 'socket': client_socket, 'address': client_address }
        
    def register(self):
        self.client['socket'].sendall(b"What is your username?")
        username_okay = False
        while not username_okay:
            user_input = self.client['socket'].recv(256).decode()
            if self.chatroom.username_exists(user_input):
                self.client['socket'].sendall(b"Username already exists, try another one?")
            else:
                msg = ''
                self.client['username'] = user_input
                self.chatroom.add_client(self.client)
                msg += "Welcome "+user_input + "\n-------------------\nmembers online:\n"+self.chatroom.render_client_list()
                print(self.chatroom.render_client_list())
                self.client['socket'].sendall(msg.encode('utf-8'))
                
                self.chatroom.broadcast("*** "+user_input+" has joined the Chatroom ***", self.client)
                
                username_okay = True
    
    def run(self):
        print("Client connected from "+self.client['address'][0]+"\n")
        print(self.chatroom.render_client_list())
        msg = 'Welcome to Chatroom at '+self.chatroom.host+'\n------------------------\n'
        msg += 'members online : \n'
        msg += self.chatroom.render_client_list()
        self.client['socket'].sendall(msg.encode('utf-8'))
        self.register()
        while True:
            chunk = self.client['socket'].recv(256)
            if not chunk:
                break
            print(self.client['username']+' : '+chunk.decode())
            # sock.sendall(chunk)
            
            self.chatroom.broadcast((self.client['username']+' : '+chunk.decode('utf-8')), self.client)
        self.chatroom.remove_client(self.client['socket'])
        self.chatroom.broadcast("*** "+self.client['username']+" has left the Chatroom ***", self.client)
        self.client['socket'].close()
        print("Client disconnected from "+self.client['address'][0]+"\n")

class Chatroom():
    def __init__(self, host='', port=8100, max_connections=10):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.socket.bind((host, port))
        
        self.clients = []
        
    def add_client(self, client_data):
        self.clients.append(client_data)
    
    def remove_client(self, client_socket):
        ri = -1
        for i, client in enumerate(self.clients):
            if client['socket'] == client_socket:
                ri = i
        self.clients.pop(ri)
        
    def username_exists(self, username):
        for i, client in enumerate(self.clients):
            if client['username'] == username:
                return True
        return False
        
    def broadcast(self, message, announcer):
        for cli in self.clients:
            if not cli['socket'] == announcer['socket']:
                cli['socket'].sendall(message.encode('utf-8'))
        
    def render_client_list(self):
        msg = '------------------------\n'
        for cli in self.clients:
            msg += cli['username'] + '\n'
        msg += '------------------------\n'
        return msg
        
    def start(self):
        print("------------------------")
        print("Starting Chatroom at host "+self.host+":"+str(self.port))
        print("------------------------")
        print("Maximum Number of Connections : "+str(self.max_connections))
        print("------------------------")
        self.socket.listen(self.max_connections)
        while True:
            (cs, address) = self.socket.accept()
            handler = ClientHandler(self, cs, address)
            handler.start()
        self.socket.close()
        
if __name__ == "__main__":
    host_info = ['', 8100]
    max_conn = 10
    if len(sys.argv) > 1:
        host_info[0] = sys.argv[1].split(':')[0]
        host_info[1] = int(sys.argv[1].split(':')[1])
        if len(sys.argv) == 3:
            max_conn = int(sys.argv[2])
    chatroom = Chatroom(host_info[0], host_info[1])
    chatroom.start()