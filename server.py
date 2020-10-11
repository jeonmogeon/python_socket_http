import socket
import threading

PORT = 8080
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

ACCESS = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"NEW CONNECTION {addr} connected.\n")
    if addr[0] in ACCESS:
        print("Not Permitted Client")
        AC = False
    else: 
        AC = True

    connected = True
    while connected:  
        req = conn.recv(65535)
        if req == b'':
            break
        print(req.decode(FORMAT))
        REQ = req.decode(FORMAT).split('\r\n')
        for RE in REQ:
            ID = RE.split(" ")[0]
            if ID == "GET":  reqProtocol = RE
            if ID == "Host:":  reqHost = RE
            if ID == "Referer:":  reqReferer = RE
            if ID == "Accept:":  reqAccept = RE
            if ID == "Accept-Encoding:":  reqAcceptEncoding = RE      

        reqType = reqProtocol.split(' ')[0]
        reqDir = reqProtocol.split(' ')[1]
        reqProtocol = reqProtocol.split(' ')[2]
        
#MOD
        INDEX = "/index.html"

        if reqDir == "/":
            with open("."+INDEX, 'rb') as f:
                byte = f.read()

            resProtocol = reqProtocol
            resStatusCode = "200 OK"
            resContentType = "text/html; charset=utf-8"
            resContent = byte

        elif inc(reqDir, "/mp3"):
            try:
                with open("."+reqDir, 'rb') as f:
                    byte = f.read()
        
                resProtocol = reqProtocol
                resStatusCode = "200 OK"
                resContentType = "audio/mp3"
                resContent = byte
            except Exception:
                resProtocol = reqProtocol
                resStatusCode = "404 Forbidden"
                resContentType = "text/plain"
                resContent = "404 Fobbiden".encode(FORMAT)

        elif inc(reqDir, "/mp4"):
            try:
                with open("."+reqDir, 'rb') as f:
                    byte = f.read()
        
                resProtocol = reqProtocol
                resStatusCode = "200 OK"
                resContentType = "video/mp4"
                resContent = byte
            except Exception:
                resProtocol = reqProtocol
                resStatusCode = "404 Forbidden"
                resContentType = "text/plain"
                resContent = "404 Fobbiden".encode(FORMAT)

        elif inc(reqDir, "/storage"):
            with open("."+reqDir, 'rb') as f:
                byte = f.read()
    
            resProtocol = reqProtocol
            resStatusCode = "200 OK"
            resContentType = "video/mp4"
            resContent = byte

        elif reqDir == "/favicon.ico":
            with open("."+reqDir, 'rb') as f:
                byte = f.read()
            
            resProtocol = reqProtocol
            resStatusCode = "200 OK"
            resContentType = "image/png"
            resContent = byte
# FIX
        else:
            resProtocol = reqProtocol
            resStatusCode = "404 Forbidden"
            resContentType = "text/plain"
            resContent = "404 Fobbiden".encode(FORMAT)
        
        if AC == False:
            resProtocol = reqProtocol
            resStatusCode = "401 Unauthorized"
            resContentType = "text/plain"
            resContent = "401 Unauthorized".encode(FORMAT)

        res = f"{resProtocol} {resStatusCode}\r\nServer: Python\r\nContent-Type: {resContentType}\r\n\r\n".encode(FORMAT)+resContent+"\r\n".encode(FORMAT)
        conn.send(res)
        print(f"{resProtocol} {resStatusCode}\r\nServer: Python\r\nContent-Type: {resContentType}\n")
        
        if resProtocol == "HTTP/1.1":
            connected = False

    print(f'CONNECTION ENDED {addr}\n')

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS {threading.activeCount() - 1}\n")

def inc(sra, srb):
    return sra.replace(srb,'')!=sra #sra included in srb

print(f">>> SERVER RUNNING at {SERVER}:{PORT} <<<")
start()