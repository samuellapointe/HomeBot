import socket
import sys
import traceback
from Bot.Packets.Serverbound import Handshake

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
		
	print("Server found")