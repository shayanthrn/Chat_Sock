import threading
import socket
import os
import socketserver

class tcpserverthread(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
    def run(self):
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
           s.bind(('127.0.0.1',free_tcpport))
           s.listen()
           while(True):
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    strdata=data.decode('utf-8')
                    print(strdata)
                    print("")


class handshaketoserver(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
    def run(self):
        s = socket.socket()
        s.connect((addr,port))
        msg="handshake"+"-"+name+"-"+myip+"-"+str(free_tcpport)
        bytemsg=bytes(msg,'utf-8')
        s.send(bytemsg)
        s.close()



addr=input("Please Enter the server address:")
port=int(input("Please Enter the Port of server:"))
name=input("Please Enter your name:")
myip="127.0.0.1"  #u can use os library to find your ip in practice

with socketserver.TCPServer(("localhost", 0), None) as s:
    free_tcpport = s.server_address[1]

tcpserver=tcpserverthread()
handshake=handshaketoserver()
tcpserver.start()
handshake.start()

while(True):
    choice=input("please enter your command:\n").split()
    if(choice[0].lower()=="join"):
        gpid=choice[1]
        s = socket.socket()
        s.connect((addr,port))
        msg="join"+"-"+gpid+"-"+name
        bytemsg=bytes(msg,'utf-8')
        s.send(bytemsg)
        s.close()
    else:
        if(choice[0].lower()=="send"):
            gpid=choice[1]
            txt=""
            for word in choice[2:]:
                txt += word + " "
            txt = txt.strip()
            s = socket.socket()
            s.connect((addr,port))
            msg="send"+"-"+gpid+"-"+txt+"-"+name
            bytemsg=bytes(msg,'utf-8')
            s.send(bytemsg)
            s.close()
        else:
            if(choice[0].lower()=="leave"):
                gpid=choice[1]
                s = socket.socket()
                s.connect((addr,port))
                msg="leave"+"-"+gpid+"-"+name
                bytemsg=bytes(msg,'utf-8')
                s.send(bytemsg)
                s.close()
            else:
                if(choice[0].lower()=="quit"):
                    os._exit(0)
                else:
                    print("invalid input")

