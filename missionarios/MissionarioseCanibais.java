import java.util.LinkedList;
import java.util.List;

import busca.BuscaLargura;
import busca.Estado;
import busca.Nodo;
import busca.MostraStatusConsole;

public class MissionarioseCanibais implements Estado {

    final int m; // qtd missionarios na esquerda
    final int c; // qtd canibais na esquerda
    final int barco; // 1 = esquerda, 2 = direita
    final String op; 

    public MissionarioseCanibais(int m, int c, int barco, String op) {
        this.m = m;
        this.c = c;
        this.barco = barco;
        this.op = op;
    }

    @Override
    public String getDescricao() {
        return "Problema dos Missionarios e Canibais";
    }

    @Override
    public boolean ehMeta() {
        return this.m == 0 && this.c == 0 && this.barco == 0;
    }

    @Override
    public int custo() {
        return 1;
    }

    // restricoes
    private boolean estadoValido(int miss, int can) {
        if (miss < 0 || can < 0 || miss > 3 || can > 3) {
            return false;
        }
        
        int missDestino = 3 - miss;
        int canDestino = 3 - can;

        // verifica esquerda
        if (miss > 0 && can > miss) {
            return false;
        }
        
        // verifica direita
        if (missDestino > 0 && canDestino > missDestino) {
            return false;
        }

        return true;
    }

    /**
     * tenta aplicar um movimento e se eh valido poem aos sucessores
     */
    private void tentarMover(int qtM, int qtC, List<Estado> sucessores) {
        int novoM, novoC, novoBarco;
        String direcao;

        if (this.barco == 1) { 
            // barco esquerda pra direita
            novoM = this.m - qtM;
            novoC = this.c - qtC;
            novoBarco = 0;
            direcao = "indo para a direita";
        } else { 
            // barco direita pra esquerda
            novoM = this.m + qtM;
            novoC = this.c + qtC;
            novoBarco = 1;
            direcao = "voltando para a esquerda";
        }

        // se nao interferir nas restricoes...
        if (estadoValido(novoM, novoC)) {
            String operacao = "Moveu " + qtM + "M e " + qtC + "C " + direcao;
            MissionarioseCanibais novoEstado = new MissionarioseCanibais(novoM, novoC, novoBarco, operacao);
            sucessores.add(novoEstado);
        }
    }

    @Override
    public List<Estado> sucessores() {
        List<Estado> visitados = new LinkedList<Estado>();

        // tentar todas as combinacoes
        tentarMover(1, 0, visitados);
        tentarMover(2, 0, visitados); 
        tentarMover(0, 1, visitados); 
        tentarMover(0, 2, visitados); 
        tentarMover(1, 1, visitados); 

        return visitados;
    }

    @Override
    public boolean equals(Object o) {
        if (o instanceof MissionarioseCanibais) {
            MissionarioseCanibais e = (MissionarioseCanibais) o;
            return this.m == e.m && 
                   this.c == e.c && 
                   this.barco == e.barco;
        }
        return false;
    }

    @Override
    public int hashCode() {
        return ("" + this.m + this.c + this.barco).hashCode();
    }

    @Override
    public String toString() {
        String margemEsq = "Esq: " + this.m + "M/" + this.c + "C";
        String margemDir = "Dir: " + (3 - this.m) + "M/" + (3 - this.c) + "C";
        String posBarco = (this.barco == 1) ? "[Barco na Esq]" : "[Barco na Dir]";
        
        return String.format("%-15s | %-15s | %s -> %s\n", margemEsq, margemDir, posBarco, op);
    }

    public static void main(String[] args) {
        MissionarioseCanibais estadoInicial = new MissionarioseCanibais(3, 3, 1, "Estado Inicial");

        System.out.println("Buscando solucao...");
        
        // largura nesse caso é melhor
        Nodo n = new BuscaLargura(new MostraStatusConsole()).busca(estadoInicial);
        
        if (n == null) {
            System.out.println("Sem solucao!");
        } else {
            System.out.println("Solucao encontrada:\n");
            System.out.println(n.montaCaminho());
        }
    }
}