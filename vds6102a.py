import pyvisa
import sys


class vds6102a:
    def __init__(self):
        self.vds = self._finder()
        self.vds.timeout = 2000
        print(self.get_IDN())
        self.npoints = 1e3
        self.databytes = self.npoints * 2

    def set_ch_scale(self, chanel, mV):
        self._write(f':CH{chanel}:SCAL {mV}mV')

    def set_timebase(self, timebase):
        self._write(f':HORI:SCAL {timebase}us')

    def get_timebase(self):
        return self._query(':HORI:SCAL?')

    def get_acq_mode(self):
        return self._query(':ACQ:MODE?')

    def get_mem_depth(self):
        return self._query(':ACQ:DEPMEM?')

    def get_IDN(self):
        return self._query('*IDN?')

    def get_ch_bwlimit(self, chanel):
        return self._query(f':CH{chanel}:BAND?')

    def get_ch_coupling(self, chanel):
        return self._query(f':CH{chanel}:COUP?')

    def get_ch_scale(self, chanel):
        return self._query(f':CH{chanel}:SCAL?')

    def get_ch_display(self, chanel):
        return self._query(f':CH{chanel}:DISP?')

    def get_ch_offset(self, chanel):
        return self._query(f':CH{chanel}:OFFS?')

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


if __name__ == '__main__':
    osc = vds6102a()

    print(osc.get_timebase(),
          osc.get_acq_mode(),
          osc.get_ch_scale(1), osc.get_ch_scale(2),
          osc.get_mem_depth(),
          osc.get_ch_bwlimit(1), osc.get_ch_bwlimit(2),
          osc.get_ch_coupling(1), osc.get_ch_coupling(2),
          osc.get_ch_offset(1), osc.get_ch_offset(2))

    osc.set_ch_scale(1, 500)
    osc.set_ch_scale(2, 500)
    osc.set_timebase(200)
    print(osc.get_ch_scale(1), osc.get_ch_scale(2), osc.get_timebase())
