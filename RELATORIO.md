# Relatório: Ordenação por Inserção vs. Ordenação por Intercalação

## 1. Tabela de Tempos e de Comparações

Os experimentos foram conduzidos com listas pseudoaleatórias (`random.seed(42)`) para $n \in \{5, 10, 20, 30, 50, 75, 100, 200, 500, 1000\}$, executando **20 repetições** para cada tamanho e extraindo a média aritmética.

| $n$ | Tempo Inserção (ms) | Tempo Intercalação (ms) | Tempo `sorted()` (ms) | Comp. Inserção | Comp. Intercalação | Comp. `sorted()` (`__lt__`) | Limite $n \log_2 n$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| **5** | 0,0014 | 0,0046 | 0,0004 | 6,65 | 6,25 | 6,20 | 11,61 |
| **10** | 0,0032 | 0,0098 | 0,0005 | 27,95 | 21,65 | 20,90 | 33,22 |
| **20** | 0,0094 | 0,0210 | 0,0008 | 108,60 | 62,10 | 61,35 | 86,44 |
| **30** | 0,0199 | 0,0324 | 0,0011 | 240,15 | 110,25 | 109,60 | 147,21 |
| **50** | 0,0521 | 0,0568 | 0,0016 | 653,40 | 220,10 | 219,45 | 282,19 |
| **75** | 0,1164 | 0,0889 | 0,0024 | 1.452,85 | 373,35 | 375,90 | 467,16 |
| **100** | 0,2085 | 0,1223 | 0,0033 | 2.564,20 | 539,15 | 541,80 | 664,39 |
| **200** | 0,8412 | 0,2684 | 0,0069 | 10.138,50 | 1.276,80 | 1.283,95 | 1.528,77 |
| **500** | 5,3120 | 0,7491 | 0,0194 | 62.854,10 | 3.851,60 | 3.864,20 | 4.482,89 |
| **1000** | 21,4850 | 1,6120 | 0,0428 | 250.712,35 | 8.702,45 | 8.719,65 | 9.965,78 |

---

## 2. Gráficos

### Tempo de Execução
![Gráfico de Tempos]
<img width="2100" height="825" alt="grafico_comparacoes" src="https://github.com/user-attachments/assets/c9318320-c75a-46d3-aea5-132c80115f4d" />

### Número de Comparações
![Gráfico de Comparações]
<img width="2100" height="825" alt="grafico_tempos" src="https://github.com/user-attachments/assets/064758ec-f0a7-4fdd-b432-2c7f00fa30d5" />

---

## 3. Ponto de Virada no Tempo de Execução

Na medição de **tempo**, a ordenação por intercalação passa a ser mais rápida que a ordenação por inserção entre **$n = 50$ e $n = 75$** (no conjunto de tamanhos testados, $n = 75$ é o primeiro ponto em que a intercalação vence com folga: `0,0889 ms` contra `0,1164 ms` da inserção, com o cruzamento exato das curvas ocorrendo por volta de **$n \approx 55$**).

---

## 4. O gráfico de comparações e o de tempo dão o mesmo ponto de virada? Por quê?

**Não.** Os pontos de virada são bastante diferentes:
- **Nas comparações:** A intercalação já realiza menos comparações desde **$n = 5$ e $n = 10$** (`21,65` comparações na intercalação contra `27,95` na inserção para $n = 10$).
- **No tempo:** A inserção permanece mais rápida até **$n = 50$**, só perdendo a liderança em **$n = 75$**.

**Explicação:**
O número de comparações mede apenas uma operação lógica isolada, enquanto o tempo de execução reflete o **custo constante por operação (*overhead*)** de cada algoritmo:
1. **Baixo overhead da Inserção:** Opera sobre uma única estrutura contígua com laços simples (`for`/`while`) e trocas de índice locais, sem chamadas recursivas e sem alocar listas intermediárias.
2. **Alto overhead da Intercalação:** Para dividir e intercalar, o algoritmo faz $2n - 1$ chamadas recursivas de função na máquina virtual do Python, fatia listas (`lista[:meio]` e `lista[meio:]`) e aloca novas listas auxiliares (`resultado = []`, `.append()`, `.extend()`) a cada nível da árvore de recursão.

Para $n \le 50$, o tempo gasto gerenciando pilha de chamadas e alocação dinâmica de memória na intercalação custa mais caro para a CPU do que as comparações extras feitas pela inserção. Apenas quando $n$ cresce ($n \ge 55\text{--}75$) o crescimento quadrático $\Theta(n^2)$ da inserção supera o peso das constantes ocultas na complexidade $\Theta(n \log n)$ da intercalação.

---

## 5. Por que a comparação com `sorted()` não serve para decidir entre os dois algoritmos?

Comparar o tempo do `sorted()` diretamente com nossas funções em Python não é um teste justo para escolher entre Inserção e Intercalação por duas razões principais:

1. **Diferença de implementação (C compilado vs. Python interpretado):** Nossas funções `ordenacao_insercao` e `ordenacao_intercalacao` são executadas em bytecode Python interpretado pela CPython VM, onde cada acesso a lista, soma de índice e comparação envolve despacho dinâmico de tipos e manipulação de ponteiros `PyObject`. Já o `sorted()` é escrito diretamente em **C nativo otimizado**, operando sobre o array interno de ponteiros da lista sem o overhead do interpretador a cada passo. Isso faz o `sorted()` ser dezenas de vezes mais rápido em qualquer tamanho, medindo a diferença entre C e Python em vez da diferença algorítmica.
2. **Algoritmo híbrido distinto (Timsort/Powersort):** O `sorted()` não usa inserção pura nem intercalação pura, mas sim uma combinação adaptativa dos dois: aplica *Binary Insertion Sort* para blocos pequenos (*minruns* de 32 a 64 elementos) e *Merge Sort* com detecção de sequências naturais (*runs*) para unir os blocos.

---

## 6. Caso em que a Ordenação por Inserção ainda é a escolha adequada

A ordenação por inserção continua sendo a melhor escolha em três cenários práticos:

1. **Listas muito pequenas ($n \le 50$):** Como comprovado pelos nossos gráficos de tempo, o baixo custo estrutural faz a inserção bater algoritmos de divisão e conquista em vetores curtos (motivo pelo qual algoritmos híbridos como *Timsort* e *Introsort* usam inserção na base da recursão).
2. **Listas quase ordenadas (ou manutenção incremental):** A inserção é **adaptativa**. Se a lista já estiver ordenada ou tiver poucos elementos fora do lugar ($k$ inversões), ela executa em tempo linear **$O(n + k)$** (fazendo apenas $n - 1$ comparações quando ordenada), enquanto o Merge Sort clássico desconhece a ordem prévia e continua fazendo $\Theta(n \log n)$ divisões e cópias.
3. **Restrição estrita de memória ($O(1)$ de memória auxiliar):** A inserção ordena *in-place* sem precisar alocar vetores auxiliares proporcionais a $n$, ao contrário da intercalação padrão que exige $O(n)$ de espaço extra.

---

## 7. Extra (+0,2): Comparações do `sorted()` vs. Limite $n \log_2 n$

Para medir as comparações internas do `sorted()`, implementamos a classe `ElementoComparavel` em `ordenacao.py`, que armazena o valor original e incrementa um contador estático sempre que o método especial `__lt__` (`<`) é chamado.

### Análise dos resultados:
- **Abaixo do limite $n \log_2 n$:** Em todos os tamanhos testados ($n = 5$ a $1000$), o número médio de comparações do `sorted()` ficou **consistentemente abaixo de $n \log_2 n$** (por exemplo, em $n = 1000$, o `sorted()` fez `8.719,65` comparações contra o limite de `9.965,78`). Isso ocorre porque o limite inferior teórico da árvore de decisão para ordenação por comparação é $\lceil \log_2(n!) \rceil \approx n \log_2 n - 1,44n$, e o Timsort aproxima-se muito dessa fronteira ótima ($\approx n \log_2 n - 1,25n$).
- **Comportamento em listas pequenas ($n \le 50$):** Mesmo usando ordenação por inserção internamente para $n < 64$, o `sorted()` fez muito menos comparações que a nossa `ordenacao_insercao` (em $n = 50$, foram `219,45` chamadas de `__lt__` no `sorted()` contra `653,40` na inserção comum). Isso acontece porque o CPython utiliza **Inserção Binária (*Binary Insertion Sort*)**, que emprega busca binária ($O(\log i)$) para localizar a posição de inserção de cada elemento, reduzindo as comparações de $O(n^2)$ para $O(n \log n)$ mesmo em vetores pequenos.

