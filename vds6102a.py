import time
import numpy as np
import pyvisa
import sys

import dictionaries as dicts_


class Vds6102a:
    def __init__(self):
        self.vds = self._finder()
        self.vds.timeout = 3000 #ms
        self.npoints = self.get_depmem()
        self.timebase = self.get_timebase()
        print(self.get_IDN())
        self.set_default()

    def set_default(self):
        self.set_ch_scale(1, 200)
        self.set_ch_scale(2, 200)
        self.set_timebase('100us')
        self.set_ch_offset(1, 0)
        self.set_ch_offset(2, 0)
        self.set_depmem('1K')
        time.sleep(3)

    def begin_ch(self, chanel):
        self._write(f':WAV:BEG CH{chanel}')

    def set_ch_scale(self, chanel, mV):
        if mV < 1000:
            self._write(f':CH{chanel}:SCAL {mV}mV')
        else:
            self._write(f':CH{chanel}:SCAL {mV/1000}V')

    def set_timebase(self, timebase):
        self._write(f':HORI:SCAL {timebase}')
        self.timebase = self.get_timebase()

    def set_ch_offset(self, ch, off):
        self._write(f':CH{ch}:OFFSet {off}')

    def set_depmem(self, dep_str):
        self._write(f':ACQ:DEPMEM {dep_str}')
        self.npoints = self.get_depmem()

    def get_timebase(self):
        return dicts_.timebase_vals[self._query(':HORI:SCAL?').split()[0]]

    def get_acq_mode(self):
        return self._query(':ACQ:MODE?')

    def get_depmem(self):
        return dicts_.depmem[self._query(':ACQ:DEPMEM?').split()[0]]

    def get_IDN(self):
        return self._query('*IDN?')

    def get_ch_bwlimit(self, chanel):
        return self._query(f':CH{chanel}:BAND?')

    def get_ch_coupling(self, chanel):
        return self._query(f':CH{chanel}:COUP?')

    def get_ch_scale(self, chanel):
        return dicts_.V_scale[self._query(f':CH{chanel}:SCAL?').split()[0]]

    def get_ch_display(self, chanel):
        return self._query(f':CH{chanel}:DISP?')

    def get_ch_offset(self, chanel):
        return self._query(f':CH{chanel}:OFFS?')

    def run(self):
        self._write(':RUN')

    def stop(self):
        self._write(':WAV:END')

    def get_timedata(self):
        return np.linspace(0, self._time_len(), self.npoints)

    def get_ch_data(self, chanel):
        t_sleep = self._time_len()
        self._write(f':WAV:BEG CH{chanel}')
        self._write(':WAV:PRE?')
        self._write(f':WAV:RANG 0,{self.npoints}')
        time.sleep(t_sleep)
        self._write(':WAV:FETC?')

        dt = np.dtype([('header', np.int8, 11), ('data', np.int16, self.npoints)])
        result = np.frombuffer(self.vds.read_raw(), dtype=dt)['data'][0]
        return self._convert_data(result, chanel)

    def _time_len(self):
        self.timebase = self.get_timebase()
        return self.npoints * self.timebase

    def _convert_data(self, data, chanel):
        return data / 6400 * self.get_ch_scale(chanel)

    def _query(self, str_):
        return self.vds.query(str_)

    def _write(self, str_):
        self.vds.write(str_)

    @staticmethod
    def _finder():
        rm = pyvisa.ResourceManager('@py')
        list_rm = rm.list_resources('?*')
        if not list_rm:
            sys.exit(1)
        print(list_rm)

        for instr in list_rm:
            if '4661' in instr:
                print('found device {}'.format(instr))
                try:
                    return rm.open_resource(instr)
                except ValueError:
                    print('device not found')
                    sys.exit(1)
