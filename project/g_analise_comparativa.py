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
    """
    Executa a bateria de testes comparativos solicitada no Item G.
    
    Relacionamento com os itens do trabalho:
    - Item E (Complexidade): Os tempos medidos aqui validam experimentalmente a análise teórica 
      (Linear/DP crescem quadraticamente com N*L, Guloso cresce linearithmicamente).
    - Item F (Qualidade): A razão calculada (Guloso/Ótimo) fornece a análise empírica da 
      qualidade da aproximação.
    - Item G (Testes Aleatórios): Este script gera as entradas aleatórias e compara os resultados.
    """
    print("=== Análise Comparativa de Algoritmos (Item G) ===")
    
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
        
        # --- Comparação 1: Tempo de Execução (Item E) ---
        # Medimos o tempo de parede (wall-clock) para cada algoritmo para validar a análise de complexidade.
        
        # 1. Algoritmo Linear (Exato, Otimizado em Espaço - Item B)
        start = time.time()
        otimo_linear = mochila_espaco_linear(pesos, utilidades, L)
        end = time.time()
        tempos_linear.append(end - start)
         
        # 2. DP Clássica (Exato, com Recuperação de Itens - Item C)
        # Espera-se que seja ligeiramente mais lento que o linear devido ao overhead da matriz.
        start = time.time()
        otimo_dp, _, _ = solucao_programacao_dinamica(pesos, utilidades, L)
        end = time.time()
        tempos_dp.append(end - start)
        
        # --- Validação Cruzada ---
        # Como ambos (Linear e DP) são métodos exatos, eles OBRIGATORIAMENTE
        # devem encontrar o mesmo valor ótimo. Se não, há um bug.
        assert otimo_linear == otimo_dp, f"Discrepância! Linear={otimo_linear}, DP={otimo_dp}"
        
        # 3. Algoritmo Guloso (Aproximado - Item D)
        # Espera-se que seja muito mais rápido (ordens de magnitude), pois é O(n log n).
        start = time.time()
        val_guloso, _ = algoritmo_guloso(pesos, utilidades, L)
        end = time.time()
        tempos_guloso.append(end - start)
        
        # --- Comparação 2: Qualidade da Solução (Relacionado ao Item F) ---
        # Calculamos a razão entre o valor encontrado pelo Guloso e o Valor Ótimo.
        # Razão = 1.0 (ou 100%) significa que o Guloso encontrou a solução ótima.
        # Razão < 1.0 (ex: 0.95) significa que o Guloso encontrou 95% do valor possível.
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
    # Usa caminho relativo considerando execução da raiz ou da pasta project
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_time = os.path.join(output_dir, 'grafico_tempos.png')
    
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
    
    output_qual = os.path.join(output_dir, 'grafico_qualidade.png')
    plt.savefig(output_qual)
    print(f"Gráfico de qualidade salvo em: {output_qual}")

if __name__ == "__main__":
    executar_analise()
