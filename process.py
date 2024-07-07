import numpy as np
from mpi4py import MPI
from colorama import Fore, Style, Back

import utils.printer as printer

class Process:
    def __init__(self, rank, size, debug=False):
        self.rank = rank # Identificador do processo
        self.size = size # Número total de processos
        self.clock = np.zeros(size, dtype=int)
        self.comm = MPI.COMM_WORLD
        self.debug = debug
        self.message_queue = []
        self.current_time = 0

    def increment_clock(self):
        self.clock[self.rank] += 1

    def send_message(self, dest, current_time, delay):
        self.current_time = current_time
        send_time = current_time + delay
        self.comm.send((self.clock.copy(), send_time), dest=dest)
        delay_print = f' com atraso de {delay}t' if delay > 1 else ''
        printer.info(f'{Fore.GREEN}[SEND]{Style.RESET_ALL} (T{current_time}) P{self.rank} enviou {self.clock}{delay_print} para P{dest}')

    def multicast_message(self, current_time):
        if self.debug:
            printer.info(f'P{self.rank} está realizando multicast...')
        send_time = current_time + 1
        self.current_time = current_time
        for dest in range(self.size):
            if dest != self.rank:
                self.comm.send((self.clock.copy(), send_time), dest=dest)
        printer.info(f'{Fore.GREEN}[MULTI]{Style.RESET_ALL} (T{current_time}) P{self.rank} realizou multicast')

    def receive_message(self, current_time):
        status = MPI.Status()
        self.current_time = current_time
        while self.comm.Iprobe(source=MPI.ANY_SOURCE, status=status):
            source = status.Get_source()
            received_clock, received_time = self.comm.recv(source=source)
            if current_time >= received_time:
                if self.check_delay_conditions(source, received_clock):
                    self.clock = np.maximum(self.clock, received_clock)
                    printer.info(f'{Fore.MAGENTA}[RECEIVE]{Style.RESET_ALL} (T{received_time}) P{self.rank} recebeu de P{source} {received_clock}')
                else:
                    reason = 'clock_condition'
                    self.message_queue.append((source, received_clock, received_time, reason))
                    printer.info(f'{Fore.YELLOW}[DELAY]{Style.RESET_ALL} (T{received_time}) P{source} enviou {received_clock}, entrou em espera pois a condição do relógio não foi atendida')
            else:
                reason = 'arrival_time'
                self.message_queue.append((source, received_clock, received_time, reason))
                if self.debug:
                    printer.info(f'{Fore.YELLOW}[DELAY]{Style.RESET_ALL} (T{current_time}) Mensagem de P{source} adicionada em espera, pois seu tempo de chegada é {received_time}t')

    def check_delay_conditions(self, source, received_clock):
        condition_1 = received_clock[source] == self.clock[source] + 1
        condition_2 = all(received_clock[k] <= self.clock[k] for k in range(self.size) if k != source)
        return condition_1 and condition_2

    def process_delayed_messages(self, current_time):
        self.current_time = current_time
        for message in self.message_queue[:]:
            source, received_clock, received_time, reason = message
            if current_time >= received_time and self.check_delay_conditions(source, received_clock):
                self.clock = np.maximum(self.clock, received_clock)
                if reason == 'arrival_time':
                    printer.info(f'{Fore.MAGENTA}[RECEIVE]{Style.RESET_ALL} (T{current_time}) P{self.rank} recebeu de P{source} {received_clock}')
                elif reason == 'clock_condition':
                    printer.info(f'{Fore.MAGENTA}[RECEIVE]{Style.RESET_ALL} (T{current_time}) P{self.rank} processou mensagem atrasada de P{source} {received_clock}, relógio atualizado para {self.clock}')
                self.message_queue.remove(message)

    def synchronize(self, current_time):
        self.current_time = current_time
        self.comm.Barrier()
        self.process_delayed_messages(current_time)

    def start(self):
        printer.config(f'Iniciando {Back.MAGENTA}{Fore.BLACK}( P{self.rank} ){Style.RESET_ALL} {self.clock}')

    def finish(self):
        if self.has_pending_messages():
            printer.error(f'T{self.current_time} Finalizou - VC({self.rank}) {self.clock} com {Fore.RED}mensagens pendentes{Style.RESET_ALL}')
            if self.debug:
                for message in self.message_queue:
                    source, received_clock, received_time, reason = message
                    printer.error(f'(T{received_time}) P{source} enviou {received_clock} para P{self.rank} - {Fore.RED}"{reason}"{Style.RESET_ALL}')
        else:
            printer.success(f'T{self.current_time} Finalizou - VC({self.rank}) {self.clock}')

        print()

    def has_pending_messages(self):
        return len(self.message_queue) > 0
