import os
from cromossomo import Cromossomo

tamanho_populacao = 500
quantidade_geracoes = 2000
taxa_selecao = 25
taxa_reproducao = 100 - taxa_selecao
frequencia_mutacao = 5 # cada 5 geracoes

populacao = list()
nova_populacao = list()

Cromossomo.gerar_populacao(populacao, tamanho_populacao)
populacao.sort(key=lambda cromossomo: cromossomo.aptidao)

print(f"geração 0 | melhor Rota: {populacao[0]}")

for i in range(1, quantidade_geracoes):
    Cromossomo.selecionar(populacao, nova_populacao, taxa_selecao)
    Cromossomo.reproduzir(populacao, nova_populacao, taxa_reproducao)

    if i % frequencia_mutacao == 0:
        Cromossomo.mutar(nova_populacao)
 
    populacao.clear()
    populacao.extend(nova_populacao)
    nova_populacao.clear()
    
    populacao.sort(key=lambda cromossomo: cromossomo.aptidao)
    
    print(f"geracao {i} | melhor atual: {populacao[0]}")

    if populacao[0].aptidao == 0:
        print(f"\nrota perfeita encontrada na geração {i}!")
        break

print("\nfinal")
print(f"melhor solução encontrada: {populacao[0]}")