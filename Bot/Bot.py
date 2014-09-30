import socket
import sys
import traceback
import hashlib
import os
import json
import urllib.request
from Bot.Packets.Serverbound import Handshake, Login, EncryptionResponse
from Bot.Packets import Packets
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from base64 import b64encode

def Authentificate(publicKey, token, username, password):
	sha1 = hashlib.sha1()
	sha1.update(bytes("", "UTF-8")) #empty server string
	sharedSecret = os.urandom(16)
	sha1.update(sharedSecret) #shared secret
	sha1.update(publicKey) #public key
	hash = javaHexDigest(sha1)
	payload = json.dumps({"agent":{"name":"Minecraft","version":1},"username":username,"password":password}).encode('UTF-8')
	print(payload)
	
	req = urllib.request.Request('https://authserver.mojang.com/authenticate')
	req.add_header('Content-Type', 'application/json')
	response = urllib.request.urlopen(req, payload)
	responseText = response.read().decode('utf-8')
	responseVar = json.loads(responseText)
	
	accessToken = responseVar['accessToken']
	selectedProfile = responseVar['selectedProfile']
	payload = json.dumps({"accessToken": accessToken, "selectedProfile": selectedProfile, "serverId": hash}).encode('UTF-8')
	req = urllib.request.Request('https://sessionserver.mojang.com/session/minecraft/join')
	req.add_header('Content-Type', 'application/json')
	response = urllib.request.urlopen(req, payload)
	responseText = response.read().decode('utf-8')
	
	return sharedSecret

	

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
	cpt += 2
	
	publicKey = data[cpt:cpt+publicKeyLength]
	
	tokenLength = data[cpt+publicKeyLength]
	print(tokenLength)
	cpt += 1
	
	token = data[cpt+publicKeyLength:cpt+publicKeyLength+tokenLength]
	sharedSecret = Authentificate(publicKey, token, username, password)
	
	#print(b64encode(publicKey))
	
	cipher = PKCS1_v1_5.new(RSA.importKey(publicKey))
	Packets.Send(s, EncryptionResponse.CreateEncryptionResponse(cipher.encrypt(sharedSecret), cipher.encrypt(token)))
	


	while(True):
		data = s.recv(4096)
		print(len(data))
		print("---")
		print(data)
		if(len(data)!= 4096):
			input()
	#Packets.Read(data)