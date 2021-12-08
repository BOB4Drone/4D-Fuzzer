import socket
import serial
import sys

def programInfo():
    print('''
   ___ ______  ______  _   _  ______ ______ _____ ______ 
  /   ||  _  \ |  ___|| | | ||___  /|___  /|  ___|| ___ \\
 / /| || | | | | |_   | | | |   / /    / / | |__  | |_/ /
/ /_| || | | | |  _|  | | | |  / /    / /  |  __| |    / 
\___  || |/ /  | |    | |_| |./ /___./ /___| |___ | |\ \ 
    |_/|___/   \_|     \___/ \_____/\_____/\____/ \_| \_|                                                                                                                                                                                                   
''')
    print('Created by team4drone')
    print('Usage: python3.x\n')

def showHelp():
    print('Options:')
    print(' -h, --help          Show up Options')
    print(' -m mode             Selcet Target PX4,QGC,MAVROS[default PX4]')
    print(' -i ip               Set the Target ip [default 127.0.0.1]')
    print(' -p port             Set the Target port [default 18570]')
    print(' -s port             Use Serial port')
    print('')

def optionHandler():
    global mode, ip, port, serial_flag
    mode = 'PX4'
    ip = '127.0.0.1'
    serial_flag = 0
    port = 18570
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            showHelp()
            mode = ''
            break
        
        elif sys.argv[i] == '-m':
            if sys.argv[i+1] == 'QGC' or sys.argv[i+1] == 'qgc':
                mode = 'QGC'
                port = 14550
            
            elif sys.argv[i+1] == 'MAVROS' or sys.argv[i+1] == 'mavros':
                mode = 'MAVROS'

        elif sys.argv[i] == '-i':
            ip = sys.argv[i+1]

        elif sys.argv[i] == '-p':
            port = int(sys.argv[i+1])
        
        elif sys.argv[i] == '-s':
            serial_flag = 1
            port = sys.argv[i+1]

def udpSocketOpen():
    global ip,port,sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip,port))
    print('Socket binded in {}:{}'.format(ip, port))
    

def serialOpen():
    global s

def PX4Fuzz():
    global serial_flag
    if serial_flag == 0:
        udpSocketOpen()
        select = input('Do You Want Run mission fuzzing mode? [y/N]')
        if select == '' or select == 'N' or select =='n':
            print('Do You Want msgID FIX mode? [y/N]')

    else:
        serialOpen()

def QGCFuzz():
    global serial_flag
    if serial_flag == 0:
        udpSocketOpen()
    else:
        print("CAN NOT USE SERIAL")

def ROSFuzz():
    global serial_flag
    if serial_flag == 0:
        udpSocketOpen()
    else:
        print("CAN NOT USE SERIAL")

if __name__ == '__main__':
    global mode
    programInfo()
    optionHandler()

    if mode == 'PX4':
        PX4Fuzz()
    
    elif mode == 'QGC':
        QGCFuzz()
    
    elif mode == 'MAVROS':
        ROSFuzz()
