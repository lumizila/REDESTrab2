### Implementar um jogo de batalha naval de 4 jogadores
#### Em python usando Socket Datagram
#### Imprementar o controle de acesso de passagem de bastao

- O relatorio eh obrigatorio
- Valor: 1,0
- Apresentacoes no lab
- Codigo por email depois da apresentacao

### Detalhes sobre a implementacao

Podem ser parametros, e em caso negativo:
- Tabuleiro 5x5
- 2 navios 3x1

#### Outros detalhes

- Inicio: jogadores distribuem seus navios pelo tabuleiro 
- Jogador com bastao escolhe um openente e uma area pra atacar, cria e envia a mensagem
- Jogador sem bastao que nao foi atacado: repassa mensagem
- Jogador sem bastao atacado: adiciona resultado do ataque na mensagem e manda para frente, mas se o navio AFUNDOU a mensagem deve ir para todos os jogadores. 
- Quem coloca mensagem no anel eh quem tira
- Quando um navio eh afundado, todas as maquinas devem ser avisadas que o navio X do jogador Y foi afundado nas posicoes z1, z2, z3. 
- Bastao nao eh temporizado
- Deve ter timeout na mensagem
- Jogador com tudo afundado para de jogar

#### Maquinas para conectar

Para este trabalho, vamos ter que conectar em 4 maquinas diferentes, que podem ser:
-macalan
-dalmore
-
-

A porta usada pode ser a: 5318

