import threading
import socket


class tcpserverthread(threading.Thread):
    def __init__(self,port):
      threading.Thread.__init__(self)
      self.port=int(port)
    def run(self):
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
           s.bind(('127.0.0.1',self.port))
           s.listen()
           while(True):
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    strdata=data.decode('utf-8')
                    parseddata=strdata.split("-")
                    if(parseddata[0]=="handshake"):
                        connectedusers[parseddata[1]]=(parseddata[2],int(parseddata[3]))
                        print("user with name of ",parseddata[1]," connected to server")
                        print(connectedusers)
                    else:
                        if(parseddata[0]=="join"):
                            gpid=parseddata[1]
                            username=parseddata[2]
                            if(not(username in connectedusers.keys())):
                                pass
                            else:
                                if(gpid in groups.keys()):
                                    if(username not in groups[gpid]):
                                        groups[gpid].append(username)
                                else:
                                    groups[gpid]=[username]
                                print(groups)
                        else:
                            if(parseddata[0]=="send"):
                                gpid=parseddata[1]
                                txt=parseddata[2]
                                username=parseddata[3]
                                msg=username+"said: "+txt+ "in the group: " + gpid
                                for user in groups[gpid]:
                                    if(user!=username):
                                        s1=sendmsgthread(msg,connectedusers[user])
                                        s1.start()
                            else:
                                if(parseddata[0]=="leave"):
                                    gpid=parseddata[1]
                                    username=parseddata[2]
                                    groups[gpid].remove(username)
                                    



class sendmsgthread(threading.Thread):
    def __init__(self,msg,addr):
      threading.Thread.__init__(self)
      self.msg=msg
      self.addr=addr
    def run(self):
        s2 = socket.socket()
        s2.connect(self.addr)
        bytemsg=bytes(self.msg,'utf-8')
        s2.send(bytemsg)
        s2.close()


connectedusers={}
groups={}
port = input("Set Server port:")
tcpserver=tcpserverthread(port)
tcpserver.start()