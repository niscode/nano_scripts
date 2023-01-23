# coding: utf-8

import sys
import socket
import time
import websocket
import threading
import select
import ssl
from datetime import datetime, timedelta
import json
import rel
import requests

jetsonIP = "10.186.42.60"

addr = ''
port = 0
cws = None


### socket client ####
def __sendmsg(soc, msg) :
    result = True
    n = len(msg)
    remain = n
    while remain > 0 :
        try :
            t = soc.send(msg)
            print(" socket client 使ってるのよ")
            remain -= t
            msg = msg[t:]
        except :
            result = False
            break
    return result

def doSotaCommand(soc, cmd) :
    result = True

    cmdlist = []
    initstr = 'M0 0 800 -40 -800 40 0 0 0 0 0 0 -50 0\n'
    if cmd == '*init*' :
        cmdlist = ["S\n"]
    elif cmd == '*terminate*' :
        cmdlist = ["E\n"]
    else :
        pass
    
    for command in cmdlist :
        if len(command) == 0 : continue
        #print("command =", command)
        if command[0] == '*' :
            n = int(command[1:]) / 1000
            time.sleep(n)
        else :
            if not __sendmsg(soc, command.encode('utf-8')) :
                result = False
                break
            try :
                msg = soc.recv(1024)
            except :
                result = False
                break
            
    return result

# def login(soc, sid):
#     sf = soc.makefile()
#     try :
#         data = soc.recv(4096).decode()
#         print(str(data))
#         cmd = str(data.rstrip())
#         line = 'id;%s' % sid
#         #print(line)
#         soc.send(line.encode('utf-8'))
#         rdata = soc.recv(4096).decode()
#         # サーバから受信したデータを出力
#         print(rdata)
#     except :
#         print('サーバーとの通信に失敗しました。')
#         sys.exit(0)

def loop(serversoc, adr,port, tlc):
    #tlc  = ("localhost", 1234)
    #tlc  = ("10.186.42.31", 1234)
    sota = (adr, port)
    st = serversoc.makefile()

    tlc_soc = None
    
    while True:
        if tlc_soc is None :
            tlc_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                tlc_soc.connect(tlc)
            except :
                print('SotaServerとの通信に失敗しました :', datetime.now())
                tlc_soc = None
                time.sleep(5)
                continue
            if not doSotaCommand(tlc_soc, '*init*') :
                print('SotaServerとの通信に失敗しました :', datetime.now())
                tlc_soc.close()
                tlc_soc = None
                time.sleep(5)
                continue

        try :
            data = st.readline().strip()
            #data = serversoc.recv(4096)
            print(data)
            #data = data.decode()
        except socket.timeout :
            continue
            
        cmd = str(data.rstrip())
        #cmd = st.readline()
        if len(cmd) <= 3 :
            continue
        #print(cmd)
        header = cmd[:3]
        if header == 'tlc' :
            if not doSotaCommand(tlc_soc, cmd) :
                print('Commu4Serverとの通信に失敗しました :', datetime.now())
                tlc_soc.close()
                tlc_soc = None
                continue
        else :
            try :
                sota_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sota_soc.connect(sota)
                sota_soc.send(cmd.encode('utf-8')) #(bytes(cmd))
                #cmd = st.readline()
                sota_soc.close()
                sota_soc = None
            except :
                print('SOTAとの通信に失敗しました :', datetime.now())

            if cmd == "cmd;motion;Nodding":
                print("Nodding")
            elif cmd == "cmd;motion;HeadShaking":
                print("HeadShaking")
            elif cmd == "cmd;motion;RightHandWaving":
                print("RightHandWaving")
            elif cmd == "cmd;motion;LeftHandWaving":
                print("LeftHandWaving")
            elif cmd == "cmd;motion;BothHandWaving":
                print("BothHandWaving")
            elif cmd == "cmd;motion;BothHandRaising":
                print("BothHandRaising")
            elif cmd == "cmd;end":
                print("End")
            else:
                pass
                    # print("Unknown command")



### web-socket client ####
def sendJsonCommand(ws, index):
    commands = jsonCommands[index]
    for msg in commands:
        print(msg)
        if(type(msg) is dict):
            ws.send(json.dumps(msg))
        else:
            cols = msg.split('/wait')
            millisec = int(cols[1])
            time.sleep(millisec / 1000.0)


# j -> for sota system
def on_message_j(ws, message):
    print('M:', message)

def on_error_j(ws, error):
    print('E:', error)

def on_close_j(ws):
    print("Closing")

def on_open_j(ws):
    print("openning")
    # sendJsonCommand(ws, 6)


# no j -> for capf
def on_error(ws, error):
    print('Ex:', error)

def on_close(ws):
    print("Closing")

def on_open(ws):
    print("openning")


def on_message(ws, message):
    global cws
    global addr
    global port
    global scenario
    scenario = ''

    if message == 'something' : return
    print('M:', message, addr, port, cws)
    sota = (addr, port)
    cmd = message
    # print(cmd)
    header = message[:1]

    # 音声案内コマンド 18 items   先頭 11items はブース紹介用 -- 2022/10/28  -- 2022/10/28
    if header == "V" :
        if cmd == "V_Self" :
            sendJsonCommand(cws, 0)
        else :
            num_i = 0
            while cmd != V_cmdlist[num_i][0] :
                num_i += 1
            scenario = V_cmdlist[num_i][1]

            if num_i < 11 :
                sendJsonCommand(cws, num_i + 1)
                print ('\033[34m' + V_cmdlist[num_i][0] + ' 音声案内のコマンドを受け取ったよ。ブースの紹介文を発話するね: \n' + scenario + '\033[0m')
                print()
            else :
                sendJsonCommand(cws, num_i + 1)
                print ('\033[34m' + V_cmdlist[num_i][0] + ' 音声案内のコマンドを受け取ったよ。場所の案内を開始するね: \n' + scenario + '\033[0m')

    if header == "H" :
        if cmd == "H_short1" :
            sendJsonCommand(cws, 27)
            print ('\033[34m' + ' 短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short2" :
            sendJsonCommand(cws, 28)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short3" :
            sendJsonCommand(cws, 29)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short4" :
            sendJsonCommand(cws, 30)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')
        if cmd == "H_short5" :
            sendJsonCommand(cws, 31)
            print ('\033[34m' + '短い音声案内のコマンドを受け取ったよ。短く挨拶するね: \n' + '\033[0m')


    # 動作コマンド 14 items   先頭 6items はナビゲーション用 -- 2022/10/28
    if header == "M" :
        num_j = 0
        while cmd != M_cmdlist[num_j] :
            num_j += 1

        if num_j < 7 :
            client.cancel_goal()    #実行中のnavigationを中断するリクエスト
            try:
                goal_pose = MoveBaseGoal()
                goal_pose.target_pose.header.frame_id = 'map'
                goal_pose.target_pose.pose.position.x = nav_dict[cmd][0]
                goal_pose.target_pose.pose.position.y = nav_dict[cmd][1]
                goal_pose.target_pose.pose.position.z = nav_dict[cmd][2]
                goal_pose.target_pose.pose.orientation.x = nav_dict[cmd][3]
                goal_pose.target_pose.pose.orientation.y = nav_dict[cmd][4]
                goal_pose.target_pose.pose.orientation.z = nav_dict[cmd][5]
                goal_pose.target_pose.pose.orientation.w = nav_dict[cmd][6]
                #clientとしてgoalをサーバーに送ると同時にfeedback_cb関数を呼び出す
                result = client.send_goal(goal_pose)
                print ('\033[32m' + M_cmdlist[num_j] + ' ... ナビゲーションを実行するね。' + '\033[0m')
                if result:
                    print(result)
                    rospy.loginfo("Goal execution done!")
            except rospy.ROSInterruptException:
                rospy.loginfo("Navigation test finished.")

        else :
            sendJsonCommand(cws, num_j + 12)
            print ('\033[32m' + '動作コマンド ' + M_cmdlist[num_j] + ' を実行するね' + '\033[0m')


    else :
        if cmd == "cmd;Forward" or cmd == "cmd;TurnLeft" or cmd == "cmd;TurnRight" or cmd == "cmd;Backward" or cmd == "cmd;Stop":
            print ('\033[33m' + cmd + ' ... マニュアルモードで移動するよ。' + '\033[0m')
            p=rospy.Publisher('rover_twist',Twist, queue_size=10)
            rate = rospy.Rate(10)

            x = moveBindings[cmd][0]
            y = moveBindings[cmd][1]
            z = moveBindings[cmd][2]
            th = moveBindings[cmd][3]
            
            t = Twist()
            t.linear.x = x * 0.1
            t.linear.y = y * 0.1
            t.linear.z = z * 0.1
            t.angular.x = 0
            t.angular.y = 0
            t.angular.z = th * 0.2
            
            for i in range(0, 5) :
                p.publish(t)
                rate.sleep()
        
        # print(cmd)
        if cmd == "cmd;scenario;self_intro" :
            sendJsonCommand(cws, 0)



if __name__ == '__main__':
    #global cws
    #global addr
    #global port

    if (len(sys.argv) != 9):
        print("Usage: {} <login url> <id> <passwd> <websocket url> <jetson ip> <jetson port> <sota ip> <sota port>".format(sys.argv[0]))
        sys.exit(1)

    login_url = sys.argv[1]
    sid = sys.argv[2]
    passwd = sys.argv[3]

    websockurl = sys.argv[4]
    addr = sys.argv[5]
    port = int(sys.argv[6])
    sotaip = (sys.argv[7], int(sys.argv[8]))
    websocket.enableTrace(True)




    print('sota_ip =', sotaip)
    try :
        soc.connect(server)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        print('serverとの接続に失敗しました。 : %s:%s' % (sotaip[0], sotaip[1]))
        sys.exit(0)

        
    # login(soc, sid)
    loop(soc, sotaip, sotaport, tlc)
    soc.clonse()
    




    cws = websocket.WebSocketApp("ws://%s:%d/command" %( sotaip[0], sotaip[1]),
                              on_message = on_message_j,
                              on_error = on_error_j,
                              on_close = on_close_j)
    #cws.on_open = on_open_j
    cwst = threading.Thread(target=cws.run_forever)
    cwst.daemon = True
    cwst.start()

    payload = {"name" : sid, "password" : passwd}
    r = requests.post(login_url, params = payload)
    authorisation = json.loads(r.text)["authorisation"]
    token = authorisation["token"]
    ws = websocket.WebSocketApp(websockurl + "?token=" + token,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    wst = threading.Thread(target = ws.run_forever)
    wst.daemon = True
    wst.start()
    try:
        while not rospy.is_shutdown():
        # while True :
            time.sleep(1.0)
    except KeyboardInterrupt:
        print('Ctrl-C を受け取りました。プログラムを終了します,,,,,,')
        sys.exit(1)