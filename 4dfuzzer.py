import hashlib
import socket
import traceback
import serial
import sys
import random
from crccheck.crc import Crcc16Mcrf4xx
import time
import curses

qgc_msgid_list = ['147', '77', '265', '109', '141', '136', '330', '263', '62', '116', '267', '65', '126', '242', '234', '235', '253', '129', '24', '245', '26', '27', '22', '33', '31', '30', '246', '131', '266', '130', '1', '0', '180', '74', '410', '411', '133', '413', '110', '360', '4']
qgc_msgid_crc = {'180': '52', '263': '133', '116': '76', '360': '11', '74': '20', '24': '24', '31': '167', '330': '23', '109': '185', '126': '220', '235': '179', '411': '106', '242': '104', '33': '104', '1': '124', '147': '154', '245': '130', '410': '160', '267': '35', '265': '26', '27': '144', '234': '150', '65': '124', '4': '237', '129': '46', '26': '170', '413': '77', '266': '193', '246': '184', '253': '83', '141': '47', '77': '143', '30': '22', '62': '183', '0': '50', '110': '84', '22': '220', '130': '29', '131': '223', '133': '6', '136': '1'}
qgc_msgid_length_min = {'180': '45', '263': '255', '116': '22', '360': '25', '74': '20', '24': '30', '31': '72', '330': '158', '109': '9', '126': '79', '235': '42', '411': '3', '242': '52', '33': '28', '1': '31', '147': '36', '245': '2', '410': '53', '267': '255', '265': '16', '27': '26', '234': '40', '65': '18', '4': '14', '129': '22', '26': '22', '413': '7', '266': '255', '246': '38', '253': '51', '141': '32', '77': '3', '30': '37', '62': '26', '0': '9', '110': '254', '22': '25', '130': '13', '131': '255', '133': '18', '136': '22'}
qgc_msgid_length_max = {'180': '45', '263': '255', '116': '22', '360': '25', '74': '20', '24': '30', '31': '72', '330': '158', '109': '9', '126': '79', '235': '42', '411': '3', '242': '52', '33': '28', '1': '31', '147': '36', '245': '2', '410': '53', '267': '255', '265': '16', '27': '26', '234': '40', '65': '18', '4': '14', '129': '22', '26': '22', '413': '7', '266': '255', '246': '38', '253': '51', '141': '32', '77': '3', '30': '37', '62': '26', '0': '9', '110': '254', '22': '25', '130': '13', '131': '255','133': '18', '136': '22'}



px4_msgid_list = ['110', '373', '69', '138', '117', '43', '258', '251', '330', '51', '283', '50', '109', '126', '44', '11', '84', '23', '40', '400', '147', '132', '75', '121', '144', '149', '340', '139', '41', '390', '268', '106', '73', '412', '65', '333', '45', '102', '4', '47', '233', '119', '82', '288', '70', '39', '107', '246', '122', '247', '254', '250', '253', '282', '334', '76', '115', '21', '20', '113', '331', '48', '332', '350', '77', '86', '114', '0']
px4_msgid_crc = {'110': '84', '373': '117', '69': '243', '138': '109', '117': '128', '43': '132', '258': '187', '251': '170', '330': '23', '51': '196', '283': '74', '50': '78', '109': '185', '126': '220', '44': '221', '11': '89', '84': '143', '23': '168', '40': '230', '400': '110', '147': '154', '132': '85', '75': '158', '121': '237', '144': '127', '149': '200', '340': '99', '139': '168', '41': '28', '390': '156', '268': '14', '106': '138', '73': '38', '412': '33', '65': '118', '333': '231', '45': '232', '102': '158', '4': '237', '47': '153', '233': '35', '119': '116', '82': '49', '288': '20', '70': '124', '39': '254', '107': '108', '246': '184', '122': '203', '247': '81', '254': '46', '250': '49', '253': '83', '282': '123', '334': '72', '76': '152', '115': '4', '21': '159', '20': '214', '113': '124', '331': '91', '48': '41', '332': '236', '350': '232', '77': '143', '86': '5', '114': '237', '0': '50'}
px4_msgid_length_min = {'110': '254', '373': '42', '69': '11', '138': '36', '117': '6', '43': '2', '258': '32', '251': '18', '330': '158', '51': '4', '283': '144', '50': '37', '109': '9', '126': '79', '44': '4', '11': '6', '84': '53', '23': '23', '40': '4', '400': '254', '147': '36', '132': '14', '75': '35', '121': '2', '144': '93', '149': '30', '340': '70', '139': '43', '41': '4', '390': '238', '268': '4', '106': '44', '73': '37', '412': '6', '65': '42', '333': '109', '45': '2', '102': '32', '4': '14', '47': '3', '233': '182', '119': '12', '82': '39', '288': '23', '70': '18', '39': '37', '107': '64', '246': '38', '122': '2', '247': '19', '254': '9', '250': '30', '253': '51', '282': '35', '334': '10', '76': '33', '115': '64', '21': '2', '20': '20', '113': '36', '331': '230', '48': '13', '332': '239', '350': '20', '77': '3', '86': '53', '114': '44', '0': '9'}
px4_msgid_length_max = {'110': '254', '373': '42', '69': '18', '138': '120', '117': '6', '43': '3', '258': '232', '251': '18', '330': '167', '51': '5', '283': '144', '50': '37', '109': '9', '126': '79', '44': '5', '11': '6', '84': '53', '23': '23', '40': '5', '400': '254', '147': '54', '132': '39', '75': '35', '121': '2', '144': '93', '149': '60', '340': '70', '139': '43', '41': '4', '390': '238', '268': '4', '106': '44', '73': '38', '412': '6', '65': '42', '333': '109', '45': '3', '102': '117', '4': '14', '47': '4', '233': '182', '119': '12', '82': '51', '288': '23', '70': '38', '39': '38', '107': '65', '246': '38', '122': '2', '247': '19', '254': '9', '250': '30', '253': '54', '282': '35', '334': '10', '76': '33', '115': '64', '21': '2', '20': '20', '113': '39', '331': '232', '48': '21', '332': '239', '350': '252', '77': '10', '86': '53', '114': '44', '0': '9'}


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

def printUDPStatus(count,msgid,speed, iteration, min_length, max_length, now_len):
    now = time.gmtime(time.time()-runtime)


    
    stdscr.addstr(0, 0, "--------------------------- [ 4DFUZZER V 0.1 ] ------------------------------")
    stdscr.addstr(1, 0, "  Run Time      : %dh %dm %ds                                                 "%(now.tm_hour, now.tm_min, now.tm_sec))
    stdscr.addstr(2, 0, "  Iterations    : %d [%.1fk]                                                  "%(count, count/1000))
    stdscr.addstr(3, 0, "  Fuzzed msgID  : %s                                                          "%(msgid))
    stdscr.addstr(4, 0, "  Fuzzed length : %s  ( min_length: %s ~ max_length: %s )                    "%(now_len, min_length, max_length))
    stdscr.addstr(5, 0, "  msgID Iterations : %d                                                    "%(iteration))
    stdscr.addstr(6, 0, "  Speed         : %.2f exec/sec                                               "%(speed))
    stdscr.addstr(7, 0, "--------------------------------- [ LOG ] -----------------------------------")

    stdscr.refresh()

def printStatus(count,msgid,speed):
    now = time.gmtime(time.time()-runtime)


    
    stdscr.addstr(0, 0, "--------------------------- [ 4DFUZZER V 0.1 ] ------------------------------")
    stdscr.addstr(1, 0, "  Run Time     : %dh %dm %ds                                                 "%(now.tm_hour, now.tm_min, now.tm_sec))
    stdscr.addstr(2, 0, "  Iterations   : %d [%.1fk]                                                  "%(count, count/1000))
    stdscr.addstr(3, 0, "  Fuzzed msgID : %s                                                          "%(msgid))
    stdscr.addstr(4, 0, "  Speed        : %.2f exec/sec                                               "%(speed))
    stdscr.addstr(5, 0, "--------------------------------- [ LOG ] -----------------------------------")

    stdscr.refresh()

def random_byte_gen(size):
    return ''. join ([random.choice ('0123456789abcdef') for x in range (2*size)])

def showHelp():
    print('Usage:                [-h, --help] [-m mode] [-i ip] [-p port]')
    print('                                      [-I iteration] [-s port]')
    print('')
    print('Optional arguments:                                           ')
    print(' -h, --help          Show up Options                          ')
    print(' -m mode             Selcet Target PX4,QGC,MAVROS[default PX4]')
    print(' -i ip               Set the Target ip [default 127.0.0.1]    ')
    print(' -p port             Set the Target port [default 18570]      ')
    print(' -s port             Use Serial port                          ')
    print(' -I iteartion per each msgID [default iteration=1]')
    print('')

def optionHandler():
    global mode, ip, port, serial_flag, iteration, msgid_list, msgid_crc, msgid_length_min, msgid_length_max
    mode = 'PX4'
    ip = '127.0.0.1'
    serial_flag = 0
    port = 18570
    iteration = 1
    msgid_list = px4_msgid_list
    msgid_crc = px4_msgid_crc
    msgid_length_min = px4_msgid_length_min
    msgid_length_max = px4_msgid_length_max

    for i in range(len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            showHelp()
            mode = ''
            exit(0)
        
        elif sys.argv[i] == '-m':
            if sys.argv[i+1] == 'QGC' or sys.argv[i+1] == 'qgc':
                mode = 'QGC'
                if port == 18570:
                    port = 14550
                msgid_list = qgc_msgid_list
                msgid_crc = qgc_msgid_crc
                msgid_length_min = qgc_msgid_length_min
                msgid_length_max = qgc_msgid_length_max
            
            elif sys.argv[i+1] == 'MAVROS' or sys.argv[i+1] == 'mavros':
                mode = 'MAVROS'
                msgid_list = px4_msgid_list
                msgid_crc = px4_msgid_crc
                msgid_length_min = px4_msgid_length_min
                msgid_length_max = px4_msgid_length_max
            

        elif sys.argv[i] == '-i':
            ip = sys.argv[i+1]

        elif sys.argv[i] == '-p':
            port = int(sys.argv[i+1])
        
        elif sys.argv[i] == '-s':
            serial_flag = 1
            port = sys.argv[i+1]
        elif sys.argv[i] == '-I':
            iteration = int(sys.argv[i+1])

def calculate_length(payload):
    return format(len(payload)//2 ,'02x')

def missionCountGenerator(count, seq):
    magic_val, msgid = format(int(px4_msgid_crc['44']), '02x'), 44
    

    try:
        header = "fd04000000ffbe2c0000"   
        count = format(count, '04x')
        count = count[-2:] + count[0:2]
        target_system, target_component = "01", "01"
        payload = count + target_system + target_component
        length = calculate_length(payload)
        crc = Crcc16Mcrf4xx.calc(bytes.fromhex(str(header[2:]+ payload + magic_val)))
        crc = format(crc,'04x')
        crc = [crc[-2:], crc[0:2]]

        a = []
        a.append(header)
        a.append(payload)
        a.extend(crc)

        string = ''.join(a)
                   
        string = bytes.fromhex(string)
        return string
                    
    except :
        pass

def missionItemGenerator(count, seq, original_count):
    magic_val, min_len, max_len, msgid = format(int(px4_msgid_crc['73']), '02x'), int(px4_msgid_length_min['73']), int(px4_msgid_length_max['73']), 73
    try:
        stx = "fd"
        incFLAG = "00"
        cmpFLAG = "00"
        msgID = str(format(msgid,'06x'))
        msgID = [msgID[-2:], msgID[-4:-2], msgID[0:2]]
        msgID = "".join(msgID)
        sysID = format(0xff, '02x')	# going to change it in the future
        compID = format(0xbe, '02x')	# going to change it in the future
        newSeq = format(seq, '02x')
            
        param = random_byte_gen(28)
        target_system, target_component, frame, current, autocontinue = "01", "01", "03", "01", "01"
        if count == 0:
            command = format(22, '04x')
        elif count == original_count - 1:
            command = format(20, '04x')
            frame = "02"
        else:
            command = format(16, '04x')
        command = command[-2:] + command[0:2]
        count = format(count, '04x')
        count = count[-2:] + count[0:2]
        
        mission_type = ""
        payload = param + count + command + target_system + target_component + frame + current + autocontinue + mission_type

        length = calculate_length(payload)
        crc = Crcc16Mcrf4xx.calc(bytes.fromhex(str(length + incFLAG + cmpFLAG + newSeq + sysID + compID + msgID  + payload + magic_val)))
        crc = format(crc,'04x')
        crc = [crc[-2:], crc[0:2]]
        tmp = []
        tmp.extend([stx, length, incFLAG, cmpFLAG, newSeq])
        tmp.extend([sysID, compID, msgID, payload])
        tmp.extend(crc)
                    
        final_packet = ''.join(tmp)   
                     
        final_packet = bytes.fromhex(final_packet)
        return final_packet
                    
    except :
        pass

def missionSender():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    iteration = 0
    try:
        while True:
            seq = 0 

            for count in range(10, 0xffff):
                start = time.time()
                sock.sendto(missionCountGenerator(count, seq),(ip,port))
                iteration += 1
                time.sleep(0.5)
                speed = (time.time() - start)
                printStatus(iteration,'44',speed)
                seq = seq + 1
                if seq < 255:
                    seq += 1
                else:
                    seq = 0
                for j in range(count):
                    start = time.time()
                    sock.sendto(missionItemGenerator(j, seq, count),(ip,port))
                    iteration += 1
                    time.sleep(0.1)
                    speed = (time.time() - start)
                    printStatus(iteration,'73',speed)
                    seq = seq + 1
                    if seq < 255:
                        seq += 1
                    else:
                        seq = 0
                time.sleep(0.3)

    except Exception as e:
        print('\nTry : {}'.format(iteration))
        curses.nocbreak()
        curses.endwin()

def packetGenerator(msgid,len,seq):
    global msgid_crc
    payload = random_byte_gen(len)
    stx = "fd"
    incFLAG = "00"
    cmpFLAG = "00"
    compID = str(format(random.randint(0,255),"02x"))
    sysID = str(format(random.randint(0,255),"02x"))
    magic = format(int(msgid_crc[msgid]),'02x')
    msgid = format(int(msgid),'06x')
    msgid = msgid[-2:]+msgid[-4:-2]+msgid[0:2]
    length = calculate_length(payload)
    seq = format(seq,'02x')
    packet = length+incFLAG+cmpFLAG+seq+sysID+compID+msgid+payload
    crc = Crcc16Mcrf4xx.calc(bytearray.fromhex(packet+magic))
    crc = str(format(crc,'04x'))
    crc = [crc[-2:], crc[0:2]]
    packet += crc[0]+crc[1]
    return stx+packet

def save_packet(packet, msgid):
    filename = hashlib.md5(packet.encode('utf-8')).hexdigest()
    f = open("./crash/" + filename + "_msgID" + msgid, 'w')
    f.write(packet)
    f.close()

def packetSender(msgid=0, iteration=1):

    global sock,ip,port,stdscr
    global msgid_length_min, msgid_length_max, msgid_list

    count = 0

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    seq = 0

    try:
        if msgid == 0:
            while True:
                for msgid in msgid_list:
                    for len in range(int(msgid_length_min[msgid]), int(msgid_length_max[msgid])+1):
                        for _ in range(iteration):
                            start = time.time()
                            # for seq in range(255):
                            packet = packetGenerator(msgid,len,seq)
                            sock.sendto(bytes.fromhex(packet),(ip,port))
                            count += 1
                            if seq == 255:
                                seq = 0
                            else:
                                seq +=1
                            

                            data, addr = sock.recvfrom(4096)
                        


                            speed = (time.time() - start)
                            
                            printUDPStatus(count,msgid,speed, _+1, px4_msgid_length_min[msgid], px4_msgid_length_max[msgid] ,str(len))

        
        else:
            while True:
                for len in range(int(msgid_length_min[msgid]), int(msgid_length_max[msgid])+1):
                    for _ in range(iteration):
                        start = time.time()
                        # for seq in range(255):
                        packet = packetGenerator(msgid,len,seq) 
                        sock.sendto(bytes.fromhex(packet),(ip,port))
                        count += 1
                        if seq == 255:
                            seq = 0
                        else:
                            seq +=1

                        data, addr = sock.recvfrom(4096)


                        speed = (time.time() - start)
                        
                        printUDPStatus(count,msgid,speed, _+1, px4_msgid_length_min[msgid], px4_msgid_length_max[msgid] ,str(len))
    
    except socket.timeout:
        save_packet(packet,msgid)
        print('\nTry : {}'.format(count))
        curses.nocbreak()
        curses.endwin()

def packetSenderToSerial(msgid=0, iteration=1):

    global ser,stdscr
    prev_packet_and_msgid = ['0', 'error']
    count = 0
    seq = 0
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        if msgid == 0:
            while True:
                for msgid in msgid_list:
                    for len in range(int(msgid_length_min[msgid]), int(msgid_length_max[msgid])+1):
                        for _ in range(iteration):
                            start = time.time()
                            packet = packetGenerator(msgid,len,seq) 
                            
                            ser.write(bytes.fromhex(packet))
                            count += 1

                            if seq == 255:
                                seq = 0
                            else:
                                seq += 1

                            
                            speed = (time.time() - start)
                            
                            printUDPStatus(count,msgid,speed, _+1, px4_msgid_length_min[msgid], px4_msgid_length_max[msgid] ,str(len))
                            
        else:
            while True:
                for len in range(int(msgid_length_min[msgid]), int(msgid_length_max[msgid])+1):
                    for _ in range(iteration):
                        start = time.time()
                        packet = packetGenerator(msgid, len, seq)
                        ser.write(bytes.fromhex(packet))
                        count += 1

                        if seq == 255:
                            seq = 0
                        else:
                            seq += 1

                        speed = (time.time() - start)   
                        printUDPStatus(count,msgid,speed, _+1, px4_msgid_length_min[msgid], px4_msgid_length_max[msgid] ,str(len))
                        prev_packet_and_msgid = [packet, msgid]
        
    except serial.SerialException:
        save_packet(prev_packet_and_msgid[0], prev_packet_and_msgid[1])
        print('\nTry : {}'.format(count))
        curses.nocbreak()
        curses.endwin()

def udpSocketOpen():
    global ip,port,sock,mode
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    # sock.bind((ip,port))
    print('Socket Target {}:{}'.format(ip, port))
    print('Fuzzing Target : {}\n'.format(mode))

def serialOpen():
    global ser

    ser = serial.Serial(port, baudrate=57600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)

def OnFuzz():
    global serial_flag, iteration
    if serial_flag == 0:
        udpSocketOpen()
        select = input('Do You Want Run Mission fuzzing mode? [y/N]')

        if select == '' or select == 'N' or select =='n':
            select = input('Do You Want msgID FIX mode? [y/N]')


            if select == '' or select == 'N' or select =='n':
                packetSender(iteration=iteration)
            elif select == 'Y' or select == 'y':
                msgid = input('Insert msgID : ')
                if msgid not in px4_msgid_length_max.keys():
                    print('Invalid msgID')
                    return
                packetSender(msgid, iteration=iteration)

        elif select == 'Y' or select == 'y':
            missionSender()
            
    
    else:
        serialOpen()
        select = input('Do You Want Run Mission fuzzing mode? [y/N]')

        if select == '' or select == 'N' or select =='n':
            select = input('Do You Want msgID FIX mode? [y/N]')

            if select == '' or select == 'N' or select =='n':
                packetSenderToSerial(iteration=iteration)
            
            elif select == 'Y' or select == 'y':
                msgid = input('Insert msgID : ')
                if msgid not in px4_msgid_length_max.keys():
                    print('Invalid msgID')
                    return
                packetSenderToSerial(msgid, iteration=iteration)


if __name__ == '__main__':
    
    global mode, runtime
    runtime = time.time()
    programInfo()
    optionHandler()
    OnFuzz()
