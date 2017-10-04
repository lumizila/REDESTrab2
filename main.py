#!/usr/bin/python
import sys
import math

#imprime o tabuleiro
def imprimeTabuleiro(tabuleiro, tamanho):
	for x in range(tamanho):
		for y in range(tamanho):
			sys.stdout.write(str(tabuleiro[x*tamanho+y])+" ")
		print("")
	return

#inicia tabuleiro com 0 em todas as posicoes
def iniciaTabuleiro(tabuleiro, tamanho):
	for x in range(tamanho):
		for y in range(tamanho):
			tabuleiro.append(0)
	return

#adiciona navio ao tabuleiro
def adicionaNavio(x1, y1, x2, y2, tabuleiro, tam)
	


print ("inicio do programa...")

#Pergunta a ordem que esse jogador vai jogar (se eh o primeiro ou nao)
ordem = input("Qual eh a ordem que voce vai jogar? Responder: 1, 2, 3 ou 4\n")
#Le posicoes dos navios e quantidade deles
num_navios = input("Quantos navios voce tera?\n")
tam_tabuleiro = input("Qual o tamanho do tabuleiro?\n")
tam_navio = []
tabuleiro = []

iniciaTabuleiro(tabuleiro, tam_tabuleiro);
imprimeTabuleiro(tabuleiro, tam_tabuleiro);

for navio in range(num_navios):
	while True:
		tam = input("Este eh o navio de numero "+str(navio)+", qual o tamanho dele?\n")
		if (tam <= tam_tabuleiro):
			break
		print("o tamanho do navio eh maior que o tamanho do tabuleiro")

	tam_navio.append(tam)
	
	while True:
		x1 = input("Em qual posicao x o navio comeca? Digite um numero de 0 a "+str(tam_tabuleiro-1)+"\n");		
		y1 = input("Em qual posicao y o navio comeca? Digite um numero de 0 a "+str(tam_tabuleiro-1)+"\n");	
		x2 = input("Em qual posicao x o navio termina? Digite um numero de 0 a "+str(tam_tabuleiro-1)+"\n");		
		y2 = input("Em qual posicao y o navio termina? Digite um numero de 0 a "+str(tam_tabuleiro-1)+"\n");	
		if((x1 >= 0) and (x1 < tam_tabuleiro) and (x2 >= 0) and (x2 < tam_tabuleiro) and (y1 >=0) and (y1 <= tam_tabuleiro) and (y2 >= 0) and (y2 <= tam_tabuleiro)):
			if(((math.fabs(y1-y2) != tam) and (math.fabs(x1-x2) != 0)) != ((math.fabs(y1-y2) != 0) and (math.fabs(x1-x2) != tam))):
				adicionaNavio(x1, y1, x2, y2, tabuleiro, tam)
				imprimeTabuleiro(tabuleiro, tam_tabuleiro)
				break
		print("O tamanho do navio nao corresponde as posicoes escolhidas ou as posicoes nao respeitam o tabuleiro");
		

#Printa tabuleiro inicial

#Conecta socket

#Se for o primeiro a jogar, envia primeiro ataque

#loop de aguardo de mensagem
	#Recebe mensagem
		#Se mensagem eh bastao, realiza/envia ataque e repassa bastao
		#Se mensagem eh para este jogador
			#Se ataque acertou um navio nao-completamente ou errou, 
				#Retira mensagem recebida e envia resultado ao atacante
			#Se afundou navio completamente, 
				#Retira mensagem recebida e envia resultado ao atacante
			#Se todos os navios afundaram, 
				#Retira mensagem recebida e avisa que perdeu ao atacante e sai do jogo(e do loop)
			#Se mensagem eh aviso de que afundou navio de outro jogador que nao foi atacado por este,
				#le e repassa mensagem
			#Se mensagem eh aviso de que afundou navio do atacado ou que atacado saiu do jogo, 
				#retira mensagem, cria mensagem aberta a todos e envia mensagem
		#Se mensagem foi enviada por este mesmo jogador
			#Se foi mensagem aberta de navio afundado ou jogador saiu do jogo de outro jogador, 
				#retira mensagem do anel
			#Se foi mensagem de ataque, ERRO, a mensagem nao chegou ao remetente
			#Se foi mensagem de que atacante acertou este jogador, ERRO, a msg nao chegou no remetente
		#Se mensagem nao eh para este nem enviada por este, repassa para frente
		
