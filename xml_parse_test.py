import socket
import xml.etree.ElementTree as ET
import wiringpi

def main():
    host = 'localhost'
    port = 10500

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        data = ''
        while 1:
            if '</RECOGOUT>\n.' in data:
                print(data)
                root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find('<RECOGOUT>'):].replace('\n.', ''))
                # for whypo in root.findall('./SHYPO/WHYPO'):
                #     command = whypo.get('WORD')
                #     score = float(whypo.get('CM'))
                #
                #     if command == 'リンゴ' and score >= 0.9:
                #         print("ringo star")
                #     elif command == '蜜柑' and score >= 0.996:
                #         print("mikan no kuni")
                #     elif command == 'ぶどう' and score >= 0.93:
                #         print("budo")
                # data = ''
            else:
                data = data + client.recv(1024).decode('utf-8')
    except KeyboardInterrupt:
        client.close()

if __name__ == "__main__":
    main()
