"""
Provide communication between the paradbox cubes. Currently only supporting bluetooth.

Classes:

Blutooth()
WifiComunication()
"""

import bluetooth as bl
import logging
import time

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
    Communicate with bluetooth to a another device. Uses uuid to identify and broadcast\
    a bluetooth service. Also sends predefinded messages to the connected bluetooth service.
    """


    def __repr__(self):
        # Ugly string representation
        pass


    def __str__(self):
        # Nice string representation
        pass


    def connect_to_device(self, uuid):
        """
        Coonects to the device with the uuid. If it doesn't find any service with \
        the matching uuid then it doesn't connect to any bluetooth service.
        """


        service_matches = bl.find_service(uuid = uuid)

        if len(service_matches) != 0:
            first_match = service_matches[0]
            port = first_match["port"]
            name = first_match["name"]
            host = first_match["host"]

            self.socket = bl.BluetoothSocket()
            self.socket.connect((host, port))
            logging.info("Connected to {} on port {}".format(name, port))
        else:
            logging.info("Could not connect to the device")
            self.connect_to_device(uuid)


    def send_message(self, start=True, independent=False, custom=False, message=""):
        """
        Sends a message to the connected service. Can send three different types of messages.\
        start, just sends the message 'start'. independent, just sends the message 'independent'.\
        and custom, sends a custom message to the connected service.

        :param start : boolean flag for sending start
        :param independant : boolean flag for sending independent
        :param custom : boolean flag fro sending a custom message
        :param message : string only used if custom is True

        :raise SyntaxError : If not flags are provided raise syntax error
        """


        if start:
            self.socket.send("start")
        elif independant:
            self.socket.send("independent")
        elif custom and message != "":
            self.scoket.send(message)
        else:
            raise SyntaxError("All flag are set to false. Please set one to True")


    def close_socket(self):
        """
        Close socket connection. Should only be used when you are down with everything
        """


        self.socket.close()


    def close_server(self):
        """
        Close server connection. Should only be used when you are down with everything
        """


        self.server.close()
        self.client_sock.close()


    def start_server(self, name, uuid, port):
        """
        Start server broadcasting. You must wait unil the connection is made to \
        wait for a message. Otherwise an error will be thrown.

        :param name : string name of the server
        :param uuid : string uuid of the bluetooth server
        :param port : int port number. Usually 2
        """


        self.server = bl.BluetoothSocket()
        self.server.bind(("", port))
        self.server.listen(1)
        bl.advertise_service(self.server, name, uuid)
        self.client_sock, address = self.server.accept()
        logging.info("Device Connected with address {}".format(address))


    def wait_for_message(self, callback):
        """
        Wait for message from connected bluetooth service. Should only be used \
        when a server connection has been made.

        :param callback : callable function
        """

        data = ""
        while True:
            data = str(self.client_sock.recv(1024))
            if data != "":
                break
            time.sleep(0.1)
        callback(data)
