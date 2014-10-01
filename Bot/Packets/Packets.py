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
 
def UnpackVarint(self):
	d = 0
	for i in range(5):
		b = self.unpack("B")
		d |= (b & 0x7F) << 7*i
		if not b & 0x80:
			break
	return d

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
	