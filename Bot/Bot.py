import socket
import sys
import traceback
from Bot.Packets.Serverbound import Handshake
from Bot.Packets import Packets

def Connect(username, password, ip, port):
	print("Connecting with username " + username + "...")
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	
	try:
		s.connect((ip, int(port)))
	except:
		print('Connexion failed ')
		print(traceback.format_exc())
		sys.exit()
		
	print("Server found") #Can connect so send handshake
	Packets.Send(s, Handshake.CreateHandshake(ip, port))
	
	data = s.recv(1024)
	print(data)
