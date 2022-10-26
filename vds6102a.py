import time
import numpy as np
import pyvisa
import sys
import dictionaries as dicts_


class Vds6102a:
    def __init__(self, ip=''):
        self.ip_ = ip
        self.vds = self._finder()
        self.vds.read_termination = '\n'
        self.vds.write_termination = '\n'

        self.vds.timeout = 2000 #ms
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
        time.sleep(2)

    def begin_ch(self, channel):
        self._write(f':WAV:BEG CH{channel}')

    def set_ch_scale(self, channel, mV):
        if mV < 1000:
            self._write(f':CH{channel}:SCAL {mV}mV')
        else:
            self._write(f':CH{channel}:SCAL {mV / 1000}V')

    def set_timebase(self, timebase):
        self._write(f':HORI:SCAL {timebase}')
        self.timebase = self.get_timebase()

    def set_ch_offset(self, channel, off):
        self._write(f':CH{channel}:OFFSet {off}')

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

    def get_ch_bwlimit(self, channel):
        return self._query(f':CH{channel}:BAND?')

    def get_ch_coupling(self, channel):
        return self._query(f':CH{channel}:COUP?')

    def get_ch_scale(self, channel):
        return dicts_.V_scale[self._query(f':CH{channel}:SCAL?').split()[0]]

    def get_ch_display(self, channel):
        return self._query(f':CH{channel}:DISP?')

    def get_ch_offset(self, channel):
        return self._query(f':CH{channel}:OFFS?')

    def run(self):
        self._write(':RUN')

    def stop(self):
        self._write(':WAV:END')

    def get_timedata(self):
        return np.linspace(0, self._time_len(), self.npoints)

    def get_ch_data(self, channel):
        t_sleep = self._time_len()
        self._write(f':WAV:BEG CH{channel}')
        self._write(':WAV:PRE?')
        self._write(f':WAV:RANG 0,{self.npoints}')
        time.sleep(t_sleep)
        self._write(':WAV:FETC?')
        data = self.vds.read_raw()
        dt = np.dtype([('header', np.int8, 11), ('data', np.int16, self.npoints)])
        result = np.frombuffer(data, dtype=dt)['data'][0]
        return self._convert_data(result, channel)

    def print_lan_info(self):
        print(self._query(':LAN:DEV?'))
        print(self._query(':LAN:PROT?'))
        print(self._query(':LAN:IPAD?'))
        print(self._query(':LAN:GAT?'))
        print(self._write(':LAN:MASK?'))
        print(self._query(':LAN:DNS?'))
        print(self._query(':LAN:MAC?'))

    def set_lan_dhcp(self):
        if self.ip_:
            print('To set LAN settings use USB connection')
        else:
            try:
                self._write(':LAN:PROT DHCP')
                time.sleep(5)
                self.print_lan_info()
            except pyvisa.errors.VisaIOError:
                print('Device should be connected to a network with DHCP')

    def set_lan_static(self, gateway, ip):
        if self.ip_:
            print('To set LAN settings use USB connection')
        else:
            self._write(':LAN:PROT STATIC')
            self._write(f':LAN:IPAD {ip}')
            self._write(f':LAN:GAT {gateway}')
            self._write(f':LAN:DNS {gateway}')
            time.sleep(5)
            self.print_lan_info()

    def get_waveform(self, channel):
        return self.get_timedata(), self.get_ch_data(channel)

    def _time_len(self):
        self.timebase = self.get_timebase()
        return self.npoints * self.timebase

    def _convert_data(self, data, chanel):
        return data / 6400 * self.get_ch_scale(chanel)

    def _query(self, str_):
        return self.vds.query(str_)

    def _write(self, str_):
        self.vds.write(str_)

    def _finder(self):
        rm = pyvisa.ResourceManager('@py')
        list_rm = rm.list_resources('?*')

        if self.ip_:
            try:
                print(f'connecting to IP {self.ip_}')
                return rm.open_resource(f'TCPIP::{self.ip_}::INSTR')
            except:
                print('device not found')
                sys.exit(1)

        if not list_rm:
            print('resource list is empty')
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
