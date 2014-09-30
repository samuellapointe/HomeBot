from Bot.Packets import Packets

def CreateLogin(u):
	packetId = Packets.PackVarint(0)
	username = Packets.PackString(u)
	return(packetId + username)