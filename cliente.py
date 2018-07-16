import sys
from socket import *

def recebe_dados_user(id_msg) :
	while True :
		tipo_msg = input("Digite D para inserir dados | P para pesquisa | S para sair\n")
		tipo_msg = tipo_msg.upper()
		if (tipo_msg == 'S') : return tipo_msg
		if (tipo_msg == 'D') :
			while True :
				combustivel = input("Digite o tipo do combustivel\n")
				comb = int(combustivel)
				if(comb >= 0 and comb <= 2) : break
				else : print ("Digite um combustivel valido\n")
			preco = input("Digite o preco do combustivel\n")
			latitude = input("Digite a latitude\n")
			longitude = input("Digite a longitude\n")
			envio = tipo_msg+'|'+str(id_msg[0])+'|'+combustivel+'|'+preco+'|'+str(latitude)+'|'+str(longitude)
			id_msg[0] += 1
			break
		elif (tipo_msg == 'P') :
			while True :
				combustivel = input("Digite o tipo do combustivel\n")
				comb = int(combustivel)
				if(comb >= 0 and comb <= 2) : break
				else : print ("Digite um combustivel valido\n")
			raio = input("Digite o raio de busca\n")
			latitude = input("Digite a latitude\n")
			longitude = input("Digite a longitude\n")		
			envio = tipo_msg+'|'+str(id_msg[0])+'|'+combustivel+'|'+raio+'|'+str(latitude)+'|'+str(longitude)
			id_msg[0] += 1
			break
		else : print ("Digitou errado. Tente novamente\n")
	return envio

def tipo_ip (ip_recv, flag) :
	ip = ''
	for res2 in sa :
		conteudo = str(sa)
		for res3 in conteudo :
			if (res3 == "'") : flag +=1
			if(flag == 1 and res3 != "'") : ip = ip+res3
	return ip

def manipula_resposta(resp, id_resp) :
	print("Mensagem recebida: "+resp+"\n")
	lista_res = []
	if(resp.find("|") < 0 and resp != '-1') :
		if(resp not in id_resp) :
			id_resp.append(resp)
			print("Dado inserido no arquivo com sucesso")
	else :
		lista_res = resp.split("|")
		if(lista_res[0] not in id_resp) :
			id_resp.append(lista_res[0])
			if(resp == '-1') : print("Dado inexistente")
			else : 
				if(lista_res[1] == '99999') :
					print("Nao foi encontrado nada no raio de busca\n")
				else :
					print("Menor valor: "+str(lista_res[1])+
							" na latitude "+str(lista_res[3])+
								" e longitude "+str(lista_res[2])+"\n")

def recebe_mensagem(client_socket, id_resp) :
	rcv_msg, server_addr = client_socket.recvfrom(2048)
	rcv_msg1 = rcv_msg.decode()
	manipula_resposta(rcv_msg1, id_resp)

def envio_mensagem(client_socket, msg_envio, server_name, server_port,id_resp) :
	client_socket.sendto(msg_envio.encode(),(server_name, server_port))
	print("Mensagem enviada: "+msg_envio)
	client_socket.settimeout(5.0)
	recebe_mensagem(client_socket, id_resp)
	client_socket.settimeout(None)

if __name__ == "__main__":
	id_msg = [0]
	id_resp = [0]
	server_name = sys.argv[1]
	server_port = int(sys.argv[2])
	client_socket = socket(AF_INET6, SOCK_DGRAM)
	flag = 0

	ipv4 = ''
	ipv6 = ''
	
	#saber o endereco correto, sem ser nome
	for res in (getaddrinfo(server_name, 1995, 0,SOCK_DGRAM)) :
		flag = 0
		arq_ip, socktype, proto, canonname, sa = res
		sarq_ip = str(arq_ip)
		if(sarq_ip.find("AF_INET6") >= 0) : ipv6 = tipo_ip (sa, flag)
		elif (sarq_ip.find("AF_INET6") < 0): ipv4 = tipo_ip (sa, flag)
		else : print("erro")

	if(ipv6 == '') : server_name ='::FFFF:' + ipv4
	else : server_name = ipv6
		
	while True :
		msg_envio = recebe_dados_user(id_msg)
		if(msg_envio == "S") : break

		try: 
			envio_mensagem(client_socket, msg_envio, server_name, server_port, id_resp)
		except Exception as e: 
			print("Resposta nao recebida, tentando novamente")
			try :
				envio_mensagem(client_socket, msg_envio, server_name, server_port, id_resp)
			except Exception as e:
				print("Impossivel receber uma resposta. Digite novamente\n")
			
	# Closing socket
	client_socket.close()
