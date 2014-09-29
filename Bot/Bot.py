import socket
import sys
import traceback
import hashlib
import os
import json
import urllib.request
from Bot.Packets.Serverbound import Handshake, Login
from Bot.Packets import Packets

def Authentificate(publicKey, token, username):
	sha1 = hashlib.sha1()
	sha1.update(bytes("", "UTF-8")) #empty server string
	sha1.update(os.urandom(16)) #shared secret
	sha1.update(publicKey) #public key
	hash = javaHexDigest(sha1)
	payload = json.dumps({'accessToken': str(token), 'selectedProfile': username, 'serverId': hash}).encode('UTF-8')
	print(payload)
	
	req = urllib.request.Request('https://sessionserver.mojang.com/session/minecraft/join')
	req.add_header('Content-Type', 'application/json')
	response = urllib.request.urlopen(req, payload)

# This function courtesy of barneygale
def javaHexDigest(digest):
    d = int(digest.hexdigest(), 16)
    if d >> 39 * 4 & 0x8:
        d = "-%x" % ((-d) & (2 ** (40 * 4) - 1))
    else:
        d = "%x" % d
    return d
	
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
	Packets.Send(s, Login.CreateLogin(username))
	
	data = s.recv(1024)
	Packets.Read(data) #Encryption request
	
	#Assuming encryption is enabled, getting public key and token:
	cpt=4
	
	publicKeyLength = data[cpt]
	cpt += 1
	
	publicKey = data[cpt:publicKeyLength]
	cpt += 1
	
	tokenLength = data[cpt+publicKeyLength]
	cpt += 1
	
	token = data[cpt+publicKeyLength:cpt+publicKeyLength+tokenLength]

	Authentificate(publicKey, token, username)
