"""
SQLServer network utilities
"""

import socket


class SqlServerFinder(object):
    """Class to help find SQLServer instances
    """

    def __init__(self, port=1434, timeout=4, ip="0.0.0.0"):
        self._port = port
        self._timeout = timeout
        self._ip = ip

    def find(self):
        """Find SQLServer instances responsing to a Broadcast

        Returns an array of dicts with info about each instance
        """
        res = []

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(self._timeout)
            s.bind((self._ip, 0))
            self._local_port = s.getsockname()[1]
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(bytearray([0x02]), ("255.255.255.255", self._port))

            # Wait for result
            try:
                while True:
                    data, addr = s.recvfrom(1024)
                    if len(data) > 3:
                        data = data.decode()
                        entry = {}
                        parts = data[3:].split(";")
                        nr_values = int(len(parts) / 2)
                        for i in range(nr_values):
                            key = parts[i * 2].strip()
                            value = parts[1 + i * 2].strip()
                            if (key):
                                entry[key] = value
                        res.append(entry)

            except socket.timeout:
                pass

            return res
        finally:
            s.close()
