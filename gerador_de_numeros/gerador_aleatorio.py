import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import time

# ─────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────
MINVAL  = 0
MAXVAL  = 1_000_000
BINS    = 100
SEED    = None

TAMANHOS = [50_000, 100_000, 200_000, 300_000, 400_000]  # 4 tamanhos × 3 cenários = 12 arquivos

PASTA_INPUTS   = "inputs"
PASTA_GRAFICOS = "graficos"

# ─────────────────────────────────────────────────────────────────
# CORES
# ─────────────────────────────────────────────────────────────────
DARK_BG = "#0f1117"
AX_BG   = "#1a1d27"
AX_TEXT = "#cccccc"
BLUE    = "#4da6ff"
ORANGE  = "#ff7043"
GREEN   = "#4caf6e"
RED     = "#ef5350"


def estilo_eixo(ax, titulo):
    ax.set_facecolor(AX_BG)
    ax.set_title(titulo, color="white", fontsize=10, pad=8)
    ax.tick_params(colors=AX_TEXT, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333344")
    ax.xaxis.label.set_color(AX_TEXT)
    ax.yaxis.label.set_color(AX_TEXT)


def formata_label(n):
    """5000 → '5k', 100000 → '100k'"""
    return f"{n // 1000}k"


def gerar_e_plotar(numeros, label):
    N = len(numeros)
    print(f"  Gerando gráfico: {label}")

    contagens, bordas = np.histogram(numeros, bins=BINS)
    esperado          = N / BINS
    chi2_stat         = float(np.sum((contagens - esperado) ** 2 / esperado))
    chi2_pvalue       = 1 - stats.chi2.cdf(chi2_stat, df=BINS - 1)

    amostra_size = min(N, 50_000)
    amostra_acf  = numeros[:amostra_size].astype(float)
    mean_a       = amostra_acf.mean()
    norma        = np.sum((amostra_acf - mean_a) ** 2)
    MAX_LAG      = 30
    acf_vals     = [
        float(np.sum((amostra_acf[:-lag] - mean_a) * (amostra_acf[lag:] - mean_a)) / norma)
        if norma > 0 else 0
        for lag in range(1, MAX_LAG + 1)
    ]
    conf_band = 1.96 / np.sqrt(len(amostra_acf))

    fig = plt.figure(figsize=(16, 11), facecolor=DARK_BG)
    fig.suptitle(
        f"Prova de aleatoriedade  —  {N:,} inteiros ({label})",
        fontsize=15, color="white", fontweight="bold", y=0.98,
    )
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    centros = (bordas[:-1] + bordas[1:]) / 2
    largura = (MAXVAL - MINVAL) / BINS * 0.9

    ax1 = fig.add_subplot(gs[0, :2])
    ax1.bar(centros, contagens, width=largura, color=BLUE, alpha=0.55)
    ax1.axhline(esperado, color=ORANGE, linewidth=2, linestyle="--")
    estilo_eixo(ax1, "Histograma — distribuição dos valores")

    ax_m = fig.add_subplot(gs[0, 2])
    ax_m.set_facecolor(AX_BG)
    ax_m.axis("off")
    for i, (lbl, val, cor) in enumerate([
        ("N gerado",   f"{N:,}",              "white"),
        ("Tipo",       label,                  BLUE),
        ("χ²",         f"{chi2_stat:.1f}",     GREEN),
        ("p-value χ²", f"{chi2_pvalue:.4f}",   GREEN if chi2_pvalue > 0.01 else RED),
    ]):
        y = 0.93 - i * 0.10
        ax_m.text(0.02, y, lbl + ":", color=AX_TEXT, fontsize=9, transform=ax_m.transAxes)
        ax_m.text(0.98, y, val, color=cor, fontsize=9,
                  transform=ax_m.transAxes, ha="right", fontweight="bold")

    ax2 = fig.add_subplot(gs[1, 0])
    scatter_n = min(N - 1, 8_000)
    idx = np.sort(np.random.choice(N - 1, scatter_n, replace=False))
    ax2.scatter(numeros[idx], numeros[idx + 1], s=2, alpha=0.25, color=BLUE)
    estilo_eixo(ax2, "Scatter x[i] vs x[i+1]")

    ax3 = fig.add_subplot(gs[1, 1])
    lags = list(range(1, MAX_LAG + 1))
    ax3.bar(lags, acf_vals, color=BLUE)
    ax3.axhline( conf_band, color=GREEN, linestyle="--")
    ax3.axhline(-conf_band, color=GREEN, linestyle="--")
    estilo_eixo(ax3, "Autocorrelação")
    ax3.set_ylim(-1.1, 1.1)

    png_path = os.path.join(PASTA_GRAFICOS, f"resultado_{label}.png")
    plt.savefig(png_path, dpi=100, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────
# LOOP PRINCIPAL
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(PASTA_INPUTS,   exist_ok=True)
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)

    rng = np.random.default_rng(SEED)

    # Gera uma base com o maior tamanho e fatia para os menores
    # Garante que os mesmos números aparecem nos tamanhos menores
    base_max = rng.integers(MINVAL, MAXVAL, size=max(TAMANHOS))

    total = len(TAMANHOS) * 3
    feitos = 0

    print(f"\nGerando {total} arquivos...\n")

    for n in TAMANHOS:
        label_n = formata_label(n)
        base    = base_max[:n]

        datasets = {
            "aleatorio": base,
            "ordenado":  np.sort(base),
            "reverso":   np.sort(base)[::-1],
        }

        for tipo, dados in datasets.items():
            label    = f"{label_n}_{tipo}"
            txt_path = os.path.join(PASTA_INPUTS, f"numeros_{label}.txt")

            np.savetxt(txt_path, dados, fmt="%d")
            gerar_e_plotar(dados, label)

            feitos += 1
            print(f"  [{feitos:02d}/{total}] ✔ numeros_{label}.txt")

    print(f"\nFinalizado! {total} arquivos prontos em ./{PASTA_INPUTS}/")