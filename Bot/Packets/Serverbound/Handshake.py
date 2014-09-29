from Bot.Packets import Packets

def CreateHandshake(i, p):
	packetId = Packets.pack_varint(0)
	protocolVersion = Packets.pack_varint(47)
	ip = Packets.PackString(i)
	port = Packets.PackUShort(int(p))
	nextState = Packets.pack_varint(2) #login
	return packetId + protocolVersion + ip + port + nextState