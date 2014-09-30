from Bot.Packets import Packets

def CreateEncryptionResponse(sharedSecret, token):
	packetId = Packets.PackVarint(1)
	sharedSecretLength = Packets.PackVarint(len(sharedSecret))
	tokenLength = Packets.PackVarint(len(token))
	return(packetId + sharedSecretLength + sharedSecret + tokenLength + token)