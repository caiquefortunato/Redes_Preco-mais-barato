
from socket import *
import sys
from math import *

def retorna_combustivel(tipo_comb) :
	arq = "arq.txt"

	if (tipo_comb == '0') : arq = "diesel.txt"
	elif (tipo_comb == '1') : arq = "alcool.txt"
	elif (tipo_comb == '2') : arq = "gasolina.txt"
	else : print("Erro no tipo de combustivel\n")
	
	return arq

def escreve_arquivo(mensagem) :
	msg = mensagem.split("|")
	id_m = msg[1]
	tipo_comb = msg[2]
	# Confere o tipo de combustivel
	arq = retorna_combustivel(tipo_comb)
	# Escreve os dados no arquivo
	i = 0
	file = open(arq,"a+") 
	for n in mensagem :
		if(i >= 3) : file.write(n)
		if(n == '|') : i+=1 
	file.write("\n")
	file.close() 
	return id_m

def distancia(raio, lat1, lon1, lat2, lon2) :
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	
	d = 6378.137 * acos( cos( lat1 ) * cos( lat2 ) * cos( lon2 - lon1 ) + sin( lat1 ) * sin( lat2 ) )

	if(d < raio or d == raio) : return True
	else : return False

def pesquisa_posto(mensagem) :
	msg = mensagem.split("|")
	tipo_comb = msg[2]
	m_preco = 99999
	cont = 0
	# Confere o tipo de combustivel
	arq = retorna_combustivel(tipo_comb)
	# Explode a string com split
	id_m = msg[1]
	lat_menor = 0
	lon_menor = 0
	raio = float(msg[3])
	lat = float(msg[4])
	lon = float(msg[5])
	
	try: arquivo = open(arq,"r")
	except Exception : return '-1'
	# Para cada linha verifico o raio
	for line in arquivo:
		line.strip('\n')
		lin_split = line.split("|")
		#Tiro a virgula do preco e passo para int
		preco = lin_split[0]
		for b in preco :
			if(b == ',') : preco = preco.replace(preco[cont],"")
			cont += 1
		preco = int(preco)
		px = float(lin_split[1])
		py = float(lin_split[2])
		# Calculo do raio, verifica se o preco eh menor
		if distancia(raio,lat,lon,px,py) : 
			if preco < m_preco :
				m_preco = preco 
				lat_menor = py
				lon_menor = px
	arquivo.close() 
	return id_m+'|'+str(m_preco)+'|'+str(lat_menor)+'|'+str(lon_menor)

def interpreta_mensagem(msg_cliente) :
	if msg_cliente[0] == 'D' : return escreve_arquivo(msg_cliente)
	if msg_cliente[0] == 'P' : return pesquisa_posto(msg_cliente)

if __name__ == "__main__":
	server_port = int(sys.argv[1])
	IP = "::" # = 0.0.0.0 u IPv4
	id_mens = ''
	lista_id = []
	server_socket = socket(AF_INET6, SOCK_DGRAM)
	# Bind IP + Port
	server_socket.bind((IP, server_port))
	
	print ("Server is ready to receive data.")

	while True: 
		msg, client_addr = server_socket.recvfrom(2048)
		msg1 = msg.decode()

		mens = msg1.split("|")
		id_mens = mens[1]

		print("Mensagem recebida: "+msg1)
				
		new_msg = interpreta_mensagem(msg1)
		print("Mensagem enviada: "+new_msg+"\n")
		server_socket.sendto(new_msg.encode(), client_addr)
