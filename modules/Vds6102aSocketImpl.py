from modules.vds6102a import Vds6102a
import modules.socketscpi_patched as socket
import numpy as np


class Vds6102aSocketImpl(Vds6102a):
    def __init__(self, ip):
        vds = socket.SocketInstrument(ip, port=8866, timeout=2)
        super().__init__(vds=vds)

    def _get_ch_buffer(self):
        data = self.vds.query_binary_values(':WAV:FETC?', debug=False, datatype='b')
        return np.frombuffer(data, dtype=np.int16)
