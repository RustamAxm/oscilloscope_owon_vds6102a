import matplotlib.pyplot as plt
from vds6102a import Vds6102a


def demo():
    osc = Vds6102a('172.17.15.115')
    # osc.set_lan_static(ip='192.168.10.3', gateway='192.168.10.1')
    # or
    osc.set_lan_dhcp()

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

    plt.figure()
    plt.plot(x, data1, label='channel 1')
    plt.plot(x, data2, label='channel 2')
    plt.xlabel('Time(s)')
    plt.ylabel('Voltage(V)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    demo()
