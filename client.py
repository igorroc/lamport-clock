import rpyc
import time

class VectorClock:
    def __init__(self, size, id):
        self.vc = [0] * size
        self.id = id

    def increment(self):
        self.vc[self.id] += 1

    def update(self, received_vc):
        self.vc = [max(self.vc[i], received_vc[i]) for i in range(len(self.vc))]
        self.vc[self.id] += 1

    def get_clock(self):
        return self.vc.copy()

    def adjust_size(self, new_size):
        if new_size > len(self.vc):
            self.vc.extend([0] * (new_size - len(self.vc)))
        elif new_size < len(self.vc):
            self.vc = self.vc[:new_size]

def send_message(conn, vc, message):
    return conn.root.send_message(vc, message)

if __name__ == "__main__":
    conn = rpyc.connect("localhost", 18861)
    
    process_id = int(input("Enter the process ID (0-based index): "))
    client_count = conn.root.get_client_count()
    
    vc = VectorClock(client_count, process_id)

    while True:
        action = input("Enter 'send' to send a message or 'receive' to receive a message: ")
        
        if action == "send":
            vc.increment()
            message = f"Message from process {process_id}"
            response, server_vc = send_message(conn, vc.get_clock(), message)
            print(response)
            print(f"Updated vector clock after sending: {vc.get_clock()}")
        
        elif action == "receive":
            received_vc = [int(x) for x in input("Enter the received vector clock: ").split()]
            vc.update(received_vc)
            print(f"Updated vector clock after receiving: {vc.get_clock()}")
        
        # Ajusta o tamanho do vetor de relógio se o número de clientes mudar
        new_client_count = conn.root.get_client_count()
        if new_client_count != len(vc.vc):
            vc.adjust_size(new_client_count)
            print(f"Adjusted vector clock size to: {new_client_count}")
        
        time.sleep(1)
