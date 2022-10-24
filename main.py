import time

import matplotlib.pyplot as plt

from vds6102a import Vds6102a


def demo():
    osc = Vds6102a()

    print(osc.get_timebase(),
          osc.get_acq_mode(),
          osc.get_ch_scale(1), osc.get_ch_scale(2),
          osc.get_depmem(),
          osc.get_ch_bwlimit(1), osc.get_ch_bwlimit(2),
          osc.get_ch_coupling(1), osc.get_ch_coupling(2),
          osc.get_ch_offset(1), osc.get_ch_offset(2))

    osc.set_default()

    print(osc.get_ch_scale(1),
          osc.get_ch_scale(2),
          osc.get_timebase(),
          osc.get_ch_offset(1),
          osc.get_ch_offset(2))

    osc.run()
    x, data1 = osc.get_waveform(1)
    x, data2 = osc.get_waveform(2)
    osc.stop()
    x = osc.get_timedata()

    plt.figure()
    plt.plot(x, data1)
    plt.plot(x, data2)
    plt.xlabel('Time(s)')
    plt.ylabel('Voltage(V)')
    plt.show()


if __name__ == '__main__':
    demo()
