import socket
import xml.etree.ElementTree as ET
import wiringpi
import time

servo1_pin  =  12
servo2_pin  =  13

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode( servo_pin, 2 )
wiringpi.pwmSetMode(0)
wiringpi.pwmSetRange(1024)
wiringpi.pwmSetClock(375)

def ServoMyServo(set_degree, word):
    if word == 'ringo':
        if ( set_degree <= 90 and set_degree >= -90 ):
        	move_deg = int( 81 + 41 / 90 * set_degree )
        	wiringpi.pwmWrite( servo1_pin, move_deg )
        print 'ringo-star'
    elif word == 'mikan':
        if ( set_degree <= 90 and set_degree >= -90 ):
        	move_deg = int( 81 + 41 / 90 * set_degree )
        	wiringpi.pwmWrite( servo2_pin, move_deg )
        print 'mikan no kuni'

def main():
    host = 'localhost'
    port = 10500

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        data = ''
        while 1:
            if '</RECOGOUT>\n.' in data:
                root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find('<RECOGOUT>'):].replace('\n.', ''))
                for whypo in root.findall('./SHYPO/WHYPO'):
                    command = whypo.get('WORD')
                    score = float(whypo.get('CM'))

                    if command == u'リンゴ' and score >= 0.9:
                        ServoMyServo(90, ringo)
                        time.sleep(1)
                        ServoMyServo(0,ringo)
                    elif command == u'蜜柑' and score >= 0.996:
                        ServoMyServo(90, mikan)
                        time.sleep(1)
                        ServoMyServo(0, mikan)
                    elif command == u'ぶどう' and score >= 0.93:
                data = ''
            else:
                data = data + client.recv(1024)
    except KeyboardInterrupt:
        client.close()

if __name__ == "__main__":
    main()
