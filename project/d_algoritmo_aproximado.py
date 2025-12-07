def algoritmo_guloso(pesos, utilidades, capacidade):
    """
    Algoritmo Aproximado (Guloso) para o Problema da Mochila 0/1.
    
    Conceito:
    Em vez de tentar todas as combinações (como na PD ou força bruta),
    o algoritmo guloso toma decisões locais ótimas na esperança de encontrar
    um ótimo global.
    
    Critério Guloso: "Densidade de Valor"
    Calculamos a razão (utilidade / peso) para cada item. Isso nos diz
    quanta "alegria" ganhamos por quilo que colocamos na mochila.
    A ideia é priorizar os itens mais "valiosos" em relação ao espaço que ocupam.
    
    Passos:
    1. Calcular densidade d_i = u_i / p_i para todos os itens.
    2. Ordenar os itens da maior densidade para a menor.
    3. Iterar sobre a lista ordenada e colocar o item na mochila se ele couber.
    
    Complexidade: O(n log n) dominada pela ordenação. Muito mais rápido que O(n*L).
    """
    n = len(pesos)
    
    # 1. Preparação dos dados: Calculando a densidade para cada item
    lista_itens = []
    for i in range(n):
        p = pesos[i]
        u = utilidades[i]
        # Densidade = Utilidade / Peso
        # (Proteção contra divisão por zero, assumindo p > 0 pelo enunciado)
        densidade = u / p if p > 0 else 0
        
        lista_itens.append({
            'id': i + 1, # índice original (1-based) para referência
            'p': p,
            'u': u,
            'd': densidade
        })
        
    # 2. Ordenação: Do item com maior densidade para o menor
    # É aqui que a "escolha gulosa" é definida. Queremos os melhores itens primeiro.
    lista_itens.sort(key=lambda x: x['d'], reverse=True)
    
    peso_atual = 0
    valor_total = 0
    itens_escolhidos = []
    
    # 3. Seleção: Encher a mochila seguindo a ordem de prioridade
    for item in lista_itens:
        # Se o item cabe no espaço restante, nós o levamos.
        # No algoritmo guloso 0/1 simples, se não couber, nós o descartamos e passamos para o próximo.
        # (Diferente da Mochila Fracionária, onde poderíamos levar uma parte dele).
        if peso_atual + item['p'] <= capacidade:
            peso_atual += item['p']
            valor_total += item['u']
            itens_escolhidos.append(item['id'])
            
    # Ordena os índices apenas para facilitar a leitura do resultado
    itens_escolhidos.sort()
    
    return valor_total, itens_escolhidos

if __name__ == "__main__":
    # Os valores abaixo foram extraídos diretamente do exemplo apresentado no livro.
    #
    # Descrição do Exemplo:
    # "Seja o seguinte problema da mochila cuja capacidade é 6 e 4 itens:
    #  p1=1, p2=2, p3=4, p4=5 (Pesos)
    #  u1=2, u2=3, u3=3, u4=4 (Utilidades)"
    #
    # Utilizamos este mesmo conjunto para verificar o quão próximo a solução
    # aproximada (gulosa) chega da solução ótima (que sabemos ser 6).
    
    p = [1, 2, 4, 5]
    u = [2, 3, 3, 4]
    L = 6
    
    print("=== Teste: Algoritmo Guloso (Heurística de Densidade) ===")
    print(f"Itens: Pesos={p}, Utilidades={u}, L={L}")
    
    val, itens = algoritmo_guloso(p, u, L)
    
    print(f"Valor Guloso: {val}")
    print(f"Itens Escolhidos: {itens}")
    
    # Sabemos que o ótimo é 6
    otimo = 6
    print(f"Valor Ótimo: {otimo}")
    if otimo > 0:
        print(f"Erro Relativo: {abs(otimo - val) / otimo:.2%}")
    else:
        print("Erro Relativo: N/A")
    print("Nota: O algoritmo guloso não garante o ótimo global, mas é muito rápido.")
