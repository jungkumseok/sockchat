import socket, threading, sys

class ReceiveHandler(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.exit = False
        
    def terminate(self):
        self.exit = True
#         print("Terminating...")
        
    def run(self):
        self.socket.setblocking(0)
        while not self.exit:
            try:
                chunk = self.socket.recv(256)
                if not chunk:
                    continue
                print(chunk.decode('utf-8'))
#                 print(('\r'+chunk.decode('utf-8')+'\n Y O U : '), end='')
            except BlockingIOError:
                continue
#         print("Receive Handler closed")

class Chatter():
    def __init__(self, chatroom_host='localhost', chatroom_port=8100):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatroom = { 'host': chatroom_host, 'port': chatroom_port }
    
    def start(self):
        print('Type \q to exit chat program')
        self.socket.connect((self.chatroom['host'], self.chatroom['port']))
        greeting = self.socket.recv(256) #receive greetings
        print(greeting.decode('utf-8'))
        
        receiver = ReceiveHandler(self.socket)
        receiver.daemon = True
        receiver.start()
        
        while True:
            uin = input('').encode('utf-8')
            if uin == b'\q':
                print("\n------------------\nExiting Chatroom...")
                break
            self.socket.sendall(uin)
            # reply = cs.recv(1024)
            # print("from:localhost << "+reply.decode())
        receiver.terminate()
        receiver.join()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
#         print("Bye bye!")
        
if __name__ == "__main__":
    server = ['', 8100]
    if len(sys.argv) > 1:
        server[0] = sys.argv[1].split(':')[0]
        server[1] = int(sys.argv[1].split(':')[1])
    chatter = Chatter(chatroom_host=server[0], chatroom_port=server[1])
    chatter.start()