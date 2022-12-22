import time
import numpy as np
import sys
import modules.dictionaries as dicts_
import logging
from modules.logging_helper import set_logging

logger = logging.getLogger('owon_vds6102a')


class Vds6102a:
    def __init__(self, vds=0):
        set_logging(logger)
        self.vds = vds
        logger.info(self.get_IDN())
        self.npoints = self.get_depmem()
        self.timebase = self.get_timebase()
        self.set_default()

    def set_default(self):
        self.set_ch_scale(1, 200)
        self.set_ch_scale(2, 200)
        self.set_timebase('100us')
        self.set_ch_offset(1, 0)
        self.set_ch_offset(2, 0)
        self.set_depmem('1K')
        time.sleep(2)

    def begin_ch(self, channel):
        self._write(f':WAV:BEG CH{channel}')

    def set_ch_scale(self, channel, mV):
        '''should be from dict data'''
        if mV < 1000:
            self._write(f':CH{channel}:SCAL {mV}mV')
        else:
            self._write(f':CH{channel}:SCAL {mV / 1000}V')

        if abs(self.get_ch_scale(channel) - mV / 1000) > 0.01:
            logger.error(f'ch scale setting error {abs(self.get_ch_scale(channel) - mV / 1000)}')
            sys.exit(1)

    def set_timebase(self, timebase):
        self._write(f':HORI:SCAL {timebase}')
        self.timebase = self.get_timebase()

    def set_ch_offset(self, channel, off):
        self._write(f':CH{channel}:OFFSet {off}')

    def set_depmem(self, dep_str):
        self._write(f':ACQ:DEPMEM {dep_str}')
        self.npoints = self.get_depmem()

    def set_ch_coupling(self, channel, coupling='AC'):
        return self._write(f':CH{channel}:COUP {coupling}')

    def get_timebase(self):
        return dicts_.timebase_vals[self._query(':HORI:SCAL?').split()[0]]

    def get_acq_mode(self):
        return self._query(':ACQ:MODE?')

    def get_depmem(self):
        return dicts_.depmem[self._query(':ACQ:DEPMEM?').split()[0]]

    def get_IDN(self):
        return self._query('*IDN?')

    def get_ch_bwlimit(self, channel):
        return self._query(f':CH{channel}:BAND?')

    def get_ch_coupling(self, channel):
        return self._query(f':CH{channel}:COUP?')

    def get_ch_scale(self, channel):
        return dicts_.V_scale[self._query(f':CH{channel}:SCAL?').split()[0]]

    def get_ch_display(self, channel):
        return self._query(f':CH{channel}:DISP?')

    def get_ch_offset(self, channel):
        return float(self._query(f':CH{channel}:OFFS?'))

    def run(self):
        self._write(':RUN')

    def stop(self):
        self._write(':WAV:END')

    def get_timedata(self):
        return np.linspace(0, self._time_len(), self.npoints)

    def _get_ch_buffer(self):
        return None

    def get_ch_data(self, channel):
        t_sleep = self._time_len()
        offset = self.get_ch_offset(channel)
        scale = self.get_ch_scale(channel)
        self._setup_ch_data(channel)
        time.sleep(t_sleep)
        result = self._get_ch_buffer()
        return self._convert_data(result, offset, scale)

    def get_waveform(self, channel):
        return self.get_timedata(), self.get_ch_data(channel)

    def print_lan_info(self):
        logger.info(self._query(':LAN:DEV?'))
        logger.info(self._query(':LAN:PROT?'))
        logger.info(self._query(':LAN:IPAD?'))
        logger.info(self._query(':LAN:GAT?'))
        logger.info(self._write(':LAN:MASK?'))
        logger.info(self._query(':LAN:DNS?'))
        logger.info(self._query(':LAN:MAC?'))

    def set_lan_dhcp(self):
        try:
            self._write(':LAN:PROT DHCP')
            time.sleep(5)
            self.print_lan_info()
        except:
            logger.warning('Device should be connected to a network with DHCP')

    def set_lan_static(self, gateway, ip):
        try:
            self._write(':LAN:PROT STATIC')
            self._write(f':LAN:IPAD {ip}')
            self._write(f':LAN:GAT {gateway}')
            self._write(f':LAN:DNS {gateway}')
            time.sleep(5)
            self.print_lan_info()
        except:
            logger.warning('reconnect with socket impl')

    def _setup_ch_data(self, channel):
        self._write(f':WAV:BEG CH{channel}')
        self._write(f':WAV:RANG 0,{self.npoints}')

    def _time_len(self):
        self.timebase = self.get_timebase()
        return self.npoints * self.timebase

    def _query(self, str_):
        return self.vds.query(str_)

    def _write(self, str_):
        self.vds.write(str_)

    @staticmethod
    def _convert_data(data, offset, scale):
        return (data / 6400 - offset) * scale
