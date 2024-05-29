import rpyc
from rpyc.utils.server import ThreadedServer

class ClockService(rpyc.Service):
    clients = []

    def on_connect(self, conn):
        ClockService.clients.append(conn)
        print(f"Client connected. Total clients: {len(ClockService.clients)}")

    def on_disconnect(self, conn):
        ClockService.clients.remove(conn)
        print(f"Client disconnected. Total clients: {len(ClockService.clients)}")

    def exposed_get_client_count(self):
        return len(ClockService.clients)

    def exposed_send_message(self, vc, message):
        print(f"Received message: {message}")
        print(f"Received vector clock: {vc}")
        return "Message received", vc

if __name__ == "__main__":
    server = ThreadedServer(ClockService, port=18861)
    print("Server started on port 18861")
    server.start()
