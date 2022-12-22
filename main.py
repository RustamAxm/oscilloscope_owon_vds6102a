import matplotlib.pyplot as plt
import numpy as np


from modules.Vds6102aPyVisaImpl import Vds6102aPyVisaImpl
from modules.Vds6102aSocketImpl import Vds6102aSocketImpl


def demo():
    """
     Vds6102aPyVisaImpl use cases:
     ip = '172.17.xxx.xxx'- if u know ip address
     ip = '' - usb use case
     Vds6102aSocketImpl use case:
     ip = '172.17.xxx.xxx'- if u know ip address
    """
    osc = Vds6102aPyVisaImpl(ip='')
    # osc.set_lan_static(ip='192.168.10.3', gateway='192.168.10.1')
    # or
    # osc.set_lan_dhcp()
    osc.print_lan_info()
    osc.set_default()
    osc.set_ch_coupling(1, coupling='AC')
    osc.set_ch_coupling(2, coupling='AC')
    osc.set_ch_scale(1, 5000)
    osc.set_ch_scale(2, 200)

    print(osc.get_timebase(),
          osc.get_acq_mode(),
          osc.get_ch_scale(1), osc.get_ch_scale(2),
          osc.get_depmem(),
          osc.get_ch_bwlimit(1), osc.get_ch_bwlimit(2),
          osc.get_ch_coupling(1), osc.get_ch_coupling(2),
          osc.get_ch_offset(1), osc.get_ch_offset(2))

    print(osc.get_ch_scale(1),
          osc.get_ch_scale(2),
          osc.get_timebase(),
          osc.get_ch_offset(1),
          osc.get_ch_offset(2))

    big_data1 = []
    big_data2 = []
    big_x = []
    for i in range(4):
        osc.run()
        if i == 0:
            x, big_data1 = osc.get_waveform(1)
            big_x, big_data2 = osc.get_waveform(2)
        else:
            x, data1 = osc.get_waveform(1)
            x, data2 = osc.get_waveform(2)
            big_data1 = np.append(big_data1, data1)
            big_data2 = np.append(big_data2, data2)
            big_x = np.append(big_x, x + big_x[-1])
        osc.stop()

    print(big_x.shape, big_data1.shape)
    plt.figure()
    plt.plot(big_x, big_data1, label='channel 1')
    plt.plot(big_x, big_data2, label='channel 2')
    plt.xlabel('Time(s)')
    plt.ylabel('Voltage(V)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    demo()
