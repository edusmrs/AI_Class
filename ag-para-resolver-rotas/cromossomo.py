import copy
import random
from collections import Counter

from util import Util



class Cromossomo:
    def __init__(self, palavra):  
        self.palavra = palavra
        self.aptidao = self.calcular_aptidao()
        
    def calcular_aptidao(self):
        nota = 0
        
        # se uma cidade for maior que a prox, tem uma penalidade (10 por ocorrencia)
        for i in range(0,len(self.palavra)-1):
            if (self.palavra[i] > self.palavra[i+1]):
                nota += 10

        # se uma cidade for repetida, tem uma penalidade (20 por repeticao)
        contagem = Counter(self.palavra) 

        for ocorrencias in contagem.values():
            if ocorrencias > 1:
                pares = (ocorrencias * (ocorrencias - 1)) / 2 # calcular o numero de pares de repeticoes
                nota += 20 * pares
        return nota
    
    def __str__(self):
        return f'{self.palavra} - {self.aptidao}'
    
    def __eq__(self, other):
        if isinstance(other, Cromossomo):
            return self.palavra == other.palavra
        return False
        

    @staticmethod
    def gerar_populacao(populacao, tamanho_populacao):
        palavra = list()
        for i in range(tamanho_populacao):
            for i in range(1,10):
                palavra.append(i)
            random.shuffle(palavra)
            populacao.append(Cromossomo(copy.deepcopy(palavra)))            
            palavra.clear()   

    @staticmethod
    def exibir_populacao(populacao, numero_geracao):
        print('Geração...', numero_geracao)
        for individuo in populacao:
            print(individuo)

    @staticmethod
    def selecionar(populacao, nova_populacao, taxa_selecao):
        #definir quantos serao selecionados
        #len(populacao)             - 100
        #quantidade_selecionados    - taxa_selecao
        quantidade_selecionados = int(len(populacao) * taxa_selecao / 100)

        torneio = list()

        #elistimo - o mais apto sempre é selecionado
        nova_populacao.append(populacao[0])

        i = 1
        while (i < quantidade_selecionados):
            c1 = populacao[ random.randrange( len(populacao) ) ]

            while (True):
                c2 = populacao[ random.randrange( len(populacao) ) ]
                if not c1.__eq__(c2):
                    break

            while (True):
                c3 = populacao[ random.randrange( len(populacao) ) ]
                if (not c1.__eq__(c3)) and (not c2.__eq__(c3)):
                    break
            
            torneio.append(c1)
            torneio.append(c2)
            torneio.append(c3)


            # como a nota agora aje como penalidade, reserve=False
            torneio.sort(key=lambda cromossomo: cromossomo.aptidao, reverse=False)
            selecionado = torneio[0]
            if selecionado not in nova_populacao:
                nova_populacao.append(selecionado)
                i+=1

            torneio.clear()


    @staticmethod
    def reproduzir(populacao, nova_populacao, taxa_reproducao):
        #definir a quantidade de reproduzidos
        #len(populacao)             - 100
        #quantidade_reproduzidos    - taxa_reproducao
        quantidade_reproduzidos = int(len(populacao) * taxa_reproducao / 100)

        for i in range(int(quantidade_reproduzidos/2)+1):
            #sorteia um pai entre os primeiros 20% da populacao
            cromossomo_pai = populacao[ random.randrange( len(populacao) ) ]

            while (True):
                cromossomo_mae = populacao[ random.randrange( len(populacao) ) ]
                if cromossomo_pai != cromossomo_mae:
                    break

            pai = cromossomo_pai.palavra
            mae = cromossomo_mae.palavra

            # esse tipo de cruzamento é uma porcaria pra resolver problema de rota,
            # pq gera filhos com cidades repetidas e outras faltando, mas é o mais simples de implementar
            # certo mesmo era fazer um cruzamento que pelo menos n repetisse as cidadas

            #primeira metade do pai + segunda metade da mae
            primeira_metade = pai[0 : int(len(pai)/2)] 
            segunda_metade = mae[int(len(mae)/2) : len(mae)]

            filho1 = primeira_metade + segunda_metade
            # print(filho1)

            #primeira metade da mae + segunda metade do pai
            primeira_metade = mae[0 : int(len(mae)/2)] 
            segunda_metade = pai[int(len(pai)/2) : len(pai)]
            filho2 = primeira_metade + segunda_metade
            # print(filho2)

            nova_populacao.append(Cromossomo(filho1))
            nova_populacao.append(Cromossomo(filho2))

            #podar os excedentes
            while (len(nova_populacao) > len(populacao)):
                nova_populacao.pop()


    @staticmethod
    def mutar(populacao):
        quantidade_mutantes = random.randrange(int(len(populacao)))
        
        while (quantidade_mutantes > 0):
            posicao_mutante = random.randrange(len(populacao))
            mutante = populacao[posicao_mutante]
            

            # pra resolver o problema de rota, ideal era trocar a cidade de lugar em vez de substituir
            # visto que pra rota todas as cidades devem estar presentes.

            posicao_gene = random.randrange(len(mutante.palavra))
            nova_cidade = random.randrange(1, 10)
            
            mutante.palavra[posicao_gene] = nova_cidade

            # # sortear duas posicoes
            # pos1 = random.randrange(len(mutante.palavra))
            # pos2 = random.randrange(len(mutante.palavra))
            
            # # trocar os valores de lugar em vez de substituir
            # mutante.palavra[pos1], mutante.palavra[pos2] = mutante.palavra[pos2], mutante.palavra[pos1]

            # atualizar nota
            mutante.aptidao = mutante.calcular_aptidao()
            
            quantidade_mutantes -= 1

            