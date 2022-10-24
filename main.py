import time

import matplotlib.pyplot as plt

from vds6102a import vds6102a


if __name__ == '__main__':
    osc = vds6102a()

    print(osc.get_timebase(),
          osc.get_acq_mode(),
          osc.get_ch_scale(1), osc.get_ch_scale(2),
          osc.get_depmem(),
          osc.get_ch_bwlimit(1), osc.get_ch_bwlimit(2),
          osc.get_ch_coupling(1), osc.get_ch_coupling(2),
          osc.get_ch_offset(1), osc.get_ch_offset(2))

    osc.set_ch_scale(1, 200)
    osc.set_ch_scale(2, 200)
    osc.set_timebase('100us')
    osc.set_ch_offset(1, 0)
    osc.set_ch_offset(2, 0)
    osc.set_depmem('1K')
    time.sleep(3)

    print(osc.get_ch_scale(1), osc.get_ch_scale(2), osc.get_timebase(), osc.get_ch_offset(1), osc.get_ch_offset(2))

    osc.run()
    data1 = osc.get_ch_data(1)
    data2 = osc.get_ch_data(2)
    osc.stop()
    x = osc.get_timedata()
    print("len datas", len(data1), len(data2))

    plt.figure()
    plt.plot(x, data1)
    plt.plot(x, data2)
    plt.xlabel('Time(s)')
    plt.ylabel('Voltage(V)')
    plt.show()