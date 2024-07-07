from mpi4py import MPI
from process import Process

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Cria a instância do processo
process = Process(rank, size)

# Sincronização inicial para garantir que todos os processos iniciem juntos
process.synchronize()

if rank == 0:
    process.multicast_message()
    process.synchronize()  # Espera todos os processos enviarem suas mensagens
    process.receive_message()
    process.synchronize()
elif rank == 1:
    process.synchronize()  # Espera todos os processos enviarem suas mensagens
    process.receive_message()
    process.multicast_message()
    process.synchronize()
elif rank == 2:
    process.synchronize()  # Espera todos os processos enviarem suas mensagens
    process.receive_message()
    process.multicast_message()
    process.synchronize()
elif rank == 3:
    process.synchronize()  # Espera todos os processos enviarem suas mensagens
    process.receive_message()
    process.multicast_message()
    process.synchronize()

# Sincronização final para garantir que todos os processos terminem juntos
process.synchronize()

# Imprime o relógio final de cada processo, com o texto "Finalizou - "
print(f'Finalizou - {process}')