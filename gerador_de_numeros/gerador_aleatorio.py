"""
Gerador de números inteiros aleatórios — 9 arquivos (1M a 9M)
Salva direto na pasta inputs/ para uso com heapsort.exe

Para cada quantidade N gera:
  - inputs/numeros_NM.txt              (inteiros, um por linha)
  - graficos/resultado_NM.png          (prova visual de aleatoriedade)

Dependências:
  python -m pip install numpy matplotlib scipy
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import time

# ─────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────
MINVAL      = 0
MAXVAL      = 10_000_000   # intervalo dos inteiros gerados
BINS        = 100
SEED        = None         # None = aleatório; inteiro = reproduzível

QUANTIDADES = [100_000 * i for i in range(1,11)]  # 1M, 2M, ..., 9M

PASTA_INPUTS  = "inputs"
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


def gerar_e_plotar(N, rng):
    label = f"{N // 1_000_000}M"
    print(f"\n{'='*60}")
    print(f"  Processando {N:,} números  ({label})")
    print(f"{'='*60}")

    # ── Geração de inteiros ───────────────────────────────────────
    t0 = time.perf_counter()
    numeros = rng.integers(MINVAL, MAXVAL, size=N)   # inteiros
    print(f"  Geração: {time.perf_counter() - t0:.3f}s")

    # ── Salvar TXT em inputs/ ─────────────────────────────────────
    txt_path = os.path.join(PASTA_INPUTS, f"numeros_{label}.txt")
    t1 = time.perf_counter()
    np.savetxt(txt_path, numeros, fmt="%d")          # formato inteiro
    print(f"  Salvo '{txt_path}': {time.perf_counter() - t1:.3f}s")

    # ── Estatísticas ─────────────────────────────────────────────
    media_obs = numeros.mean()
    media_esp = (MINVAL + MAXVAL) / 2
    std_obs   = numeros.std()
    std_esp   = (MAXVAL - MINVAL) / np.sqrt(12)

    contagens, bordas = np.histogram(numeros, bins=BINS)
    esperado          = N / BINS
    chi2_stat         = float(np.sum((contagens - esperado) ** 2 / esperado))
    chi2_pvalue       = 1 - stats.chi2.cdf(chi2_stat, df=BINS - 1)

    amostra_acf = numeros[:50_000].astype(float)
    mean_a      = amostra_acf.mean()
    norma       = np.sum((amostra_acf - mean_a) ** 2)
    MAX_LAG     = 30
    acf_vals    = [
        float(np.sum((amostra_acf[:-lag] - mean_a) * (amostra_acf[lag:] - mean_a)) / norma)
        for lag in range(1, MAX_LAG + 1)
    ]
    conf_band = 1.96 / np.sqrt(len(amostra_acf))

    print(f"  Média obs={media_obs:.1f} esp={media_esp:.1f} | "
          f"χ²={chi2_stat:.1f} p={chi2_pvalue:.4f} | "
          f"ACF_max={max(abs(v) for v in acf_vals):.5f}")

    # ── Figura ───────────────────────────────────────────────────
    fig = plt.figure(figsize=(16, 11), facecolor=DARK_BG)
    fig.suptitle(
        f"Prova de aleatoriedade  —  {N:,} inteiros  ({MINVAL}–{MAXVAL})",
        fontsize=15, color="white", fontweight="bold", y=0.98,
    )
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    centros = (bordas[:-1] + bordas[1:]) / 2
    largura = (MAXVAL - MINVAL) / BINS * 0.9

    # 1. Histograma + KDE
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.bar(centros, contagens, width=largura, color=BLUE, alpha=0.55,
            label="Frequência observada")
    ax1.axhline(esperado, color=ORANGE, linewidth=2, linestyle="--",
                label=f"Esperado uniforme ({esperado:,.0f})")
    ax1.fill_between([MINVAL, MAXVAL], esperado * 0.97, esperado * 1.03,
                     color=ORANGE, alpha=0.12, label="±3% tolerância")
    kde_x      = np.linspace(MINVAL, MAXVAL, 500)
    kde_y      = stats.gaussian_kde(numeros[::100].astype(float))(kde_x)
    kde_scaled = kde_y * N * (MAXVAL - MINVAL) / BINS
    ax1.plot(kde_x, kde_scaled, color=GREEN, linewidth=2, label="KDE suavizada")
    estilo_eixo(ax1, "Histograma — distribuição dos valores")
    ax1.set_xlabel("Valor")
    ax1.set_ylabel("Frequência")
    ax1.legend(fontsize=8, facecolor=AX_BG, edgecolor="#444", labelcolor="white")

    # 2. Métricas
    ax_m = fig.add_subplot(gs[0, 2])
    ax_m.set_facecolor(AX_BG)
    ax_m.axis("off")
    ax_m.set_title("Métricas", color="white", fontsize=10, pad=8)
    metricas = [
        ("N gerado",      f"{N:,}",                                       "white"),
        ("Média obs.",    f"{media_obs:.1f}",                              GREEN),
        ("Média esp.",    f"{media_esp:.1f}",                              AX_TEXT),
        ("Desvio obs.",   f"{std_obs:.1f}",                                GREEN),
        ("Desvio esp.",   f"{std_esp:.1f}",                                AX_TEXT),
        ("χ²",            f"{chi2_stat:.1f}",                              GREEN),
        ("p-value χ²",    f"{chi2_pvalue:.4f}",                            GREEN if chi2_pvalue > 0.01 else RED),
        ("Max |ACF|",     f"{max(abs(v) for v in acf_vals):.5f}",          GREEN),
        ("Banda ACF 95%", f"±{conf_band:.5f}",                             AX_TEXT),
    ]
    for i, (lbl, val, cor) in enumerate(metricas):
        y = 0.93 - i * 0.10
        ax_m.text(0.02, y, lbl + ":", color=AX_TEXT, fontsize=9, transform=ax_m.transAxes)
        ax_m.text(0.98, y, val, color=cor, fontsize=9,
                  transform=ax_m.transAxes, ha="right", fontweight="bold")

    # 3. Scatter x[i] vs x[i+1]
    ax2 = fig.add_subplot(gs[1, 0])
    idx = np.sort(np.random.choice(N - 1, 8_000, replace=False))
    ax2.scatter(numeros[idx], numeros[idx + 1], s=2, alpha=0.25,
                color=BLUE, rasterized=True)
    estilo_eixo(ax2, "Scatter  x[i] vs x[i+1]\n(independência sequencial)")
    ax2.set_xlabel("x[i]")
    ax2.set_ylabel("x[i+1]")

    # 4. Autocorrelação
    ax3 = fig.add_subplot(gs[1, 1])
    lags      = list(range(1, MAX_LAG + 1))
    cores_acf = [RED if abs(v) > conf_band else BLUE for v in acf_vals]
    ax3.bar(lags, acf_vals, color=cores_acf, width=0.7)
    ax3.axhline( conf_band, color=GREEN, linewidth=1.2, linestyle="--", label="±95% conf.")
    ax3.axhline(-conf_band, color=GREEN, linewidth=1.2, linestyle="--")
    ax3.axhline(0, color="#555", linewidth=0.8)
    estilo_eixo(ax3, "Autocorrelação por lag\n(vermelho = correlação detectada)")
    ax3.set_xlabel("Lag")
    ax3.set_ylabel("ACF")
    ax3.set_ylim(-0.12, 0.12)
    ax3.legend(fontsize=8, facecolor=AX_BG, edgecolor="#444", labelcolor="white")

    # 5. Componentes χ²
    ax4 = fig.add_subplot(gs[1, 2])
    desvios = (contagens - esperado) ** 2 / esperado
    ax4.bar(centros, desvios, width=largura, color=GREEN, alpha=0.7)
    ax4.axhline(desvios.mean(), color=ORANGE, linewidth=1.5, linestyle="--",
                label=f"Média = {desvios.mean():.2f}")
    estilo_eixo(ax4, "Componentes χ² por bin\n(uniformidade bin a bin)")
    ax4.set_xlabel("Bin (valor)")
    ax4.set_ylabel("(obs − esp)² / esp")
    ax4.legend(fontsize=8, facecolor=AX_BG, edgecolor="#444", labelcolor="white")

    # Veredicto
    tudo_ok = (
        abs(media_obs - media_esp) < 0.02 * (MAXVAL - MINVAL)
        and abs(std_obs - std_esp) / std_esp < 0.02
        and max(abs(v) for v in acf_vals) < conf_band * 2
        and chi2_pvalue > 0.001
    )
    cor_verd   = GREEN if tudo_ok else RED
    texto_verd = (
        "✔  DISTRIBUIÇÃO UNIFORME CONFIRMADA  —  nenhuma aglomeração detectada"
        if tudo_ok else
        "⚠  POSSÍVEL AGLOMERAÇÃO DETECTADA  —  revise o gerador"
    )
    fig.text(0.5, 0.005, texto_verd, ha="center", fontsize=11,
             color=cor_verd, fontweight="bold")

    png_path = os.path.join(PASTA_GRAFICOS, f"resultado_{label}.png")
    plt.savefig(png_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Gráfico salvo: {png_path}")

    return tudo_ok


# ─────────────────────────────────────────────────────────────────
# LOOP PRINCIPAL
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Cria as pastas se não existirem
    os.makedirs(PASTA_INPUTS,   exist_ok=True)
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)

    rng = np.random.default_rng(SEED)
    resultados = []

    t_total = time.perf_counter()

    for N in QUANTIDADES:
        ok = gerar_e_plotar(N, rng)
        resultados.append((N, ok))

    print(f"\n{'='*60}")
    print(f"  RESUMO FINAL  (tempo total: {time.perf_counter() - t_total:.1f}s)")
    print(f"{'='*60}")
    for N, ok in resultados:
        status = "✔ uniforme" if ok else "⚠ verificar"
        print(f"  {N // 1_000_000}M  →  {status}")
    print(f"\n  Arquivos de entrada em: ./{PASTA_INPUTS}/")
    print(f"  Gráficos em:            ./{PASTA_GRAFICOS}/")
    print()