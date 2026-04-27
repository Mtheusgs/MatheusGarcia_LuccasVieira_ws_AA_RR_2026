# Política de Segurança - Análise de Algoritmos (Selection Sort)

## 🔐 Visão Geral
Este repositório é dedicado ao estudo e análise de desempenho dos algoritmos **Selection Sort** e **Quick Sort**, utilizando grandes intervalos de números, medição de tempo e geração de gráficos comparativos. 

Embora seja um projeto de caráter acadêmico e de testes, levamos a segurança e a integridade do código a sério. Esta política descreve como reportar vulnerabilidades e as práticas recomendadas para executar as análises de forma segura.

## 🚀 Versões Suportadas
As correções de segurança e melhorias de performance são aplicadas prioritariamente na versão principal:

| Versão | Suportado |
| :--- | :--- |
| Main (Latest) | ✅ Sim |
| < 1.0.0 | ❌ Não |

## 🛡️ Escopo de Segurança
Consideramos como vulnerabilidades relevantes para este projeto:
* **Execução Remota de Código (RCE):** Scripts que, ao processar arquivos de entrada, permitam a execução de comandos indevidos no sistema operacional.
* **Negação de Serviço (DoS) Local:** Entradas malformadas que causem consumo excessivo e travamento do sistema além do esperado para a complexidade do algoritmo.
* **Segurança de Dependências:** Vulnerabilidades conhecidas nas bibliotecas utilizadas para plotagem de gráficos (ex: Matplotlib, Pandas, NumPy).
* **Scripts de Automação:** Comandos maliciosos embutidos em arquivos de configuração ou scripts de execução em lote.

**Fora de Escopo:** Erros de lógica no algoritmo de ordenação ou imprecisões menores nos gráficos (devem ser tratados via [Issues](https://github.com/hbgit/SEU_REPOSITORIO/issues)).

## 🧑‍💻 Relatando uma Vulnerabilidade
Se você identificar um problema de segurança, por favor, não o publique em uma Issue aberta. 

Envie um relatório detalhado para os mantenedores:
* **Matheus Garcia Sampaio:** [matheusgarciasam@gmail.com](mailto:matheusgarciasam@gmail.com)


Você receberá um retorno sobre a análise do problema em até **5 dias úteis**.

## 🔄 Processo de Correção
1. **Confirmação:** Validaremos a vulnerabilidade em um ambiente isolado.
2. **Patch:** Desenvolveremos a correção e testaremos o impacto no desempenho das análises.
3. **Release:** Publicaremos a atualização e notificaremos os usuários.

## 🔐 Recomendações de Uso
* **Ambientes Virtuais:** Recomendamos executar as análises dentro de um ambiente virtual (venv ou conda) para isolar as dependências.
* **Dados de Teste:** Tenha cautela ao utilizar arquivos de entrada (`.csv`, `.txt`) de fontes não confiáveis para as plotagens.
* **Atualização:** Mantenha suas bibliotecas de análise de dados sempre atualizadas via `pip install --upgrade`.

---
*Este projeto faz parte de estudos acadêmicos na Universidade Federal de Roraima (UFRR).*
