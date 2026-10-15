import csv
import gc
import math
import random
import time
import matplotlib.pyplot as plt
from ordenacao import (
    ordenacao_insercao,
    ordenacao_intercalacao,
    ordenar_sorted_contando,
)

TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 20
SEMENTE = 42
ARQUIVO_CSV = "dados.csv"
GRAFICO_TEMPOS = "grafico_tempos.png"
GRAFICO_COMPARACOES = "grafico_comparacoes.png"


def executar_experimento():
    random.seed(SEMENTE)
    resultados = []

    print(f"Iniciando medições ({REPETICOES} repetições por tamanho)...")

    for n in TAMANHOS:
        tempos_ins = []
        tempos_inter = []
        tempos_sorted = []

        comps_ins = []
        comps_inter = []
        comps_sorted = []

        for _ in range(REPETICOES):
            lista_base = [random.randint(1, 100000) for _ in range(n)]

            # 1. Ordenação por Inserção
            entrada_ins = lista_base.copy()
            gc.disable()
            t0 = time.perf_counter()
            _, c_ins = ordenacao_insercao(entrada_ins)
            t1 = time.perf_counter()
            gc.enable()
            tempos_ins.append((t1 - t0) * 1000.0)  # em milissegundos (ms)
            comps_ins.append(c_ins)

            # 2. Ordenação por Intercalação
            entrada_inter = lista_base.copy()
            gc.disable()
            t0 = time.perf_counter()
            _, c_inter = ordenacao_intercalacao(entrada_inter)
            t1 = time.perf_counter()
            gc.enable()
            tempos_inter.append((t1 - t0) * 1000.0)  # em milissegundos (ms)
            comps_inter.append(c_inter)

            # 3. sorted() nativo - Medição de Tempo (sem overhead de wrapper)
            entrada_sorted = lista_base.copy()
            gc.disable()
            t0 = time.perf_counter()
            _ = sorted(entrada_sorted)
            t1 = time.perf_counter()
            gc.enable()
            tempos_sorted.append((t1 - t0) * 1000.0)  # em milissegundos (ms)

            # 4. sorted() nativo - Contagem de Comparações (Extra)
            _, c_sorted = ordenar_sorted_contando(lista_base)
            comps_sorted.append(c_sorted)

        linha = {
            "n": n,
            "tempo_insercao_ms": sum(tempos_ins) / REPETICOES,
            "tempo_intercalacao_ms": sum(tempos_inter) / REPETICOES,
            "tempo_sorted_ms": sum(tempos_sorted) / REPETICOES,
            "comp_insercao": sum(comps_ins) / REPETICOES,
            "comp_intercalacao": sum(comps_inter) / REPETICOES,
            "comp_sorted": sum(comps_sorted) / REPETICOES,
            "limite_n_log2_n": n * math.log2(n),
        }
        resultados.append(linha)
        print(
            f"n={n:4d} | "
            f"T_Ins={linha['tempo_insercao_ms']:.4f}ms | "
            f"T_Inter={linha['tempo_intercalacao_ms']:.4f}ms | "
            f"T_Sorted={linha['tempo_sorted_ms']:.4f}ms | "
            f"C_Ins={linha['comp_insercao']:.1f} | "
            f"C_Inter={linha['comp_intercalacao']:.1f} | "
            f"C_Sorted={linha['comp_sorted']:.1f}"
        )

    return resultados


def salvar_csv(resultados):
    campos = [
        "n",
        "tempo_insercao_ms",
        "tempo_intercalacao_ms",
        "tempo_sorted_ms",
        "comp_insercao",
        "comp_intercalacao",
        "comp_sorted",
        "limite_n_log2_n",
    ]
    with open(ARQUIVO_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in resultados:
            writer.writerow({
                "n": r["n"],
                "tempo_insercao_ms": f"{r['tempo_insercao_ms']:.6f}",
                "tempo_intercalacao_ms": f"{r['tempo_intercalacao_ms']:.6f}",
                "tempo_sorted_ms": f"{r['tempo_sorted_ms']:.6f}",
                "comp_insercao": f"{r['comp_insercao']:.2f}",
                "comp_intercalacao": f"{r['comp_intercalacao']:.2f}",
                "comp_sorted": f"{r['comp_sorted']:.2f}",
                "limite_n_log2_n": f"{r['limite_n_log2_n']:.2f}",
            })
    print(f"\nArquivo '{ARQUIVO_CSV}' gerado com sucesso.")


def gerar_graficos(resultados):
    ns = [r["n"] for r in resultados]
    t_ins = [r["tempo_insercao_ms"] for r in resultados]
    t_inter = [r["tempo_intercalacao_ms"] for r in resultados]
    t_sort = [r["tempo_sorted_ms"] for r in resultados]

    c_ins = [r["comp_insercao"] for r in resultados]
    c_inter = [r["comp_intercalacao"] for r in resultados]
    c_sort = [r["comp_sorted"] for r in resultados]
    c_nlogn = [r["limite_n_log2_n"] for r in resultados]

    # Índice até n = 100 para o subplot de zoom no ponto de virada
    idx_zoom = [i for i, n in enumerate(ns) if n <= 100]
    ns_z = [ns[i] for i in idx_zoom]

    # --- GRÁFICO 1: TEMPOS ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    ax1.plot(ns, t_ins, "o-", label="Inserção", color="#d62728", linewidth=2)
    ax1.plot(ns, t_inter, "s-", label="Intercalação", color="#1f77b4", linewidth=2)
    ax1.plot(ns, t_sort, "^-", label="sorted() (Python)", color="#2ca02c", linewidth=2)
    ax1.set_title("Tempo de Execução — Escala Completa (n ≤ 1000)")
    ax1.set_xlabel("Tamanho da lista (n)")
    ax1.set_ylabel("Tempo médio (ms)")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    ax2.plot(ns_z, [t_ins[i] for i in idx_zoom], "o-", label="Inserção", color="#d62728", linewidth=2)
    ax2.plot(ns_z, [t_inter[i] for i in idx_zoom], "s-", label="Intercalação", color="#1f77b4", linewidth=2)
    ax2.plot(ns_z, [t_sort[i] for i in idx_zoom], "^-", label="sorted() (Python)", color="#2ca02c", linewidth=2)
    ax2.set_title("Zoom no Ponto de Virada (n ≤ 100)")
    ax2.set_xlabel("Tamanho da lista (n)")
    ax2.set_ylabel("Tempo médio (ms)")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(GRAFICO_TEMPOS, dpi=150)
    plt.close(fig)
    print(f"Gráfico '{GRAFICO_TEMPOS}' gerado com sucesso.")

    # --- GRÁFICO 2: COMPARAÇÕES ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    ax1.plot(ns, c_ins, "o-", label="Inserção", color="#d62728", linewidth=2)
    ax1.plot(ns, c_inter, "s-", label="Intercalação", color="#1f77b4", linewidth=2)
    ax1.plot(ns, c_sort, "^-", label="sorted() (__lt__)", color="#2ca02c", linewidth=2)
    ax1.plot(ns, c_nlogn, "--", label="Limite n log₂(n)", color="#7f7f7f", linewidth=1.8)
    ax1.set_title("Número de Comparações — Escala Completa (n ≤ 1000)")
    ax1.set_xlabel("Tamanho da lista (n)")
    ax1.set_ylabel("Média de comparações")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    ax2.plot(ns_z, [c_ins[i] for i in idx_zoom], "o-", label="Inserção", color="#d62728", linewidth=2)
    ax2.plot(ns_z, [c_inter[i] for i in idx_zoom], "s-", label="Intercalação", color="#1f77b4", linewidth=2)
    ax2.plot(ns_z, [c_sort[i] for i in idx_zoom], "^-", label="sorted() (__lt__)", color="#2ca02c", linewidth=2)
    ax2.plot(ns_z, [c_nlogn[i] for i in idx_zoom], "--", label="Limite n log₂(n)", color="#7f7f7f", linewidth=1.8)
    ax2.set_title("Zoom nas Comparações (n ≤ 100)")
    ax2.set_xlabel("Tamanho da lista (n)")
    ax2.set_ylabel("Média de comparações")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(GRAFICO_COMPARACOES, dpi=150)
    plt.close(fig)
    print(f"Gráfico '{GRAFICO_COMPARACOES}' gerado com sucesso.")


if __name__ == "__main__":
    dados = executar_experimento()
    salvar_csv(dados)
    gerar_graficos(dados)
