# TP II - Problema da Mochila (Knapsack Problem)

*Trabalho desenvolvido para a disciplina de Projeto e Análise de Algoritmos - TP II.*

### Alunos: Italo Henrique Soares dos Santos, Lucas de Souza Bueno, Mariana Aram Silva e Rodrigo Reis do Valle

Este projeto contém a implementação de diversas soluções para o **Problema da Mochila (0/1)**, conforme proposto no trabalho prático baseado no livro de Carvalho (1992).

## Descrição do Problema
O problema consiste em ajudar um escoteiro-mirim a selecionar quais itens levar em sua mochila para um acampamento. Cada item possui um **peso ($p_i$)** e uma **utilidade ($u_i$)**. A mochila possui uma capacidade máxima de carga **$L$**.

O objetivo é maximizar a soma das utilidades dos itens escolhidos sem exceder a capacidade $L$.
$$ \text{Maximizar } \sum u_i \quad \text{sujeito a } \sum p_i \le L $$

## Estrutura do Projeto

Os arquivos estão organizados na pasta `project/`, correspondendo aos itens solicitados:

| Arquivo | Item | Descrição |
| :--- | :---: | :--- |
| `a_prova_np_completo.tex` | **(a)** | Prova formal em LaTeX de que o problema é $\mathcal{NP}$-Completo (redução da Partição). |
| `b_algoritmo_linear.py` | **(b)** | Algoritmo exato com complexidade de espaço linear $O(L)$. Retorna apenas o valor ótimo. |
| `b_teste_limites.py` | **(b)** | Script de teste de carga para identificar o maior problema resolvível em tempo hábil (~30s). |
| `c_prog_dinamica.py` | **(c)** | Solução via Programação Dinâmica Clássica (Matriz $n \times L$) com recuperação dos itens escolhidos. |
| `d_algoritmo_aproximado.py` | **(d)** | Algoritmo Guloso (Aproximado) baseado na densidade de valor ($u_i/p_i$). |
| `g_analise_comparativa.py` | **(g)** | Script que gera instâncias aleatórias, compara os algoritmos e plota gráficos de desempenho. |

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados:

- Python 3.10 ou superior
- [Poetry](https://python-poetry.org/)
- Git

## Como Executar

Este projeto utiliza **Poetry** para gerenciamento de dependências (`numpy`, `matplotlib`).

1.  **Clonar o repositório:**
    ```bash
    git clone https://github.com/auto-tank/tp_2_PAA
    cd tp_2_PAA
    ```

2.  **Verificar Instalação do Poetry:**
    Certifique-se de que o Poetry está instalado e acessível no terminal:
    ```bash
    poetry --version
    ```
    *Se o comando não for reconhecido, instale seguindo as instruções em: https://python-poetry.org/docs/#installation*

3.  **Instalar dependências do projeto:**
    Na raiz do projeto (onde está o arquivo `pyproject.toml`), execute:
    ```bash
    poetry install
    ```
    *Isso criará um ambiente virtual e instalará todas as bibliotecas necessárias.*

4.  **Rodar os scripts (Exemplos):**
    *Para executar os scripts utilizando o ambiente virtual gerenciado pelo Poetry, utilize `poetry run python ...` ou ative o shell com `poetry shell`.*

    *   **Algoritmo Linear (Item b):**
        ```bash
        python project/b_algoritmo_linear.py
        ```
        *Valida com o exemplo do livro (Resultado esperado: 6).*

    *   **Teste de Limites (Item b):**
        ```bash
        python project/b_teste_limites.py
        ```

    *   **Programação Dinâmica Clássica (Item c):**
        ```bash
        python project/c_prog_dinamica.py
        ```
        *Exibe a tabela $UT[M][j]$ formatada conforme o livro.*

    *   **Algoritmo Guloso (Item d):**
        ```bash
        python project/d_algoritmo_aproximado.py
        ```

    *   **Análise Comparativa (Item g):**
        ```bash
        python project/g_analise_comparativa.py
        ```
        *Gera os gráficos `grafico_tempos.png` e `grafico_qualidade.png`.*

## Análise de Complexidade (Item e)

| Algoritmo | Tempo | Espaço | Observação |
| :--- | :--- | :--- | :--- |
| **Linear (Item b)** | $O(n \cdot L)$ | $O(L)$ | Mais eficiente em memória, mas não recupera os itens. |
| **PD Clássica (Item c)** | $O(n \cdot L)$ | $O(n \cdot L)$ | Permite recuperar a solução exata (backtracking). |
| **Guloso (Item d)** | $O(n \log n)$ | $O(n)$ | Muito rápido (domínio da ordenação), mas não garante ótimo global. |

## Qualidade da Aproximação (Item f)
O algoritmo guloso (Item d) utiliza a heurística de **densidade** ($d_i = u_i / p_i$).
*   **Resultados:** Nos testes realizados (`g_analise_comparativa.py`), o algoritmo guloso obteve resultados consistentemente próximos do ótimo (frequentemente acima de 99% em instâncias aleatórias uniformes).
*   **Limitação:** Existem casos extremos onde o guloso falha significativamente (ex: item pequeno de alta densidade impede item grande de enorme valor), mas na prática "média", comporta-se bem.
