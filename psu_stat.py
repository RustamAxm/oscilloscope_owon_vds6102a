import time
import requests
from vds6102a import Vds6102a
import numpy as np
import matplotlib.pyplot as plt


def upload_dict(dic, table):
    url = 'http://lava.qat.yadro.com:8086/write?db=owon_db'
    headers = {'Content-Type': 'text/plain'}
    for key, val in dic.items():
        payload = f"{table},channel={str(key).replace(' ', '_')},region=us-west value={round(val, 3)}"
        requests.request("POST", url, headers=headers, data=payload, verify=False)


def voltage_hist():
    osc = Vds6102a('172.17.182.82')

    osc.set_ch_coupling(1, coupling='AC')
    osc.set_ch_coupling(2, coupling='AC')
    osc.set_ch_scale(1, 50)
    osc.set_ch_scale(2, 500)

    for i in range(100):

        osc.run()
        x, data1 = osc.get_waveform(1)
        _, data2 = osc.get_waveform(2)
        osc.stop()

        tmp_dict = {'std_ch1': np.std(data1),
                    'std_ch2': np.std(data2),
                    'mean_ch1': np.mean(data1),
                    'mean_ch2': np.mean(data2),
                    'ptp_ch1': np.ptp(data1),
                    'ptp_ch2': np.ptp(data2)}
        upload_dict(tmp_dict, 'owon_vds')

        with open('psu_std.txt', 'a') as std:
            ch_1 = np.std(data1)
            ch_2 = np.std(data2)
            print('mean', ch_1, ch_2)
            print(ch_1, ch_2, file=std)

        with open('psu_mean.txt', 'a') as mean:
            ch_1 = np.mean(data1)
            ch_2 = np.mean(data2)
            print('mean', ch_1, ch_2)
            print(ch_1, ch_2, file=mean)

        with open('psu_ac_ptp.txt', 'a') as ptp:
            ch_1 = np.ptp(data1)
            ch_2 = np.ptp(data2)
            print('mean', ch_1, ch_2)
            print(ch_1, ch_2, file=ptp)
        time.sleep(10)


def plotter():
    std_ = np.loadtxt('psu_std.txt')
    mean_ = np.loadtxt('psu_mean.txt')
    plt.figure()
    plt.title('data logging vds6102a from 020421006D')
    plt.plot(std_, label=['std ch1', 'std ch2'])
    plt.plot(mean_, label=['mean ch1', 'mean ch2'])
    plt.xlabel('Time[s]')
    plt.ylabel('Voltage(V)')
    plt.legend()
    plt.savefig('test_1.png')
    plt.show()


if __name__ == '__main__':
    # voltage_hist()
    plotter()
