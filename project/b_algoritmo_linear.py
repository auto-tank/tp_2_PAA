def mochila_espaco_linear(pesos, utilidades, capacidade):
    """
    Resolve o Problema da Mochila (0/1) utilizando espaço linear O(L).
    """
    # Inicializa o vetor DP com 0.
    # dp[w] armazenará a utilidade máxima conseguida com capacidade w.
    # O tamanho é capacidade + 1 para incluir o índice 0 até L.
    dp = [0] * (capacidade + 1)
    
    n = len(pesos)
    
    # Itera sobre cada item
    for i in range(n):
        p_i = pesos[i]
        u_i = utilidades[i]
        
        # Atualiza o vetor DP de trás para frente.
        # Isso é crucial para garantir que cada item seja considerado apenas uma vez por capacidade alvo.
        # Se iterássemos para frente, poderíamos usar o item i para calcular dp[w] usando um valor
        # dp[w-p_i] que já contivesse o item i (problema da mochila ilimitada/com repetição).
        for w in range(capacidade, p_i - 1, -1):
            if dp[w - p_i] + u_i > dp[w]:
                dp[w] = dp[w - p_i] + u_i
                
    return dp[capacidade]

if __name__ == "__main__":
    # Teste de Validação
    # Exemplo: 4 itens, Resultado Esperado = 6.
    # Valores hipotéticos que satisfazem o exemplo (se o usuário tiver outros, deve alterar aqui).
    # Cenário Hipotético para validar resultado 6:
    # Item 1: peso 2, valor 2
    # Item 2: peso 3, valor 4
    # Item 3: peso 4, valor 5
    # Item 4: peso 1, valor 1
    # Capacidade L = 5
    # Solução Ótima: Levar Item 1 (p=2, v=2) e Item 2 (p=3, v=4). Total Peso=5 <= 5, Total Valor=6.
    
    test_pesos = [2, 3, 4, 1]
    test_utilidades = [2, 4, 5, 1]
    test_L = 5
    
    print(f"--- Teste de Validação (Espaço Linear) ---")
    print(f"Capacidade (L): {test_L}")
    print(f"Itens (Pesos): {test_pesos}")
    print(f"Itens (Utilidades): {test_utilidades}")
    
    resultado = mochila_espaco_linear(test_pesos, test_utilidades, test_L)
    
    print(f"Resultado Obtido: {resultado}")
    print(f"Resultado Esperado: 6")
    
    assert resultado == 6, f"Erro: Esperado 6, obtido {resultado}"
    print("Teste Passou!")
