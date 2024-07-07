# Para iniciar a execução do programa, execute o comando abaixo no terminal:
# mpiexec -n 4 python index.py
from mpi4py import MPI

from process import Process
import utils.config as config

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# * Configurações iniciais
# ? ------ Exemplo com multicast (3 processos)
# messages = [
#     {"source": 0, "time": 0, "receivers": []},
#     {"source": 1, "time": 2, "receivers": []},
#     {"source": 2, "time": 4, "receivers": []},
# ]
# ? ------ Exemplo sem atraso (3 processos)
messages = [
    {"source": 0, "time": 0, "receivers": [{"p": 1, "delay": 1}, {"p": 2, "delay": 4}]},
    {"source": 1, "time": 2, "receivers": [{"p": 0, "delay": 1}, {"p": 2, "delay": 1}]},
]
# ! Exercício do slide (4 processos) (com atraso)
# messages = [
#     {"source": 0, "time": 0, "receivers": [{"p": 1, "delay": 1}, {"p": 3, "delay": 6}]},
#     {"source": 1, "time": 2, "receivers": [{"p": 2, "delay": 1}, {"p": 3, "delay": 5}]},
#     {"source": 2, "time": 4, "receivers": [{"p": 3, "delay": 1}]},
# ]

messages = config.fill_messages_with_time(messages)

# Sincronização inicial para garantir que todos os processos estejam prontos antes de continuar
comm.Barrier()

# Cria a instância do processo
process = Process(rank, size, debug=False)
process.start()

global_time = 0

while global_time <= len(messages):
    for message in messages:
        if "source" not in message:
            continue
        if rank == message["source"] and message["time"] == global_time:
            process.increment_clock()  # Incrementa o clock do processo apenas uma vez por evento
            current_time = message["time"]
            if not message["receivers"]:  # Se receivers estiver vazio, enviar multicast
                process.multicast_message(current_time)
            else:
                for dest in message["receivers"]:
                    delay = dest.get("delay", 0)
                    process.send_message(dest["p"], current_time, delay)
    
    global_time += 1

    process.synchronize(global_time)
    process.receive_message(global_time)

comm.Barrier()
process.process_delayed_messages(global_time-1)  # Processa todas as mensagens atrasadas antes de finalizar
process.finish()

# Finaliza o MPI
comm.Barrier()
MPI.Finalize()
