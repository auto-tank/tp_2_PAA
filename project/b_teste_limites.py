import time
import sys
import numpy as np
# Adiciona o diretório atual ao path para importar o módulo local
sys.path.append('tp_2_PAA/project') 

try:
    from b_algoritmo_linear import mochila_espaco_linear
except ImportError:
    # Tenta importar assumindo que estamos na pasta project
    from b_algoritmo_linear import mochila_espaco_linear

def run_stress_test():
    print("=== Teste de Carga: Algoritmo de Espaço Linear ===")
    print("Objetivo: Encontrar o tamanho do maior problema resolvido em ~60s ou limite de memória.")
    
    # Inicia com um problema pequeno
    n = 1000
    L = 10000
    time_limit = 30.0 # limite de tempo seguro para não travar o PC do usuário por muito tempo
    
    max_solved_n = 0
    max_solved_L = 0
    last_time = 0
    
    try:
        while True:
            # Gera dados aleatórios
            # Pesos entre 1 e L/2 (para garantir que cabem alguns itens)
            # Utilidades aleatórias
            pesos = np.random.randint(1, max(2, L // 10), size=n).tolist()
            utilidades = np.random.randint(1, 1000, size=n).tolist()
            
            print(f"Testando: N={n}, L={L}...", end=" ", flush=True)
            
            start_time = time.time()
            _ = mochila_espaco_linear(pesos, utilidades, L)
            end_time = time.time()
            elapsed = end_time - start_time
            
            print(f"Tempo: {elapsed:.4f}s")
            
            if elapsed > time_limit:
                print(f"-> Limite de tempo ({time_limit}s) atingido.")
                break
                
            max_solved_n = n
            max_solved_L = L
            last_time = elapsed
            
            # Estratégia de crescimento:
            # Aumentamos N e L. A complexidade é O(N*L).
            # Se dobrarmos ambos, o tempo deve quadruplicar (4x).
            n = int(n * 1.5)
            L = int(L * 1.5)
            
    except MemoryError:
        print("\n-> Erro de Memória (MemoryError) atingido! O vetor DP ficou grande demais.")
    except Exception as e:
        print(f"\n-> Erro inesperado: {e}")
        
    print("\n=== Resultados ===")
    print(f"Maior problema resolvido com sucesso: N={max_solved_n}, L={max_solved_L}")
    print(f"Tempo da última execução bem-sucedida: {last_time:.4f}s")
    
    # Estimativa para 10x maior
    print("\n--- Estimativa para entrada 10x maior ---")
    print("Considerando que a complexidade é O(N * L):")
    print("Se a entrada aumenta 10x (N -> 10N, L -> 10L), o trabalho aumenta 100x.")
    print("Se a entrada aumenta 10x apenas em N (N -> 10N), o trabalho aumenta 10x.")
    
    if last_time > 0:
        est_10x_ambos = last_time * 100
        est_10x_n = last_time * 10
        print(f"Estimativa de tempo (N*10 e L*10): {est_10x_ambos/60:.2f} minutos ({est_10x_ambos:.2f}s)")
        print(f"Estimativa de tempo (apenas N*10): {est_10x_n:.2f}s")
    else:
        print("Não foi possível estimar (tempo muito baixo).")

if __name__ == "__main__":
    run_stress_test()
