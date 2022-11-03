# import socketscpi_patch as socketscpi
import socketscpi
import time

ipAddress = '172.17.14.246'
instrument = socketscpi.SocketInstrument(ipAddress, port=8866, timeout=1)
str_ = instrument.query('*IDN?')

print(str_)
channel = 1
npoints=1000
print(instrument.query(':ACQ:DEPMEM?'))
instrument.write(':RUN')
instrument.write(f':WAV:BEG CH{channel}')
# instrument.write(':WAV:PRE?')
instrument.write(f':WAV:RANG 0,{npoints}')
# instrument.write(':WAV:FETC?')
data = instrument.query_binary_values(':WAV:FETC?', debug=True, datatype='b')
print(data)
data = instrument.query_binary_values(':WAV:FETC?', debug=True, datatype='b')
print(data, len(data))

instrument.write(':WAV:END')
print(float(instrument.query(f':CH{channel}:OFFS?')))

instrument.close()