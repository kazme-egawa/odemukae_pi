import socket
import wiringpi

def word(recv_data):
    for line in recv_data.split('\n'):
        index = line.find('WORD="')
        if index!=-1:
            line = line[index+6:line.find('"',index+6)]
            if(line!='<s>' and line!='</s>'):
                print(line)
                if line == 'リンゴ':
                    print("ringo star")
                elif line == '蜜柑':
                    print("mikan no kuni")
                elif line == 'ぶどう':
                    print("budo")
                yield line

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
