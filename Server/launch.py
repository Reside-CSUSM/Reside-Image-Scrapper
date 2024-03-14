from FlaskServer import *
import socket

server = FlaskServer()
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
server.host_with("172.25.177.82", 9999)
server.host_with(IPAddr, 9999)
server.run()