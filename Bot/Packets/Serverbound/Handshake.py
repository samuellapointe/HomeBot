from Bot.Packets import Packets

def CreateHandshake(i, p):
	packetId = Packets.packVarint(0)
	protocolVersion = Packets.packVarint(47)
	ip = Packets.PackString(i)
	port = Packets.PackUShort(int(p))
	nextState = Packets.packVarint(2) #login
	return packetId + protocolVersion + ip + port + nextState