import socket
import traceback
import serial
import sys
import random
from crccheck.crc import Crcc16Mcrf4xx
import time
import curses

msg_extra_crc = {'140': '181', '375': '251', '246': '184', '301': '243', '141': '47', '30': '39', '31': '246', '61': '167', '83': '22', '138': '109', '7': '119', '286': '210', '148': '178', '147': '154', '257': '131', '262': '12', '271': '22', '263': '133', '259': '92', '260': '146', '276': '18', '275': '126', '112': '174', '336': '245', '334': '72', '5': '217', '6': '104', '247': '81', '77': '143', '80': '14', '75': '158', '76': '152', '395': '0', '146': '103', '411': '106', '67': '21', '130': '29', '254': '46', '350': '232', '250': '49', '132': '85', '225': '208', '131': '223', '290': '251', '291': '10', '230': '163', '410': '160', '245': '130', '162': '189', '110': '84', '264': '49', '144': '127', '373': '117', '285': '137', '283': '74', '284': '99', '280': '70', '282': '123', '288': '20', '287': '1', '281': '48', '33': '104', '63': '119', '101': '102', '124': '87', '128': '226', '49': '39', '123': '250', '232': '151', '24': '24', '233': '35', '127': '25', '25': '23', '105': '93', '234': '150', '235': '179', '93': '47', '91': '63', '113': '124', '114': '237', '92': '54', '107': '108', '90': '183', '115': '4', '242': '104', '12920': '20', '335': '225', '149': '200', '8': '117', '32': '185', '64': '191', '89': '231', '268': '14', '266': '193', '267': '35', '120': '134', '118': '56', '121': '237', '119': '116', '122': '203', '117': '128', '192': '36', '69': '243', '81': '106', '249': '204', '244': '95', '47': '153', '45': '232', '44': '221', '42': '28', '39': '254', '73': '38', '46': '11', '40': '230', '51': '196', '43': '132', '37': '212', '41': '28', '38': '9', '265': '26', '251': '170', '252': '44', '62': '183', '330': '23', '331': '91', '390': '156', '12902': '49', '12900': '114', '12901': '254', '12915': '62', '12905': '49', '12903': '249', '12904': '203', '100': '175', '106': '138', '360': '11', '19': '137', '324': '132', '321': '88', '320': '243', '323': '78', '322': '243', '50': '78', '21': '159', '20': '214', '23': '168', '22': '220', '4': '237', '258': '187', '400': '110', '87': '150', '85': '140', '125': '203', '109': '185', '27': '144', '28': '67', '339': '199', '65': '118', '70': '124', '35': '244', '34': '237', '66': '148', '412': '33', '142': '72', '413': '77', '55': '3', '54': '15', '26': '170', '116': '76', '129': '46', '29': '115', '137': '195', '143': '131', '126': '220', '36': '222', '256': '71', '139': '168', '82': '49', '48': '41', '243': '85', '11': '89', '86': '5', '84': '143', '108': '32', '370': '75', '253': '83', '261': '179', '401': '183', '2': '137', '1': '124', '135': '203', '134': '229', '136': '1', '133': '6', '111': '34', '380': '232', '333': '231', '332': '236', '385': '147', '311': '95', '310': '28', '340': '99', '248': '8', '74': '20', '241': '90', '104': '56', '269': '109', '270': '59', '102': '158', '103': '208', '9000': '113', '299': '19', '9005': '117', '231': '105', '295': '41', '52': '132', '53': '3', '298': '237', '0': '50', '300': '217', '17000': '103'}
msgid_length_min = {'140': '41', '375': '140', '246': '38', '301': '58', '141': '32', '30': '28', '31': '32', '61': '72', '83': '37', '138': '36', '7': '32', '286': '53', '148': '60', '147': '36', '257': '9', '262': '18', '271': '52', '263': '255', '259': '235', '260': '5', '276': '49', '275': '31', '112': '12', '336': '84', '334': '10', '5': '28', '6': '3', '247': '19', '77': '3', '80': '4', '75': '35', '76': '33', '395': '212', '146': '100', '411': '3', '67': '4', '130': '13', '254': '9', '350': '20', '250': '30', '132': '14', '225': '65', '131': '255', '290': '46', '291': '57', '230': '42', '410': '53', '245': '2', '162': '8', '110': '254', '264': '28', '144': '93', '373': '42', '285': '40', '283': '144', '284': '32', '280': '33', '282': '35', '288': '23', '287': '23', '281': '13', '33': '28', '63': '181', '101': '32', '124': '35', '128': '35', '49': '12', '123': '113', '232': '63', '24': '30', '233': '182', '127': '35', '25': '101', '105': '62', '234': '40', '235': '42', '93': '81', '91': '42', '113': '36', '114': '44', '92': '33', '107': '64', '90': '56', '115': '64', '242': '52', '12920': '5', '335': '24', '149': '30', '8': '36', '32': '28', '64': '225', '89': '28', '268': '4', '266': '255', '267': '255', '120': '97', '118': '14', '121': '2', '119': '12', '122': '2', '117': '6', '192': '44', '69': '11', '81': '22', '249': '36', '244': '6', '47': '3', '45': '2', '44': '4', '42': '2', '39': '37', '73': '37', '46': '2', '40': '4', '51': '4', '43': '2', '37': '6', '41': '4', '38': '6', '265': '16', '251': '18', '252': '18', '62': '26', '330': '158', '331': '230', '390': '238', '12902': '53', '12900': '44', '12901': '59', '12915': '254', '12905': '43', '12903': '46', '12904': '46', '100': '26', '106': '44', '360': '25', '19': '24', '324': '146', '321': '2', '320': '20', '323': '147', '322': '149', '50': '37', '21': '2', '20': '20', '23': '23', '22': '25', '4': '14', '258': '32', '400': '254', '87': '51', '85': '51', '125': '6', '109': '9', '27': '26', '28': '16', '339': '5', '65': '42', '70': '18', '35': '22', '34': '22', '66': '6', '412': '6', '142': '243', '413': '7', '55': '25', '54': '27', '26': '22', '116': '22', '129': '22', '29': '14', '137': '14', '143': '14', '126': '79', '36': '21', '256': '42', '139': '43', '82': '39', '48': '13', '243': '53', '11': '6', '86': '53', '84': '53', '108': '84', '370': '87', '253': '51', '261': '27', '401': '6', '2': '12', '1': '31', '135': '8', '134': '43', '136': '22', '133': '18', '111': '16', '380': '20', '333': '109', '332': '239', '385': '133', '311': '116', '310': '17', '340': '70', '248': '254', '74': '20', '241': '32', '104': '32', '269': '213', '270': '19', '102': '32', '103': '20', '9000': '137', '299': '96', '9005': '34', '231': '40', '295': '20', '52': '7', '53': '5', '298': '37', '0': '9', '300': '22', '17000': '179'}
msgid_length = {'140': '41', '375': '140', '246': '38', '301': '58', '141': '32', '30': '28', '31': '48', '61': '72', '83': '37', '138': '120', '7': '32', '286': '53', '148': '78', '147': '54', '257': '9', '262': '22', '271': '52', '263': '255', '259': '235', '260': '13', '276': '49', '275': '31', '112': '12', '336': '84', '334': '10', '5': '28', '6': '3', '247': '19', '77': '10', '80': '4', '75': '35', '76': '33', '395': '212', '146': '100', '411': '3', '67': '4', '130': '13', '254': '9', '350': '252', '250': '30', '132': '39', '225': '65', '131': '255', '290': '46', '291': '57', '230': '42', '410': '53', '245': '2', '162': '9', '110': '254', '264': '28', '144': '93', '373': '42', '285': '40', '283': '144', '284': '32', '280': '33', '282': '35', '288': '23', '287': '23', '281': '13', '33': '28', '63': '181', '101': '117', '124': '57', '128': '35', '49': '20', '123': '113', '232': '65', '24': '52', '233': '182', '127': '35', '25': '101', '105': '63', '234': '40', '235': '42', '93': '81', '91': '42', '113': '39', '114': '44', '92': '33', '107': '65', '90': '56', '115': '64', '242': '60', '12920': '5', '335': '24', '149': '60', '8': '36', '32': '28', '64': '225', '89': '28', '268': '4', '266': '255', '267': '255', '120': '97', '118': '14', '121': '2', '119': '12', '122': '2', '117': '6', '192': '54', '69': '18', '81': '22', '249': '36', '244': '6', '47': '4', '45': '3', '44': '5', '42': '2', '39': '38', '73': '38', '46': '2', '40': '5', '51': '5', '43': '3', '37': '7', '41': '4', '38': '7', '265': '20', '251': '18', '252': '18', '62': '26', '330': '167', '331': '232', '390': '238', '12902': '53', '12900': '44', '12901': '59', '12915': '254', '12905': '43', '12903': '46', '12904': '46', '100': '34', '106': '44', '360': '25', '19': '24', '324': '146', '321': '2', '320': '20', '323': '147', '322': '149', '50': '37', '21': '2', '20': '20', '23': '23', '22': '25', '4': '14', '258': '232', '400': '254', '87': '51', '85': '51', '125': '6', '109': '9', '27': '29', '28': '16', '339': '5', '65': '42', '70': '38', '35': '22', '34': '22', '66': '6', '412': '6', '142': '243', '413': '7', '55': '25', '54': '27', '26': '24', '116': '24', '129': '24', '29': '16', '137': '16', '143': '16', '126': '79', '36': '37', '256': '42', '139': '43', '82': '51', '48': '21', '243': '61', '11': '6', '86': '53', '84': '53', '108': '84', '370': '109', '253': '54', '261': '60', '401': '6', '2': '12', '1': '31', '135': '8', '134': '43', '136': '22', '133': '18', '111': '16', '380': '20', '333': '109', '332': '239', '385': '133', '311': '116', '310': '17', '340': '70', '248': '254', '74': '20', '241': '32', '104': '116', '269': '213', '270': '19', '102': '117', '103': '57', '9000': '137', '299': '98', '9005': '34', '231': '40', '295': '20', '52': '7', '53': '5', '298': '37', '0': '9', '300': '22', '17000': '179'}

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

def printStatus(count,msgid,speed):
    now = time.gmtime(time.time()-runtime)


    
    stdscr.addstr(0, 0, "--------------------------- [ 4DFUZZER V 0.1 ] ------------------------------")
    stdscr.addstr(1, 0, "  Run Time     : %dh %dm %ds  "%(now.tm_hour, now.tm_min, now.tm_sec))
    stdscr.addstr(2, 0, "  Iterations   : %d [%.1fk]  "%(count, count/1000))
    stdscr.addstr(3, 0, "  Fuzzed msgID : %s  "%(msgid))
    stdscr.addstr(4, 0, "  Speed        : %.2f exec/sec  "%(speed))
    stdscr.addstr(5, 0, "--------------------------------- [ LOG ] -----------------------------------")

    stdscr.refresh()

def random_byte_gen(size):
    return ''. join ([random.choice ('0123456789abcdef') for x in range (2*size)])

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
            exit(0)
        
        elif sys.argv[i] == '-m':
            if sys.argv[i+1] == 'QGC' or sys.argv[i+1] == 'qgc':
                mode = 'QGC'
                if port == 18570:
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

def calculate_length(payload):
    return format(len(payload)//2 ,'02x')

def missionCountGenerator(count, seq):
    magic_val, msgid = format(int(msg_extra_crc['44']), '02x'), 44
    

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
                    
    except Exception as ex:
        print(traceback.format_exc())
        pass

def missionItemGenerator(count, seq, original_count):
    magic_val, min_len, max_len, msgid = format(int(msg_extra_crc['73']), '02x'), int(msgid_length_min['73']), int(msgid_length['73']), 73
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
                    
    except Exception as ex:
        print(traceback.format_exc())
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
    payload = random_byte_gen(len)
    stx = "fd"
    incFLAG = "00"
    cmpFLAG = "00"
    sysID = "ff"
    compID = "00"
    magic = format(int(msg_extra_crc[msgid]),'02x')
    msgid = format(int(msgid),'06x')
    msgid = msgid[-2:]+msgid[-4:-2]+msgid[0:2]
    length = calculate_length(payload)
    seq = format(seq,'02x')
    packet = length+incFLAG+cmpFLAG+seq+sysID+compID+msgid+payload
    crc = Crcc16Mcrf4xx.calc(bytearray.fromhex(packet+magic))
    crc = str(format(crc,'04x'))
    crc = [crc[-2:], crc[0:2]]
    packet += crc[0]+crc[1]
    return bytes.fromhex(stx+packet)

def packetSender(msgid=0):

    global sock,ip,port,stdscr
    count = 0

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()


    try:
        if msgid == 0:
            while True:
                for msgid in msgid_length.keys():
                    for len in range(int(msgid_length_min[msgid]), int(msgid_length[msgid])+1):
                        start = time.time()
                        for seq in range(255): 
                            sock.sendto(packetGenerator(msgid,len,seq),(ip,port))
                            count += 1
                        speed = 255/(time.time() - start)
                        
                        printStatus(count,msgid,speed)

        
        else:
            while True:
                for len in range(int(msgid_length_min[msgid]), int(msgid_length[msgid])+1):
                    start = time.time()
                    for seq in range(255): 
                        sock.sendto(packetGenerator(msgid,len,seq),(ip,port))
                        count += 1
                    speed = 255/(time.time() - start)
                    printStatus(count,msgid,speed)
    
    except Exception as e:
        print('\nTry : {}'.format(count))
        curses.nocbreak()
        curses.endwin()

def packetSenderToSerial(msgid=0):

    global ser
    count = 0

    try:
        if msgid == 0:
            while True:
                for msgid in msgid_length.keys():
                    for len in range(int(msgid_length_min[msgid]), int(msgid_length[msgid])+1):
                        start = time.time()
                        for seq in range(255): 
                            ser.write(packetGenerator(msgid,len,seq))
                            count += 1
                        speed = 255/(time.time() - start)
                        
                        printStatus(count,msgid,speed)
        
        else:
            while True:
                for len in range(int(msgid_length_min[msgid]), int(msgid_length[msgid])+1):
                    start = time.time()
                    for seq in range(255): 
                        ser.write(packetGenerator(msgid,len,seq))
                        count += 1
                    speed = 255/(time.time() - start)
                    printStatus(count,msgid,speed)
    
    except:
        print('\nTry : {}'.format(count))

def udpSocketOpen():
    global ip,port,sock,mode
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind((ip,port))
    print('Socket Target {}:{}'.format(ip, port))
    print('Fuzzing Target : {}\n'.format(mode))

def serialOpen():
    global ser

    ser = serial.Serial(port, baudrate=57600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)

def OnFuzz():
    global serial_flag
    if serial_flag == 0:
        udpSocketOpen()
        select = input('Do You Want Run Mission fuzzing mode? [y/N]')

        if select == '' or select == 'N' or select =='n':
            select = input('Do You Want msgID FIX mode? [y/N]')

            if select == '' or select == 'N' or select =='n':
                packetSender()
            
            elif select == 'Y' or select == 'y':
                msgid = input('Insert msgID : ')
                if msgid not in msgid_length.keys():
                    print('Invalid msgID')
                    return
                packetSender(msgid)

        elif select == 'Y' or select == 'y':
            missionSender()
            
    
    else:
        serialOpen()
        select = input('Do You Want Run Mission fuzzing mode? [y/N]')

        if select == '' or select == 'N' or select =='n':
            select = input('Do You Want msgID FIX mode? [y/N]')

            if select == '' or select == 'N' or select =='n':
                packetSender()
            
            elif select == 'Y' or select == 'y':
                msgid = input('Insert msgID : ')
                if msgid not in msgid_length.keys():
                    print('Invalid msgID')
                    return
                packetSender(msgid)


if __name__ == '__main__':
    
    global mode, runtime
    runtime = time.time()
    programInfo()
    optionHandler()
    OnFuzz()
