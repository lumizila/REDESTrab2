#!/usr/bin/python

#PROTOCOLO DAS MENSAGENS:

#Formato da mensagem: [TIPO]_[QUEM ENVIOU]_[PARA QUEM ENVIOU]_[POSICAO X]_[POSICAO Y]_[SITUACAO]

#Tipo pode ser:
#	1 = ataque
#	2 = navio afundou
#	3 = jogador perdeu
#	4 = ataque acertou, mas navio nao afundou
#	5 = ataque errou
#	6 = mensagem aberta de que navio afundou
#	7 = mensagem aberta de que jogador perdeu
#	9 = bastao

#Quem enviou pode ser: 
#	1,2,3,4 = jogador de numero x

#Para quem enviou pode ser:
#	1,2,3,4 = jogador de numero x

#Posicao x e posicao y representam a posicao de ataque de um navio

#Dependendo da mensagem, ela deve ser lida por todos os jogadores(se for msg Tipo 6 ou 7)
#Situacao indica:
#	9 = NACK
#	1 = ACK ou lido por 1 jogador
#	2 = Lido por 2 jogadores
#	3 = Lido por 3

import sys
import math
import socket

#imprime o tabuleiro
def imprimeTabuleiro(tabuleiro, tamanho):
	sys.stdout.write("_| ");
	for aux in range(tamanho):
		sys.stdout.write(str(aux)+"  ")
	print("")	

	for x in range(tamanho):
		sys.stdout.write(str(x)+"| ")
		for y in range(tamanho):
			sys.stdout.write(tabuleiro[x*tamanho+y]+" ")
		print("")
	return

#inicia tabuleiro com 0 em todas as posicoes
def iniciaTabuleiro(tabuleiro, tamanho):
	for x in range(tamanho):
		for y in range(tamanho):
			tabuleiro.append("--")
	return

#adiciona navio ao tabuleiro
def adicionaNavio(x1, y1, x2, y2, tabuleiro, tamanho, navio):
	if(x1 < x2):
		for x in range(x1, x2+1):
			if(y1 < y2):
				for y in range(y1, y2+1):
					tabuleiro[x*tamanho+y] = "n"+str(navio)
			else:
				for y in range(y2, y1+1):
					tabuleiro[x*tamanho+y] = "n"+str(navio)
	else:
		for x in range(x2, x1+1):
			if(y1 < y2):
				for y in range(y1, y2+1):
					tabuleiro[x*tamanho+y] = "n"+str(navio)
			else:
				for y in range(y2, y1+1):
					tabuleiro[x*tamanho+y] = "n"+str(navio)
	return

def geraAtaque(atacante):
	jogador = input("Qual jogador voce quer atacar?\n")
	x = input("Qual a posicao x que voce quer atacar?\n")
	y = input("Qual a posicao y que voce quer atacar?\n")
	# Empacota mensagem de ataque
	# O 1 representa ataque, o atacante eh este jogador, 
	# o 'jogador' eh o atacado, x e y sao as posicoes do ataque
	mensagem = "1_"+str(atacante)+"_"+str(jogador)+"_"+str(x)+"_"+str(y)
	return mensagem

#Agrupa as mensagens em uma so para poder enviar
def enviaMensagem(mensagens, sock, udp_ip, udp_port):
	msg = '.'.join(mensagens)
	print("enviando mensagem")
	sock.sendto(msg, (udp_ip, udp_port))	
	return

#Traduz a mensagem para poder printar para o usuario
def leMensagem(partes):
	if(partes[0] == '2'):
		print("O navio do jogador "+partes[1]+" afundou.")
	elif(partes[0] == '3'):
		print("O jogador "+partes[1]+" perdeu e saiu do jogo")
	elif(partes[0] == '4'):
		print("O navio do jogador "+partes[1]+" nao afundou, porem voce acertou as posicoes: x="+partes[3]+", y="+partes[4]+".")	
	elif(partes[0] == '5'):
		print("O ataque ao jogador "+partes[1]+ "nas posicoes : x="+partes[3]+", y="+partes[4]+ " errou.")
	else:
		print("Erro: Mensagem nao conhecida.")	

#Conferir se essa posicao vai se sobrepor a outro navio
def checaSobreposicao(tabuleiro, tamanho, x1, x2, y1, y2):
	sobrepoe = False
	if(x1 < x2):
		for x in range(x1, x2+1):
			if(y1 < y2):
				for y in range(y1, y2+1):
					if(tabuleiro[x*tamanho+y] != "--"):
						sobrepoe = True
			else:
				for y in range(y2, y1+1):
					if(tabuleiro[x*tamanho+y] != "--"):
						sobrepoe = True
	else:
		for x in range(x2, x1+1):
			if(y1 < y2):
				for y in range(y1, y2+1):
					if(tabuleiro[x*tamanho+y] != "--"):
						sobrepoe = True
			else:
				for y in range(y2, y1+1):
					if(tabuleiro[x*tamanho+y] != "--"):
						sobrepoe = True
	if(sobrepoe == True):
		print("Erro: Este navio se sobrepoe a outro")	
	return sobrepoe

#Checa mensagem de ataque, atualiza tabuleiro e variaveis e retorna resultado
def checaAtaque(partes, tabuleiro, tamanho, num_navios):
	x = partes[3]
	y = partes[4]
	if(tabuleiro[x*tamanho+y] == "--"):
		return "errou"
	else:	
		navio = tabuleiro[x*tamanho+y]
		
		#realiza ataque
		tabuleiro[x*tamanho+y] = "--"

		for linha in range(tamanho):
			for coluna in range(tamanho):
				#Testa se navio nao afundou totalmente
				if(tabuleiro[x*tamanho+y] == navio):
					return "acertou"
				#Testa se afundou navio
				elif(tabuleiro[x*tamanho+y] != "--"):
					num_navios = num_navios -1
					return "afundou"
		#Se a funcao nao retornou ate agora, significa que jogador perdeu
		return "perdeu"	

#TODO como implementar timeout ? Acho que timeout vale caso demore muito para receber ack/nack
#TODO arrumar este tamanho
TAM_MSG = 1024

#Pergunta a ordem que esse jogador vai jogar (se eh o primeiro ou nao)
ordem = input("Qual eh a ordem que voce vai jogar? Responder: 1, 2, 3 ou 4\n")

tam_tabuleiro = input("Qual o tamanho do tabuleiro? ")

#Le posicoes dos navios e quantidade deles
num_navios = input("Quantos navios voce tera? ")

tam_navio = []
tabuleiro = []

iniciaTabuleiro(tabuleiro, tam_tabuleiro);

for navio in range(num_navios):
	while True:
		tam = input("Este eh o navio de numero "+str(navio)+", qual o tamanho dele? ")
		if (tam <= tam_tabuleiro and tam > 0):
			break
		print("o tamanho do navio eh maior que o tamanho do tabuleiro ou eh < 1")

	tam_navio.append(tam)
	
	while True:
		x1 = input("Em qual posicao x o navio comeca? Digite um numero de 0 a "+str(tam_tabuleiro-1)+": ");		
		y1 = input("Em qual posicao y o navio comeca? Digite um numero de 0 a "+str(tam_tabuleiro-1)+": ");	
		x2 = input("Em qual posicao x o navio termina? Digite um numero de 0 a "+str(tam_tabuleiro-1)+": ");		
		y2 = input("Em qual posicao y o navio termina? Digite um numero de 0 a "+str(tam_tabuleiro-1)+": ");
		
		sobrepoe = checaSobreposicao(tabuleiro, tam_tabuleiro, x1, x2, y1, y2)
		
		#conferindo se navio fica dentro do tabuleiro
		if((sobrepoe == False) and (x1 >= 0) and (x1 < tam_tabuleiro) and (x2 >= 0) and (x2 < tam_tabuleiro) and (y1 >=0) and (y1 <= tam_tabuleiro) and (y2 >= 0) and (y2 <= tam_tabuleiro)):
			#conferindo se tamanho do navio realmente eh do tamanho escolhido
			if(((math.fabs(y1-y2) == 0) and (math.fabs(x1-x2) == (tam-1))) or ((math.fabs(y1-y2) == (tam-1)) and (math.fabs(x1-x2) == 0))):
				adicionaNavio(x1, y1, x2, y2, tabuleiro, tam_tabuleiro, navio)
				imprimeTabuleiro(tabuleiro, tam_tabuleiro)
				break
		print("Erro: O tamanho do navio nao corresponde as posicoes escolhidas ou as posicoes nao respeitam o tabuleiro");
		
udp_port = input("Qual sera o port utilizado?\n")
#udp_ip1 = raw_input("Qual o IP desta maquina?\n")
udp_ip2 = raw_input("Qual o IP da proxima maquina?\n") 
#udp_ip3 = raw_input("Qual o IP da maquina anterior?\n")

#Conecta socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Liga o socket com a maquina que vai enviar para esta
sock.bind(('', udp_port))

#Lista de mensagens a enviar no anel
mensagensEnviar = []

#Lista de mensagens para repassar imediatamente, ja que nao sao para este jogador
aRepassar = []

#Lista de mensagens recebidas do anel
mensagensRec = []

#Mensagens separadas para poder operar sobre elas.
mensagens = []

#Indica se ha bastao para poder enviar novas mensagens
bastao = False

#Se for o primeiro a jogar, envia primeiro ataque
if(ordem == 1):
	#Adicionando bastao as mensagens	
	mensagensEnviar.append(geraAtaque(ordem))
	mensagensEnviar.append("9_9_9_9_9_9")
	enviaMensagem(mensagensEnviar, sock, udp_ip2, udp_port)
	del mensagensEnviar[:]

#loop de aguardo de mensagem
while True:
	#Recebe mensagens
	mensagensRec, addr = sock.recvfrom(TAM_MSG)
	print(mensagensRec)

	if(addr[0] == udp_ip3):
		mensagens = mensagensRec.split('.')
		#Iterando pelas mensagens
		for msg in mensagens:
			print ("a mensagem recebida foi: " + msg)

			#Dividindo cada parte da mensagem
			partes = msg.split("_")

			#Se mensagem eh para este jogador
			if(partes[2] == str(ordem)):

				#Se mensagem eh aviso de que afundou navio do atacado 
				if(partes[0] == '2'):
					#Marca mensagem recebida como lida/ACK
					mensagensEnviar.append(partes[0]+"_"+partes[1]+"_"+partes[2]+"_"+partes[3]+"_"+partes[4]+"_1")
					#Cria mensagem aberta a todos e envia mensagem
					mensagensEnviar.append("6_"+str(ordem)+"_"+partes[1]+"_"+partes[3]+"_"+partes[4]+"_0")		
					#TODO COLOCAR NO TIMEOUT	

				#Se mensagem eh aviso que jogador saiu do jogo			
				elif(partes[0] == '3'):
					#Marca mensagem recebida como lida/ACK
					mensagensEnviar.append(partes[0]+"_"+partes[1]+"_"+partes[2]+"_"+partes[3]+"_"+partes[4]+"_1")
					#ACK mensagem, cria mensagem aberta a todos e envia mensagem
					mensagensEnviar.append("7_"+str(ordem)+"_"+partes[1]+"_"+partes[3]+"_"+partes[4]+"_0")		
					#TODO COLOCAR NO TIMEOUT	

				#Se eh mensagem de que ataque falhou ou acertou nao completamente
				elif(partes[0] == '4' or partes[0] == 5):
					#Marca mensagem recebida como lida/ACK
					mensagensEnviar.append(partes[0]+"_"+partes[1]+"_"+partes[2]+"_"+partes[3]+"_"+partes[4]+"_1")
					#Imprime mensagem na tela
					leMensagem(partes)

				#Se eh uma mensagem de ataque
				elif(partes[0] == '1'):
					#Marca mensagem recebida como lida/ACK
					mensagensEnviar.append(partes[0]+"_"+partes[1]+"_"+partes[2]+"_"+partes[3]+"_"+partes[4]+"_1")
					ataque = checaAtaque(partes, tabuleiro, tam_tabuleiro, num_navios) 
					
					#Se ataque acertou um navio nao-completamente ou errou,
					if(ataque == 'acertou'):
						#adiciona resultado ao atacante as msgs 
						mensagensEnviar.append("4_"+str(ordem)+"_"+partes[1]+"_"+partes[3]+"_"+partes[4]+"_0")
						#TODO COLOCAR NO TIMEOUT	

					#Se ataque errou
					elif(ataque == 'errou'):
						#adiciona resultado ao atacante as msgs e um ACK
						mensagensEnviar.append("5_"+str(ordem)+"_"+partes[1]+"_"+partes[3]+"_"+partes[4]+"_0")
						#TODO COLOCAR NO TIMEOUT	

					#Se afundou navio completamente, 
					elif(ataque == 'afundou'):
						#Retira mensagem recebida e adiciona resultado ao atacante as msgs como um ACK
						mensagensEnviar.append("2_"+str(ordem)+"_"+partes[1]+"_"+partes[3]+"_"+partes[4]+"_0")
						#TODO COLOCAR NO TIMEOUT	

					#Se todos os navios afundaram, 
					elif(ataque == 'perdeu'):
						#Avisa que perdeu atacante e sai do jogo(e do loop)
						mensagensEnviar.append("3_"+str(ordem)+"_"+partes[1]+"_"+partes[3]+"_"+partes[4]+"_0")
						#TODO COLOCAR NO TIMEOUT	
						#TODO tirar jogador do jogo quando receber ack desta mensagem
					
				else:
					#NACK
					mensagensEnviar.append(partes[0]+"_"+str(ordem)+"_"+partes[1]+"_"+partes[3]+"_"+partes[4]+"_9") 

			#Se mensagem foi enviada por este mesmo jogador
			elif(partes[1] == str(ordem)):				
				#Se foi mensagem aberta de navio afundado ou jogador saiu do jogo de outro jogador, 
				if(partes[0] == '6' or partes[0] == '7'):
					#Checa se todo mundo recebeu (se os 4 leram)
					if(partes[5] == "3"):
						leMensagem(partes)
						#retira mensagem do anel
						print("Retirando mensagem: "+msg+" do anel")
					else:
						#Passa mensagem de novo mas com "lido" = 0
						mensagensEnviar.append(partes[0]+"_"+partes[1]+"_"+partes[2]+"_"+partes[3]+"_"+partes[4]+"_0")
				#Se foi um ACK/NACK, retira mensagem de ACK/NACK
				elif(partes[5] == '1' or partes[5] == '0'):
					print("Retirando mensagem de ACK/NACK: "+msg+" do anel")
					#TODO se foi um NACK tem que reenviar a mensagem referente ao NACK
					#TODO se foi um ACK/NACK, retira mensagem do timeout
				#TODO retira mensagem do timeout

			#Se mensagem eh aberta: aviso de que afundou navio de outro jogador
			#(e/ou saiu do jogo) que nao foi atacado por este,
			elif(partes[0] == '6' or partes[0] == '7'):
				#le e repassa mensagem
				leMensagem(partes)	
				#adiciona lido deste jogador para esta mensagem
				aRepassar.append(partes[0]+"_"+partes[1]+"_"+partes[2]+"_"+partes[3]+"_"+partes[4]+"_"+str(int(partes[5])+1))
				enviaMensagem(aRepassar, sock, udp_ip2, udp_port)
				del aRepassar[:]
			
			#Se mensagem nao eh para este nem enviada por este e nao eh o bastao, repassa para frente
			elif(partes[0] != '9'):
				aRepassar.append(msg)
				enviaMensagem(aRepassar, sock, udp_ip2, udp_port)
				del aRepassar[:]

			#Se mensagem eh bastao, o primeiro elemento sera 9, realiza ataque
			elif(partes[0] == '9'):
				bastao = True
				mensagensEnviar.append("9_9_9_9_9_9")
				mensagensEnviar.append(geraAtaque(ordem))
				#TODO timeout de ack de ataque
			else:
				print("Erro: mensagem "+msg+" nao eh conhecida")

		# repassa bastao com mensagens
		if(bastao == True):
			enviaMensagem(mensagensEnviar, sock, udp_ip2, udp_port)
			#limpando as variaveis
			bastao = False
			del mensagensEnviar[:]
			
