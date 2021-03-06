import socket
import sys
import traceback
import hashlib
import os
import json
import urllib.request
import zlib
from Bot.Packets.Serverbound import Handshake, Login, EncryptionResponse
from Bot.Packets import Packets
from Bot import AESCipher
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode
from base64 import b64decode
import base64

def Authentificate(publicKey, token, username, password):
	sha1 = hashlib.sha1()
	sha1.update(bytes("", "UTF-8")) #empty server string
	sharedSecret = os.urandom(16)
	sha1.update(sharedSecret) #shared secret
	sha1.update(publicKey) #public key
	hash = javaHexDigest(sha1)
	payload = json.dumps({"agent":{"name":"Minecraft","version":1},"username":username,"password":password}).encode('UTF-8')
	
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
	cpt += 1
	
	token = data[cpt+publicKeyLength:cpt+publicKeyLength+tokenLength]
	sharedSecret = Authentificate(publicKey, token, username, password)
	
	
	#To encrypt once
	pubCipher = PKCS1_v1_5.new(RSA.importKey(publicKey)) 
	Packets.Send(s, EncryptionResponse.CreateEncryptionResponse(pubCipher.encrypt(sharedSecret), pubCipher.encrypt(token)))
	
	cipher = AESCipher.AESCipher(sharedSecret)
	while(True):
		buffer = s.recv(4096)
		data = buffer;
		while(len(buffer) == 4096):
			buffer = s.recv(4096)
			data = data + buffer

		uncryptedData = cipher.decrypt(data)
		
		#if(len(data) == 0):
			#break;
			
		#packetSize = Packets.UnpackVarint(uncryptedData[0:2])
		if(len(uncryptedData) > 3):
			packetId = uncryptedData[3]
			if(packetId == 2):
				print(uncryptedData)
			if(packetId == 0):
				print("KEEPALIVE" + str(len(uncryptedData)))
				#Packets.Send(s, data)
		
			
	#Packets.Read(data)

	