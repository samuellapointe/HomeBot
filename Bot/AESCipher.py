from Crypto.Cipher import AES

class AESCipher:
	def __init__(self, SharedSecret):
		#Name courtesy of dx
		self.encryptifier = AES.new(SharedSecret, AES.MODE_CFB, IV=SharedSecret)
		self.decryptifier = AES.new(SharedSecret, AES.MODE_CFB, IV=SharedSecret)
		
	def encrypt(self, data):
		return self.encryptifier.encrypt(data)
		
	def decrypt(self, data):
		return self.decryptifier.decrypt(data)