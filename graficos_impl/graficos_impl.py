import os
import matplotlib.pyplot as plt
import numpy as np
# ─────────────────────────────────────────────────────────────────
# DADOS EXTRAÍDOS DOS LOGS (Tempo Médio Interno do C em segundos)
# ─────────────────────────────────────────────────────────────────
# Atualizado com dados de 50k a 400k
tamanhos = [50000, 100000, 200000, 300000, 400000]

# SELECTION SORT (Dados do log run_exe_data_selection.log — execução limpa 27/04/2026)
sel_aleatorio = [2.140625, 8.584135, 34.332933, 77.212740, 137.290865]
sel_ordenado  = [2.141827, 8.588942, 34.290865, 77.211538, 137.295673]
sel_reverso   = [2.143029, 8.610577, 34.312500, 77.227163, 137.335337]

# QUICK SORT (Dados do log run_exe_data_quicksort.log)
# O QuickSort é ordens de magnitude mais rápido (O(n log n))
# Nota: 50k ordenado retornou 0.000000s (abaixo da resolução do timer do C)
quick_aleatorio = [0.003606, 0.008413, 0.014423, 0.026442, 0.034856]
quick_ordenado  = [0.000000, 0.003606, 0.009615, 0.010817, 0.015625]
quick_reverso   = [0.001202, 0.002404, 0.007212, 0.012019, 0.016827]

# ─────────────────────────────────────────────────────────────────
# PLOTAGEM DOS GRÁFICOS
# ─────────────────────────────────────────────────────────────────
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 6))
fig.suptitle("Análise de Tempo de Execução: QuickSort vs SelectionSort", fontsize=16, fontweight='bold')

# --- Gráfico 1: Comparação Geral ---
ax1.plot(tamanhos, sel_aleatorio, 'o-',  color='#ef5350', label='Selection (Aleatório)')
ax1.plot(tamanhos, sel_ordenado,  's--', color='#ff7043', label='Selection (Ordenado)')
ax1.plot(tamanhos, sel_reverso,   '^:',  color='#ffa726', label='Selection (Reverso)')
ax1.plot(tamanhos, quick_aleatorio, 'o-',  color='#42a5f5', label='Quick (Aleatório)', linewidth=2)
ax1.plot(tamanhos, quick_ordenado,  's--', color='#66bb6a', label='Quick (Ordenado)',  linewidth=2)
ax1.plot(tamanhos, quick_reverso,   '^:',  color='#ab47bc', label='Quick (Reverso)',   linewidth=2)
ax1.set_title("Visão Geral (Escala Linear)")
ax1.set_xlabel("Tamanho da Entrada (N)")
ax1.set_ylabel("Tempo de Execução (segundos)")
ax1.grid(True, alpha=0.2)
ax1.legend(fontsize=8)

# --- Gráfico 2: Apenas SelectionSort c/ Tendência O(N²) ---
ax2.plot(tamanhos, sel_aleatorio, 'o-',  color='#ef5350', label='Selection (Aleatório)')
ax2.plot(tamanhos, sel_ordenado,  's--', color='#ff7043', label='Selection (Ordenado)')
ax2.plot(tamanhos, sel_reverso,   '^:',  color='#ffa726', label='Selection (Reverso)')

# Curva teórica O(N²) baseada no ponto de 200k (mais estável)
idx_ref = 2
constante_c = sel_aleatorio[idx_ref] / (tamanhos[idx_ref]**2)
curva_teorica_n2 = [constante_c * (n**2) for n in tamanhos]
ax2.plot(tamanhos, curva_teorica_n2, '--', color='white', label='Tendência O(N²)', alpha=0.7)

ax2.set_title("Comportamento Assintótico do SelectionSort")
ax2.set_xlabel("Tamanho da Entrada (N)")
ax2.set_ylabel("Tempo de Execução (segundos)")
ax2.grid(True, alpha=0.2)
ax2.legend(fontsize=8)

# --- Gráfico 3: Apenas QuickSort c/ Tendência O(N log N) ---
ax3.plot(tamanhos, quick_aleatorio, 'o-',  color='#42a5f5', label='Quick (Aleatório)', linewidth=2)
ax3.plot(tamanhos, quick_ordenado,  's--', color='#66bb6a', label='Quick (Ordenado)',  linewidth=2)
ax3.plot(tamanhos, quick_reverso,   '^:',  color='#ab47bc', label='Quick (Reverso)',   linewidth=2)

# Curva teórica O(N log N) ajustada ao ponto 400k aleatório
idx_ref_q = 4
c_nlogn = quick_aleatorio[idx_ref_q] / (tamanhos[idx_ref_q] * np.log(tamanhos[idx_ref_q]))
curva_nlogn = [c_nlogn * n * np.log(n) for n in tamanhos]
ax3.plot(tamanhos, curva_nlogn, '--', color='white', label='Tendência O(N log N)', alpha=0.7)

ax3.set_title("Comportamento Assintótico do QuickSort")
ax3.set_xlabel("Tamanho da Entrada (N)")
ax3.set_ylabel("Tempo de Execução (segundos)")
ax3.grid(True, alpha=0.2)
ax3.legend(fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analise_sort_v3.png'), dpi=150, bbox_inches='tight')
plt.show()