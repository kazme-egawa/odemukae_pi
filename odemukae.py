import socket
import wiringpi
import time
import sys

servo1_pin  =  12
servo2_pin  =  13

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode( servo1_pin, 2 )
wiringpi.pinMode( servo2_pin, 2 )
wiringpi.pwmSetMode(0)
wiringpi.pwmSetRange(1024)
wiringpi.pwmSetClock(375)

def ServoMyServo(set_degree, word):
    if word == 'ringo':
        if ( set_degree <= 90 and set_degree >= -90 ):
        	move_deg = int( 81 + 41 / 90 * set_degree )
        	wiringpi.pwmWrite( servo1_pin, move_deg )
    elif word == 'mikan':
        if ( set_degree <= 90 and set_degree >= -90 ):
        	move_deg = int( 81 + 41 / 90 * set_degree )
        	wiringpi.pwmWrite( servo2_pin, move_deg )

def word(recv_data):
    for line in recv_data.split('\n'):
        index1 = line.find('WORD="')
        index2 = line.find('CM="')
        if index1!=-1:
            WORD = line[index1+6:line.find('"',index1+6)]
            if index2!=-1:
                CM = float(line[index2+4:line.find('"',index2+4)])
                if(WORD!='<s>' and WORD!='</s>'):
                    if WORD == 'リンゴ' and CM >= 0.9:
                        print("ringo star")
                        ServoMyServo(90, 'ringo')
                        time.sleep(1)
                        ServoMyServo(0, 'ringo')
                    elif WORD == '蜜柑' and CM >= 0.9:
                        print("mikan no kuni")
                        ServoMyServo(90, 'mikan')
                        time.sleep(1)
                        ServoMyServo(0, 'mikan')
                    elif WORD == 'ぶどう' and CM >= 0.9:
                        print("budo")
                    yield WORD

def main():
    host = 'localhost'
    port = 10500

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        data = ''
        while 1:
            if '</RECOGOUT>\n.' in data:
                data = data[data.find('<RECOGOUT>'):].replace('\n.', '')
                print(''.join(word(data)))
                data = ''
            else:
                data = data + client.recv(1024).decode('utf-8')
    except KeyboardInterrupt:
        client.close()

if __name__ == "__main__":
    main()
