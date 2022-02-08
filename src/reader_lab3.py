'''
@file reader_lab3.py

'''
import serial, time
from matplotlib import pyplot as plot

x = []
y = []

with serial.Serial ('COM3', 115200) as s_port:
    
    s_port.write(b'\r\n')
    while True:
        data_line = s_port.readline().strip().decode()
#             print(data_line)
        new_data = data_line.split(',')
        if data_line == 'Stop Transmission':
            break
        try:
            t = (float(new_data[0]))
            pos = (float(new_data[1]))
        except ValueError:
            pass
        except IndexError:
            pass
        else:
            x.append(t)
            y.append(pos)


plot.plot(x,y)
plot.xlabel('Time (ms)')
plot.ylabel('Encoder Ticks')
    
