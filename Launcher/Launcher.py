import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from Server.FlaskServer import *
import socket


server = FlaskServer()
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
server.host_with("172.25.177.82", 9999)
server.host_with(IPAddr, 9999)
server.run()



