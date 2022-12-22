from modules.vds6102a import Vds6102a
import pyvisa
import numpy as np
import sys
import logging

from modules.logging_helper import set_logging

logger = logging.getLogger('owon_pyvisa')


class Vds6102aPyVisaImpl(Vds6102a):
    def __init__(self, ip):
        set_logging(logger)
        vds = self._pyvisa_connection(ip)
        super().__init__(vds=vds)

    def _get_ch_buffer(self):
        self._write(':WAV:FETC?')
        data = self.vds.read_raw()
        dt = np.dtype([('header', np.int8, 11), ('data', np.int16, self.npoints)])
        return np.frombuffer(data, dtype=dt)['data'][0]

    @staticmethod
    def _pyvisa_connection(ip_):
        rm = pyvisa.ResourceManager('@py')

        if ip_:
            try:
                logger.info(f'connecting to IP {ip_}')
                vds = rm.open_resource(f'TCPIP::{ip_}::INSTR')
                vds.read_termination = '\n'
                vds.write_termination = '\n'
                vds.timeout = 2000  # ms
                return vds
            except:
                logger.error('device not found')
                sys.exit(1)

        list_rm = rm.list_resources('?*')
        if not list_rm:
            logger.error('resource list is empty')
            sys.exit(1)

        for instr in list_rm:
            if '4661' in instr:
                logger.info('found device {}'.format(instr))
                try:
                    vds = rm.open_resource(instr)
                    vds.read_termination = '\n'
                    vds.write_termination = '\n'
                    vds.timeout = 2000  # ms
                    return vds
                except ValueError:
                    logger.error('device not found')
                    sys.exit(1)
