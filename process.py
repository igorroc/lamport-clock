from mpi4py import MPI
import numpy as np
from colorama import Fore, Style

class Process:
    def __init__(self, rank, size):
        self.rank = rank
        self.size = size
        self.clock = np.zeros(size, dtype=int)
        self.comm = MPI.COMM_WORLD

    # funcao base quando é chamado dentro de um print
    def __str__(self):
        return f'VC({self.rank}) {self.clock}'

    def send_message(self, dest):
        self.clock[self.rank] += 1
        self.comm.send(self.clock.copy(), dest=dest)
        print(f'{Fore.GREEN}Processo {self.rank} enviou {self.clock} para {dest}{Style.RESET_ALL}')

    def multicast_message(self):
        self.clock[self.rank] += 1
        for dest in range(self.size):
            if dest != self.rank:
                self.comm.send(self.clock.copy(), dest=dest)
                print(f'{Fore.GREEN}Processo {self.rank} enviou {self.clock} para {dest}{Style.RESET_ALL}')

    def receive_message(self):
        status = MPI.Status()
        while self.comm.Iprobe(source=MPI.ANY_SOURCE, status=status):
            source = status.Get_source()
            received_clock = self.comm.recv(source=source)
            self.clock = np.maximum(self.clock, received_clock)
            self.clock[self.rank] += 1
            print(f'{Fore.BLUE}Processo {self.rank} recebeu {received_clock} de {source}, relógio atualizado para {self.clock}{Style.RESET_ALL}')

    def synchronize(self):
        self.comm.Barrier()
