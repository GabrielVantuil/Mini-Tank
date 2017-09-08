from socket import *
from machine import Pin
from machine import PWM
import network
import webrepl

sta_if = network.WLAN(network.STA_IF)
webrepl.start()
for i in (0, 2, 4, 5, 12, 13, 14, 15):    #by default ESP initializes all ports with high level, so, this turn then off
	PWM(Pin(i)).freq(500)
	PWM(Pin(i)).duty(1024)

if not sta_if.isconnected():
	ap_if = network.WLAN(network.AP_IF)
	ap_if.config(essid="Esp" , authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")
	
PWM(Pin(2)).duty(10)

def anda(ME1,MD1,ME2,MD2):
	PWM(Pin(12)).duty(ME1)		#esquerdo 1
	PWM(Pin(14)).duty(MD1)		#direito  1
	PWM(Pin(4)).duty(ME2)		#esquerdo 2
	PWM(Pin(5)).duty(MD2)		#direito  2

def connect(rede,senha):
	sta_if.disconnect()
	if not sta_if.isconnected():
		print('connecting to network...')
		sta_if.active(True)
		sta_if.connect(rede, senha)
		while not sta_if.isconnected():
			pass
	print('network config:', sta_if.ifconfig())
	PWM(Pin(2)).freq(500)

PWM(Pin(2)).freq(1)
PWM(Pin(2)).duty(1020)
webrepl.start()

#while not sta_if.isconnected():
#	pass
adr = (sta_if.ifconfig()[0],8000)
udp = socket(AF_INET, SOCK_DGRAM)
udp.bind(adr)

PWM(Pin(2)).duty(1000)
while True:
	print ("Esperando comandos de:", adr[0],":",adr[1])
	PWM(Pin(2)).freq(10)
	PWM(Pin(2)).duty(1020)
	msg, cliente = udp.recvfrom(1024)
	msg = str(msg)
	msg = msg.replace("b'","").replace("'","")
	#msg = str(msg)[2:-1].split("/")
	print (cliente, msg)
	if msg == "frente":
		anda(1024,1024,0,0)
	if msg == "tras":
		anda(0,0,1024,1024)
	if msg == "giraD":
		anda(1024,0,0,1024)
	if msg == "giraE":
		anda(0,1024,1024,0)
	if msg == "parar":
		anda(0,0,0,0)
	
	if msg[2:6] == "pwm:":		#sintaxe: pwm:2,500
		PWM(Pin(int(msg[6]))).freq(500)
		PWM(Pin(int(msg[6]))).duty(int(msg[8:]))
		#print ("pwm ",int(msg[6])," ",int(msg[8,11]))

udp.close()



#D1(5) e D5(14) => motor direito
#D2(4) e D6(12) => motor esquerdo
#frente	= anda(1024,1024,0,0)
#tras 	= anda(0,0,1024,1024)
#giraD 	= anda(1024,0,0,1024)
#giraE 	= anda(0,1024,1024,0)
#parar 	= anda(0,0,0,0)
