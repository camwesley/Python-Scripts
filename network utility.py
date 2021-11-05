import socket
import ssl
from datetime import datetime
import pickle
import subprocess
import platform


class Server():
    def __init__(self, name, port, connection, priority):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()

        self.history = []
        self.alert = False

    def check_connection(self):
        msg = ""
        success = True
        now = datetime.now()

        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False

            elif self.connection == "ssl":
                ssl.wrap_socket(socket.create_connection(self.name, self.port))
                msg = f"{self.name} is up. On {self.port} with {self.connection}"
                success = True
                self.alert = False
            else:
                if self.ping():
                    msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                    success = True
                    self.alert = False
        except socket.timeout:
            msg = f"server {self.name} timeout. on port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"server: {self.name} {e}"
        except Exception as e:
            msg = f"No Clue??: {e}"

        self.create_history(msg, success, now)

    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg, success, now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output(
                "ping -{} 1 {}".format('n' if platform.system().lower() == "MacOSX" else 'c', self.name), shell=True,
                universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
            return False


if __name__ == "__main__":
    servers = [
        Server("reddit.com", 443, 'plain', 'high'),
        Server("msn.com", 443, 'plain', 'high'),
        Server("google.com", 443, 'plain', 'high')

    ]

    for server in servers:
        server.check_connection()
        print(server.history[-1])
