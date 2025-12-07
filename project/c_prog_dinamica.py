def solucao_programacao_dinamica(pesos, utilidades, capacidade):
    """
    Resolve o Problema da Mochila (0/1) utilizando Programação Dinâmica.
    - Linhas: M (Capacidade), de 0 a L.
    - Colunas: j (Itens), de 0 a n.
    
    Recorrência: UT[M][j] = max { UT[M][j-1], u_j + UT[M - p_j][j-1] }
    """
    n = len(pesos)
    L = capacidade
    
    # Matriz UT[M][j]
    # M: Capacidade (0 a L)
    # j: Itens (0 a n)
    UT = [[0 for _ in range(n + 1)] for _ in range(L + 1)]
    
    # --- EXPLICAÇÃO DA TABELA UT ---
    # A tabela UT funciona como uma memória de soluções passadas.
    # UT[M][j] (Linha M, Coluna j) responde à pergunta: 
    # "Qual a MAIOR utilidade que consigo obter se eu tiver uma mochila de capacidade M 
    # e puder escolher itens apenas do conjunto {1, ..., j}?"
    
    # Preenchimento da Tabela
    # Seguindo o livro: "preenchido por colunas (valores crescentes de j), e, dentro das colunas, por linhas (valores crescentes de M)"
    # Isso significa que fixamos um item j e calculamos seu impacto para todas as capacidades M possíveis.
    
    for j in range(1, n + 1): # Itera sobre as colunas (Itens)
        p_j = pesos[j-1]      # Peso do item atual j
        u_j = utilidades[j-1] # Utilidade do item atual j
        
        for M in range(1, L + 1): # Itera sobre as linhas (Capacidades)
            
            # Para cada célula UT[M][j], tomamos a decisão: Item j entra ou não?
            
            # 1. CENÁRIO: Item j NÃO entra.
            # Se ele não entra, a solução ótima é a mesma que já tínhamos encontrado 
            # usando apenas os itens anteriores (1 até j-1) para essa mesma capacidade M.
            # Consultamos a coluna anterior na mesma linha: UT[M][j-1].
            nao_leva = UT[M][j-1]
            
            # 2. CENÁRIO: Item j ENTRA.
            # Para entrar, ele ocupa p_j de capacidade.
            # Sobra então (M - p_j) de capacidade na mochila.
            # A melhor utilidade para esse espaço restante, usando os itens anteriores, 
            # está na linha (M - p_j) da coluna anterior (j-1).
            # Valor = u_j + UT[M - p_j][j-1].
            
            if p_j <= M: # Verifica se o item cabe na capacidade atual M
                utilidade_restante = UT[M - p_j][j-1] # Look-up na tabela (coluna anterior)
                leva = u_j + utilidade_restante
                
                # Princípio da Otimalidade: Escolhemos o maior valor entre levar e não levar
                UT[M][j] = max(nao_leva, leva)
            else:
                # Item j é maior que a capacidade M, não pode ser levado.
                UT[M][j] = nao_leva
                
    valor_otimo = UT[L][n]
    
    # Recuperação da Solução (Backtracking)
    itens_escolhidos = []
    M_atual = L
    
    # Percorremos as colunas de n até 1
    for j in range(n, 0, -1):
        # Comparamos o valor atual com o valor na coluna à esquerda (mesma capacidade)
        # Se for diferente, significa que a inclusão do item j alterou o valor -> Item escolhido.
        if UT[M_atual][j] != UT[M_atual][j-1]:
            itens_escolhidos.append(j)
            M_atual -= pesos[j-1]
            
    itens_escolhidos.reverse()
    
    return valor_otimo, itens_escolhidos, UT

def imprimir_tabela_formatada(UT, n, L):
    print("\nTabela UT (linhas=M, colunas=j):")
    
    # Cabeçalho das colunas (j)
    header = "M \\ j |"
    for j in range(n + 1):
        header += f" {j:2} "
    print(header)
    print("-" * len(header))
    
    # Linhas (M)
    for M in range(L + 1):
        row_str = f" {M:3} |"
        for j in range(n + 1):
            row_str += f" {UT[M][j]:2} "
        print(row_str)
    print("-" * len(header))

if __name__ == "__main__":
    # Os valores abaixo foram extraídos diretamente do exemplo apresentado no 
    # livro, conforme solicitado na especificação do trabalho.
    #
    # Descrição do Exemplo:
    # "Seja o seguinte problema da mochila cuja capacidade é 6 e 4 itens:
    #  p1=1, p2=2, p3=4, p4=5 (Pesos)
    #  u1=2, u2=3, u3=3, u4=4 (Utilidades)"
    #
    # O objetivo é validar se a implementação reproduz o resultado ótimo esperado (6).
    
    p = [1, 2, 4, 5] # Lista de pesos (p_i)
    u = [2, 3, 3, 4] # Lista de utilidades (u_i)
    L = 6            # Capacidade da mochila
    
    print("=== Teste Programação Dinâmica ===")
    
    valor, itens, tabela = solucao_programacao_dinamica(p, u, L)
    
    imprimir_tabela_formatada(tabela, len(p), L)
    
    print(f"\nValor Ótimo Encontrado (UT[{L}][{len(p)}]): {valor}")
    print(f"Itens Selecionados: {itens}")
    
    assert valor == 6
    print("Teste Passou!")
