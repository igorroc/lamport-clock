from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Inicializa o relógio vetorial
vector_clock = np.zeros(size, dtype=int)

def send_event(destination, clock):
    clock[rank] += 1
    comm.send(clock, dest=destination)
    print(f'Processo {rank} enviou {clock} para {destination}')

def receive_event(source, clock):
    received_clock = comm.recv(source=source)
    clock = np.maximum(clock, received_clock)
    clock[rank] += 1
    print(f'Processo {rank} recebeu {received_clock} de {source}, relógio atualizado para {clock}')
    return clock

if rank == 0:
    send_event(1, vector_clock)
    vector_clock = receive_event(1, vector_clock)
elif rank == 1:
    vector_clock = receive_event(0, vector_clock)
    send_event(0, vector_clock)