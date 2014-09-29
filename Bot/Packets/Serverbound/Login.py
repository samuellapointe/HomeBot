from Bot.Packets import Packets

def CreateLogin(u):
	packetId = Packets.packVarint(0)
	username = Packets.PackString(u)
	return(packetId + username)