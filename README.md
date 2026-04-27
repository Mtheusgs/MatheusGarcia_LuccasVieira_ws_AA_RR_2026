# Análise Experimental: Selection Sort vs. Quick Sort 🚀

Este repositório contém um estudo prático sobre a eficiência de algoritmos de ordenação, comparando uma abordagem de **força bruta** (Selection Sort) com uma de **divisão e conquista** (Quick Sort). O projeto foi desenvolvido como parte das atividades de **Análise de Algoritmos** na Universidade Federal de Roraima (UFRR).

## 📋 Sumário
- [Visão Geral](#-visão-geral)
- [Algoritmos Analisados](#-algoritmos-analisados)
- [Análise de Complexidade](#-análise-de-complexidade)
- [Metodologia de Testes](#-metodologia-de-testes)
- [Configuração do Ambiente](#-configuração-do-ambiente)
- [Resultados Esperados](#-resultados-esperados)
- [Contribuidores](#-contribuidores)

---

## 🔍 Visão Geral
O foco deste projeto é observar o comportamento assintótico dos algoritmos na prática. Através da execução de múltiplos testes com arrays de tamanhos variados, medimos o tempo de resposta e geramos evidências visuais (gráficos) que confirmam as teorias de complexidade computacional.

## 💡 Algoritmos Analisados

### 1. Selection Sort
Funciona selecionando o menor elemento de uma lista e trocando-o com o elemento na primeira posição, repetindo o processo para o restante da lista.
* **Vantagem:** Simplicidade e baixo uso de memória auxiliar.
* **Desvantagem:** Ineficiente para grandes conjuntos de dados.

### 2. Quick Sort
Utiliza a estratégia de dividir para conquistar, escolhendo um "pivô" e particionando o array em sub-arrays de elementos menores e maiores que o pivô.
* **Vantagem:** Extremamente veloz para a maioria dos casos práticos.
* **Desvantagem:** No pior caso (pivô mal escolhido), sua performance cai drasticamente.

---

## 📊 Análise de Complexidade

| Algoritmo | Melhor Caso | Caso Médio | Pior Caso | Memória Auxiliar |
| :--- | :--- | :--- | :--- | :--- |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ |

---

## 🧪 Metodologia de Testes
Para garantir a precisão dos dados:
1.  **Geração de Dados:** São gerados arrays de números inteiros aleatórios utilizando `random.sample` para evitar duplicatas ou `random.randint`.
2.  **Ranges:** Os testes variam de $N=100$ até $N=10.000$ (ou mais, dependendo do hardware).
3.  **Métricas:** O tempo é capturado em segundos com precisão de milissegundos utilizando a biblioteca `time`.
4.  **Repetibilidade:** O processo é repetido para garantir que picos isolados de processamento não distorçam a média.

---

## 🛠️ Configuração do Ambiente

### Pré-requisitos
* Python 3.10 ou superior.
* Pip (gerenciador de pacotes).

### Instalação
1. Clone o repositório:
   ```bash
   git clone [https://github.com/Mtheusgs/MatheusGarcia_LuccasVieira_ws_AA_RR_2026.git](https://github.com/Mtheusgs/MatheusGarcia_LuccasVieira_ws_AA_RR_2026.git)
