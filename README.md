# Comparação de Algoritmos de Ordenação: Inserção vs. Intercalação

Repositório contendo a implementação, testes automatizados e benchmark comparativo entre **Ordenação por Inserção (Insertion Sort)**, **Ordenação por Intercalação (Merge Sort)** e o **`sorted()` nativo do Python**.

## Estrutura de Arquivos

- `ordenacao.py`: Implementação dos algoritmos de ordenação e do contador de comparações para o `sorted()`.
- `testes.py`: Testes automatizados (`unittest`) cobrindo casos de borda (lista vazia, 1 elemento, elementos iguais, ordenada, invertida e listas aleatórias).
- `medir.py`: Script que executa os experimentos para $n \in \{5, 10, 20, 30, 50, 75, 100, 200, 500, 1000\}$, gera o arquivo `dados.csv` e plota os gráficos `grafico_tempos.png` e `grafico_comparacoes.png`.
- `dados.csv`: Resultados brutos das medições (médias de tempo e de comparações).
- `RELATORIO.md`: Análise detalhada dos resultados, gráficos e respostas às questões.

## Pré-requisitos

- **Python 3.8+**
- Biblioteca `matplotlib` (para geração dos gráficos)

Para instalar a dependência:

```bash
pip install matplotlib
