from Bot.Packets import Packets

def CreateHandshake(i, p):
	packetId = Packets.PackVarint(0)
	protocolVersion = Packets.PackVarint(47)
	ip = Packets.PackString(i)
	port = Packets.PackUShort(int(p))
	nextState = Packets.PackVarint(2) #login
	return packetId + protocolVersion + ip + port + nextState