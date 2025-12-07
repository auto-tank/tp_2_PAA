
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Ajuste de path para importação dos módulos irmãos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from b_algoritmo_linear import mochila_espaco_linear
    from c_prog_dinamica import solucao_programacao_dinamica
    from d_algoritmo_aproximado import algoritmo_guloso
except ImportError as e:
    print(f"Erro de importação: {e}")
    sys.exit(1)

def gerar_instancia(n):
    """
    Gera uma instância aleatória do problema da mochila.
    L é proporcional a n para garantir que a complexidade O(n*L) cresça quadraticamente com n.
    """
    L = n * 50 # Capacidade razoável
    
    # Pesos e utilidades aleatórios
    # Pesos variam até L/4 para que caibam pelo menos 4 itens grandes ou muitos pequenos
    pesos = np.random.randint(1, max(2, L // 4), size=n).tolist()
    utilidades = np.random.randint(1, 100, size=n).tolist()
    
    return pesos, utilidades, L

def executar_analise():
    print("=== Análise Comparativa de Algoritmos ===")
    
    # Tamanhos de problemas para teste
    # Como DP e Linear são O(n*L) e L cresce com n, a complexidade efetiva é O(n^2).
    # Valores moderados para não demorar demais.
    tamanhos_n = [50, 100, 200, 300, 400]
    
    tempos_linear = []
    tempos_dp = []
    tempos_guloso = []
    
    qualidade_guloso = [] # Razão (Valor Guloso / Valor Ótimo)
    
    print(f"Executando testes para n: {tamanhos_n}")
    
    for n in tamanhos_n:
        pesos, utilidades, L = gerar_instancia(n)
        print(f"-> Rodando n={n}, L={L}...", end=" ", flush=True)
        
        # 1. Algoritmo Linear (Espaço O(L))
        start = time.time()
        otimo_linear = mochila_espaco_linear(pesos, utilidades, L)
        end = time.time()
        tempos_linear.append(end - start)
         
        # 2. DP Clássica (Espaço O(nL), com Matriz e Recuperação)
        start = time.time()
        otimo_dp, _, _ = solucao_programacao_dinamica(pesos, utilidades, L)
        end = time.time()
        tempos_dp.append(end - start)
        
        # Verificação de consistência (ambos exatos devem dar mesmo valor)
        assert otimo_linear == otimo_dp, f"Discrepância! Linear={otimo_linear}, DP={otimo_dp}"
        
        # 3. Algoritmo Guloso (Aproximado)
        start = time.time()
        val_guloso, _ = algoritmo_guloso(pesos, utilidades, L)
        end = time.time()
        tempos_guloso.append(end - start)
        
        # Cálculo da qualidade
        razao = val_guloso / otimo_linear if otimo_linear > 0 else 1.0
        qualidade_guloso.append(razao)
        
        print(f"OK. (Linear={tempos_linear[-1]:.4f}s, DP={tempos_dp[-1]:.4f}s, Guloso={tempos_guloso[-1]:.4f}s, Qualidade={razao:.2%})")
        
    # --- Geração dos Gráficos ---
    
    # 1. Gráfico de Tempo
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos_n, tempos_linear, label='Exato: Espaço Linear O(L)', marker='o', linestyle='--')
    plt.plot(tamanhos_n, tempos_dp, label='Exato: PD Clássica (Matriz)', marker='s')
    plt.plot(tamanhos_n, tempos_guloso, label='Aproximado: Guloso O(n log n)', marker='^')
    
    plt.xlabel('Número de Itens (n)')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Comparação de Tempo: Exatos vs Aproximado')
    plt.legend()
    plt.grid(True)
    
    # Salvar
    output_time = 'tp_2_PAA/project/grafico_tempos.png'
    plt.savefig(output_time)
    print(f"\nGráfico de tempos salvo em: {output_time}")
    
    # 2. Gráfico de Qualidade
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos_n, qualidade_guloso, label='Razão de Aproximação', color='green', marker='d')
    plt.axhline(y=1.0, color='r', linestyle='--', label='Ótimo (100%)')
    
    plt.xlabel('Número de Itens (n)')
    plt.ylabel('Qualidade (Valor Guloso / Valor Ótimo)')
    plt.title('Qualidade da Solução Aproximada (Guloso)')
    plt.legend()
    plt.grid(True)
    plt.ylim(0.5, 1.05) # Focar na parte superior (geralmente > 50%)
    
    output_qual = 'tp_2_PAA/project/grafico_qualidade.png'
    plt.savefig(output_qual)
    print(f"Gráfico de qualidade salvo em: {output_qual}")

if __name__ == "__main__":
    executar_analise()
