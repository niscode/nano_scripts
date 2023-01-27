# coding: utf-8
# 【latest】 2022-08-26 created by Imura-san

import sys
import socket
import select

from datetime import datetime, timedelta

interval = timedelta(seconds = 60.0)


'''
def readline(soc) :
    data = None
    try :
        data = serversoc.recv(1024).decode()
    except :
        r = False
    return data, r
'''

def readline(soc) :
    readText = ''
    result = True
    while True :
        try :
            data = soc.recv(1)
        except :
            result = False
            break

        if data == b'\n' :
            break
        readText += data.decode()

    return readText, result
    
def loop(serversoc, adr, port, sid):
    lastComm = datetime.now()
    controler = (adr, port)
    while True:
        try :
            rready, _, _ = select.select([serversoc], [], [], 0)
            if not serversoc in rready :
                if datetime.now() > lastComm + interval :
                    line = 'id;%s' % sid
                    soc.send(line.encode('utf-8'))
                    print('send : %s' % line)
                    lastComm = datetime.now()
                    continue
            else :
                data, r = readline(soc)
                lastComm = datetime.now()
                if not r :
                    break
                cmd = str(data.strip())
                if len(cmd) == 0 :
                    continue
                print(cmd)

                try :
                    ctrsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ctrsoc.connect(controler)
                    ctrsoc.send(cmd.encode('utf-8'))
                    ctrsoc.close()
                except :
                    print('Controllerとの通信に失敗しました :', datetime.now())

                continue
        finally :
            pass

if __name__ == '__main__':
    if (len(sys.argv) != 6):
        print("Usage: {} <id> <server ip> <server port> <controller ip> <controller port>".format(sys.argv[0]))
        sys.exit(1)

    sid = sys.argv[1]
    serverip = sys.argv[2]
    serverport = sys.argv[3]
    ctrip = sys.argv[4]
    ctrport = int(sys.argv[5])
    server = (serverip, int(serverport))

    while True :
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            soc.connect(server)
            #soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            print('serverとの接続に失敗しました。 : %s:%s' % (serverip, serverport))
            soc.close()
            soc = None
            continue

        try :
            data = soc.recv(4096).decode()
            print(str(data))
            cmd = str(data.rstrip())
            line = 'id;%s' % sid
            soc.send(line.encode('utf-8'))
        except :
            print('サーバーとの通信に失敗しました。')
            soc.close()
            soc = None
            continue
        loop(soc, ctrip, ctrport, sid)
        soc.close()
