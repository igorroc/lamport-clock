from mpi4py import MPI

def send_message(comm, vector_clock, rank, dest, tag):
    vector_clock[rank] += 1
    message = (vector_clock.copy(), f"Message from process {rank}")
    comm.send(message, dest=dest, tag=tag)
    print(f"Process {rank} sent message to process {dest} with clock {vector_clock}")

def receive_message(comm, vector_clock, rank, source, tag):
    message = comm.recv(source=source, tag=tag)
    received_clock, text = message
    print(f"Process {rank} received message from process {source} with clock {received_clock}")
    for i in range(len(vector_clock)):
        vector_clock[i] = max(vector_clock[i], received_clock[i])
    vector_clock[rank] += 1
    print(f"Process {rank} updated clock to {vector_clock}")
