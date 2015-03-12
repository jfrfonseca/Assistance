
#!/usr/bin/env python

from threading import Thread, Lock
#from WebSocketServer import WebSocketServer  # @UnresolvedImport


import socket, struct, hashlib, threading, cgi, time
from apt_pkg import base64_encode

class WebSocketThreadObject():
    def decode_key (self, key):
        num = ""
        spaces = 0
        for c in key:
            if c.isdigit():
                num += c
            if c.isspace():
                spaces += 1
        if (spaces == 0): spaces = 1
        return int(num) / spaces
     
#    def create_hash (self, key1, key2, code):
#        a = struct.pack(">L", self.decode_key(key1))
#        b = struct.pack(">L", self.decode_key(key2))
#        md5 = hashlib.md5(a + b + code)
#        return md5.digest()
    
    def create_hash (self, key1, code):
        a = struct.pack(">L", self.decode_key(key1))
        md5 = hashlib.md5(a + code)
        return md5.digest()
     
    def recv_data (self, client, length):
        data = client.recv(length)
        if not data: return data
        return data.decode('utf-8', 'ignore')
     
    def send_data (self, client, data):
        message = "\x00%s\xFF" % data.encode('utf-8')
        return client.send(message)
     
    def parse_headers (self, data):
        headers = {}
        lines = data.splitlines()
        for l in lines:
            parts = l.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        headers['code'] = lines[len(lines) - 1]
        return headers
     
    def handshake (self, client):
        print 'Handshaking...'
        data = client.recv(1024)
        headers = self.parse_headers(data)
        print 'Got headers:'
        for k, v in headers.iteritems():
            print k, ':', v
#        digest = self.create_hash(
#                             headers['Sec-WebSocket-Key1'],
#                             headers['Sec-WebSocket-Key2'],
#                             headers['code']
#        )
        
        webSocketGUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        answerKey = base64_encode(str(hashlib.sha1(headers['Sec-WebSocket-Key']+webSocketGUID)))
        
        shake =    "HTTP/1.1 101 Switching Protocols\r\n"
        shake += "Upgrade: websocket\r\n"
        shake += "Connection: Upgrade\r\n"
        shake += "Sec-WebSocket-Accept: "+str(answerKey)+"\r\n"
        shake += "Sec-WebSocket-Protocol: chat\r\n"
        
        #shake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
        #shake += "Upgrade: WebSocket\r\n"
        #shake += "Connection: Upgrade\r\n"
        #shake += "Sec-WebSocket-Origin: %s\r\n" % (headers['Origin'])
        #shake += "Sec-WebSocket-Location: ws://%s/stuff\r\n" % (headers['Host'])
        #shake += "Sec-WebSocket-Protocol: sample\r\n\r\n"
        #shake += digest
        return client.send(shake)
     
     
    def handle (self, client, addr):
        self.handshake(client)
        print "handshake sucessful!"
        lock = threading.Lock()
        while 1:
            data = self.recv_data(client, 1024)
            if not data: break
            print str(data)
            self.receivedMessagesBuffer.append(data)
            data = self.toSendMessagesBuffer.pop(0)
            time.sleep(self.clock)
            data = cgi.escape(data)
            lock.acquire()
            [self.send_data(c, data) for c in self.clients]
            lock.release()
        print 'Client closed:', addr
        lock.acquire()
        self.clients.remove(client)
        lock.release()
        client.close()
 
 
    def webSocketThread(self):
        while(self.running):
            conn, addr = self.socketObject.accept()
            print 'Connection from:', addr
            self.clients.append(conn)
            self.handle(conn, addr)
    
    
    def __init__(self, host, port):
        self.clients = []
        self.running = True
        self.port = port
        self.host = host
        self.socketObject = socket.socket()
        self.socketObject.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socketObject.bind((host, port))
        self.socketObject.listen(5)
        self.receivedMessagesBuffer = []
        self.toSendMessagesBuffer = []
        self.clock = 0.01
        self.socketActiveThread = Thread(target = self.webSocketThread)
        self.socketActiveThread.start()
    
    def getReceivedMessagesBuffer(self):
        data = self.receivedMessagesBuffer
        if len(data) < 1:
            data = ['']
        return data
    
    def clearReceivedMessagesBuffer(self):
        self.receivedMessagesBuffer = []
        
    def sendMessage(self, message):
        lockTheBuffer = Lock()
        lockTheBuffer.acquire()
        self.toSendMessagesBuffer.append(message)
        lockTheBuffer.release()
        
    def getPort(self):
        return self.port
    
    def getServerObject(self):
        return self.socketObject
    
    def concludere(self):
        self.running = False
        
       
    



