"""
Net2Plus network utilities
"""

import socket


class Net2PlusFinder(object):
    """Class to help find Net2Plus modules
    """

    def __init__(self, port=30718, timeout=4, ip="0.0.0.0"):
        self._port = port
        self._timeout = timeout
        self._ip = ip

    def _broadcast(self):
        """Broadcast on udp
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind((self._ip, self._port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # Send twice
            s.sendto(bytearray([0x00, 0x00, 0x00, 0xf6]), ("255.255.255.255", self._port))
            s.sendto(bytearray([0x00, 0x00, 0x00, 0xf6]), ("255.255.255.255", self._port))
        finally:
            s.close()

    def find(self):
        """Find Net2Plus modules responsing to a Broadcast

        Returns an array of dicts with info about each module
        """
        res = []

        # Broadcast
        self._broadcast()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(self._timeout)
            s.bind((self._ip, self._port))

            # Wait for result
            try:
                while True:
                    data, addr = s.recvfrom(1024)
                    if len(data) >= 30:
                        mac_nrs = tuple(ord(i) for i in data[24:30])
                        mac = "%02x:%02x:%02x:%02x:%02x:%02x" % mac_nrs
                        mod_nr = (mac_nrs[3] << 16) + (mac_nrs[4] << 8) + mac_nrs[5]
                        version = "%d.%02d (%d.%02d)" % (ord(data[19]), ord(data[18]), ord(data[21]), ord(data[20]))
                        dev_dict = dict(
                            ip= addr[0],
                            mac=mac,
                            module=mod_nr,
                            version=version)
                        res.append(dev_dict)
            except socket.timeout:
                pass
            
            return res
        finally:
            s.close()
