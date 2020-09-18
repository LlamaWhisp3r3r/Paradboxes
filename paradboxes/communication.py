"""
Module DocString
"""

import bluetooth as bl

class WifiCommunication:
    """
    DocString
    """

    def __init__(self):
        pass

    def __repr__(self):
        # Ugly string representation
        pass

    def __str__(self):
        # Nice string representation
        pass


class Bluetooth:
    """
    DocString
    """

    def __init__(self):
        pass

    def __repr__(self):
        # Ugly string representation
        pass

    def __str__(self):
        # Nice string representation
        pass

    def connect_to_device(self, uuid):
        service_matches = bl.find_service(uuid = uuid)

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        self.socket = bl.BluetoothSocket()
        self.socket.connect((host, port))
        print("Connected to : {}, at {} host".format(name, host))

    def start_cube(self):
        self.socket.send("start")

    def close_socket(self):
        self.socket.close()

    def close_server(self):
        self.server.close()
        self.client_sock.close()

    def start_server(self, name, uuid, port):
        self.server = bl.BluetoothSocket()
        self.server.bind(("", port))
        self.server.listen(1)
        bl.advertise_service(self.server, name, uuid)
        self.client_sock, address = self.server.accept()
        print("Accepted Connected to {}".format(self.client_sock))
        data = self.client_sock.recv(1024)
        print("Received:")
        print(data)


    def wait_for_message(self):
        while True:
            data = self.client_sock.recv(1024)
            if data == "start":
                print("Message is start")
            elif data == "stop":
                print("Going to stop now...")
                break
