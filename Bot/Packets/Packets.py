import struct

#Functions for types
def PackVarint(val):
	total = b''
	if val < 0:
		val = (1<<32)+val
	while val>=0x80:
		bits = val&0x7F
		val >>= 7
		total += struct.pack('B', (0x80|bits))
	bits = val&0x7F
	total += struct.pack('B', bits)
	return total
 
def UnpackVarint(buff):
	total = 0
	shift = 0
	val = 0x80
	while val&0x80:
		val = struct.unpack('B', buff)[0]
		total |= ((val&0x7F)<<shift)
		shift += 7
	if total&(1<<31):
		total = total - (1<<32)
	return total

#unsigned short
def PackUShort(short):
	return struct.pack(">H", short)
	
def PackString(string):
	encodedString = bytes(string, 'utf-8')
	length = PackVarint(len(encodedString))
	return length + encodedString
	
def Send(s, packet):
	s.send(PackVarint(len(packet)) + packet)
	print("Sent packet: " + str(packet))
	
def Read(packet):
	packetId = packet[1]
	print(packet)
	