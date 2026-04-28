import os
import subprocess
import logging
import time
import sys

# Configuração do Log
logging.basicConfig(
    level=logging.DEBUG,
    filename='run_exe_data.log',
    filemode='w',
    format='%(process)d-[%(asctime)s]: %(levelname)s -> %(message)s'
)

BINARY_PROGRAM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "Impl_QuickSort", "quickSortOtm.exe")
INPUTS_FILE = os.path.join(os.path.dirname(__file__), "..", "inputs")
TIMES_RUN = 13

def parse_resultado(line):
    """Parseia a linha RESULTADO| de forma robusta, independente da ordem dos campos."""
    comp_val = None
    time_val = None
    for part in line.split('|'):
        if part.startswith("Comparacoes:"):
            comp_val = int(part.split(':')[1])
        elif part.startswith("Tempo:"):
            time_val = float(part.split(':')[1])
    return comp_val, time_val

def run_benchmark():
    if not os.path.exists(INPUTS_FILE):
        logging.error(f"ERRO: Pasta '{INPUTS_FILE}' não encontrada.")
        return

    files = [f for f in os.listdir(INPUTS_FILE) if os.path.isfile(os.path.join(INPUTS_FILE, f))]
    if not files:
        logging.warning("AVISO: Nenhum arquivo encontrado dentro da pasta inputs.")
        return

    for filename in files:
        input_path = os.path.abspath(os.path.join(INPUTS_FILE, filename))
        exe_path   = os.path.abspath(BINARY_PROGRAM)

        logging.debug(f"=== INICIANDO BATERIA: {filename} ===")

        total_comparacoes  = 0
        tempos_internos_c  = []

        start_bateria = time.perf_counter()

        for i in range(1, TIMES_RUN + 1):
            try:
                result = subprocess.run(
                    [exe_path, input_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    check=True
                )

                for line in result.stdout.splitlines():
                    if "RESULTADO|" in line:
                        comp_val, time_val = parse_resultado(line)
                        if comp_val is not None:
                            total_comparacoes += comp_val
                        if time_val is not None:
                            tempos_internos_c.append(time_val)

                logging.debug(f"  > [{filename}] Execução {i}/{TIMES_RUN} finalizada.")

            except subprocess.CalledProcessError as e:
                logging.error(f"  > Erro na execução {i}: {e.stderr}")
            except Exception as e:
                logging.error(f"  > Falha inesperada: {e}")

        end_bateria = time.perf_counter()

        tempo_total_wall = end_bateria - start_bateria
        media_c = sum(tempos_internos_c) / len(tempos_internos_c) if tempos_internos_c else 0

        logging.debug(f"--- RELATÓRIO DA BATERIA: {filename} ---")
        logging.debug(f"Nº de Execuções: {TIMES_RUN}")
        logging.debug(f"Tempo Total (Wall Time): {tempo_total_wall:.6f}s")
        logging.debug(f"Tempo Médio (Wall Time): {tempo_total_wall/TIMES_RUN:.6f}s")
        logging.debug(f"Tempo Médio (Interno do C): {media_c:.6f}s")
        logging.debug(f"Soma de Comparações (Total): {total_comparacoes}")
        logging.debug(f"Média de Comparações/Rodada: {total_comparacoes/TIMES_RUN:.2f}")
        logging.debug("=" * 60)

if __name__ == "__main__":
    logging.debug("SISTEMA INICIALIZADO - Iniciando bateria de testes de algoritmos.")
    run_benchmark()
    logging.debug("SISTEMA FINALIZADO - Todos os testes foram concluídos.")