import socket
import time

adr = ("192.168.0.13",8000)

"""
print "Endereco IP: \n"
adr[0]= raw_input()
"""
MESSAGE = ""
#import machine \npin = machine.Pin(2,machine.Pin.OUT) \npin.value(!pin.value())
print "UDP target IP:", adr[0], adr[1]
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
for i in range(0,10):
	sock.sendto("frente", (adr[0], adr[1]))
	time.sleep(1)
	sock.sendto("tras", (adr[0], adr[1]))
	time.sleep(1)
	#sock.sendto("frente", (adr[0], adr[1]))
sock.sendto("parar", (adr[0], adr[1]))

while True:
	MESSAGE = raw_input()
	print 'enviado: ',MESSAGE
	if MESSAGE == "sair":
		break
	sock.sendto(MESSAGE, (adr[0], adr[1]))
