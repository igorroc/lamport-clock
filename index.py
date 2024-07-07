from mpi4py import MPI

from process import Process
import utils.config as config

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Configurações iniciais
messages_to_send = [
    {"source": 0, "time": 0, "destinations": []},
    {"source": 1, "time": 2, "destinations": []},
    {"source": 2, "time": 4, "destinations": []},
]
# ! Exercício do slide
# messages_to_send = [
#     {"source": 0, "time": 0, "destinations": [{"p": 1, "delay": 1}, {"p": 3, "delay": 6}]},
#     {"source": 1, "time": 2, "destinations": [{"p": 2, "delay": 1}, {"p": 3, "delay": 5}]},
#     {"source": 2, "time": 4, "destinations": [{"p": 3, "delay": 1}]},
# ]

messages_to_send = config.fill_messages_with_time(messages_to_send)

# Sincronização inicial para garantir que todos os processos estejam prontos antes de continuar
comm.Barrier()

# Cria a instância do processo
process = Process(rank, size)
process.start()

global_time = 0

while global_time <= len(messages_to_send):
    for message in messages_to_send:
        if "source" not in message:
            continue
        if rank == message["source"] and message["time"] == global_time:
            process.increment_clock()  # Incrementa o clock do processo apenas uma vez por evento
            current_time = message["time"]
            if not message["destinations"]:  # Se destinations estiver vazio, enviar multicast
                process.multicast_message()
            else:
                for dest in message["destinations"]:
                    delay = dest.get("delay", 0)
                    process.send_message(dest["p"], delay)
    global_time += 1

    process.synchronize(global_time)
    process.receive_message(global_time)

comm.Barrier()
process.process_delayed_messages(global_time)  # Processa todas as mensagens atrasadas antes de finalizar
process.finish()

# Finaliza o MPI
comm.Barrier()
MPI.Finalize()
