"""
视频播放类
"""
import socket,commonData,argparse,time,threading
from pythonosc import udp_client
from log import Logger
from JDService import JDService

class VideoService():
    @staticmethod
    def sendVoiceCommnad(destip,command):
        try:
            Logger.getLog().logger.info('声音控制'+destip)
            # commonData.SENDSIG.sendText('声音控制'+destip)
            s=socket.socket()
            s.settimeout(3)
            s.connect((destip,8000))
            data='{"type":"sysvoice","data":"'+command+'"}'
            s.send(bytes(data,encoding='UTF-8'))
            s.close()
        except Exception as e:
            Logger.getLog().logger.error(e)
            # commonData.RECSIG.sendText(destip+str(e))
    @staticmethod
    def sendVideoCommand(despip,command):
        try:
            commonData.SENDSIG.sendText(':'.join(('播放器IP',despip,'指令',command)))
            Logger.getLog().logger.info(':'.join(('播放器IP',despip,'指令',command)))
            s = socket.socket()
            s.settimeout(3)
            s.connect((despip,9050))
            s.send(command.encode('utf-8') + b'\n')
        except Exception as e:
            commonData.RECSIG.sendText(despip + str(e))
            Logger.getLog().logger.error(e)
    @staticmethod
    def sendOSCCommand(destip,command):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument("--ip", default=destip,
                                help="The ip of the OSC server")
            parser.add_argument("--port", type=int, default=7000,
                                help="The port the OSC server is listening on")
            args = parser.parse_args()
            client = udp_client.SimpleUDPClient(args.ip, args.port)
            client.send_message(command, 1)
        except Exception as e:
            Logger.getLog().logger.error(e)
    @staticmethod
    def guangmoCommand(ip,command):
        try:
            commonData.SENDSIG.sendText(':'.join(('播放器IP', ip, '指令', str(command,'utf-8'))))
            Logger.getLog().logger.info(':'.join(('播放器IP', ip, '指令', str(command,'utf-8'))))
            upd_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            upd_socket.sendto(command,(ip,11412))
            upd_socket.close()
        except Exception as e:
            Logger.getLog().logger.error(e)
            print(e)
    @staticmethod
    def siteCommand(ip,command):
        try:
            commonData.SENDSIG.sendText(':'.join(('座椅动作IP', '192.168.3.16', '指令', command)))
            Logger.getLog().logger.info(':'.join(('座椅动作IP', '192.168.3.16', '指令', command)))
            upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            upd_socket.sendto(command.encode('utf-8'), ('192.168.3.16', 12346))
            upd_socket.close()
        except Exception as e:
            Logger.getLog().logger.error(e)
            print(e)
    @staticmethod
    def siteCommand2(command):
        try:
            commonData.SENDSIG.sendText(':'.join(('播放器IP', '192.168.3.16', '指令', command.strip('\n').strip('\r'))))
            Logger.getLog().logger.info(':'.join(('播放器IP', '192.168.3.16', '指令', command.strip('\n').strip('\r'))))
            s = socket.socket()
            s.settimeout(3)
            s.connect(('192.168.3.16', 57910))
            s.send(bytes(command, encoding='UTF-8'))
            s.close()
        except Exception as e:
            Logger.getLog().logger.error(e)
    @staticmethod
    def videoForZX(zxcode,command):
        if zxcode=='1001':
            print('1001')
            VideoService.videoPlay("1",command)
        elif zxcode=='1002':
            print('1002')
            VideoService.videoPlay("2", command)
        elif zxcode=='1003':
            print('1003')
            VideoService.videoPlay("3", command)
        elif zxcode=='1004':
            print('1004')
            VideoService.videoPlay("4", command)
        elif zxcode=='1005':
            print('1005')
            VideoService.videoPlay("5", command)
    @staticmethod
    def videoPlayThread(destip,command):
        t = threading.Thread(target=VideoService.videoPlay, args=(destip, command,))
        t.start()
    #despid,序号，从1开始
    @staticmethod
    def videoPlay(despip, command):
        try:
            despip=despip.encode('utf-8').decode('utf-8-sig')
            videoip=commonData.VIDEO_LIST[int(despip)-1][1]
            if(command=='play'):
                try:
                    index =commonData.VIDEO_LIST[int(despip)-1][4]
                    lines = commonData.VIDEO_LIST[int(despip)-1][5]
                    lineList = lines.split("#")
                    device = commonData.JD_DICT['devices'][int(index) - 1]
                    for lineNum in lineList:
                        line = int(lineNum)
                        IP = device['device'][line - 1]['ip']
                        port = device['device'][line - 1]['port']
                        dest =device['device'][line - 1]['road']
                        addr = device['device'][line - 1]['addr']
                        cmod = JDService.getSingleCommand(hex(addr), hex(dest - 1), '0000')
                        Logger.getLog().logger.info("关灯"+cmod)
                        JDService.sendCommand(IP, port, cmod)
                        time.sleep(0.3)
                except Exception as e:
                    print(e)
                # VideoService.siteCommand(videoip, '1#101')
                # time.sleep(2)
                if despip=='1':
                    data = '{"ID":0,"CmdType":3,"Data":null}\r\r\n'
                    VideoService.siteCommand2(data)
                    time.sleep(4)
                    data = '{"ID":101,"CmdType":1,"Data":null}\r\r\n'
                    VideoService.siteCommand2(data)
                    # VideoService.siteCommand(videoip, '1#101')
                    time.sleep(commonData.LAZY)
                    # VideoService.sendVideoCommand('192.168.3.16', 'zxplay,5')
                    VideoService.guangmoCommand(videoip,bytes.fromhex('4D 00 53 00 47 00 5F 00 46 00 50 00 43 00 4D 00 44 00 7C 00 54 00 72 00 61 00 63 00 6B 00 5F 00 50 00 6C 00 61 00 79 00 54 00 72 00 61 00 63 00 6B 00 7C 00 30 00 7C 00 00 00'))

                elif despip=='2':
                    data = '{"ID":0,"CmdType":3,"Data":null}\r\r\n'
                    VideoService.siteCommand2(data)
                    time.sleep(4)
                    data = '{"ID":102,"CmdType":1,"Data":null}\r\r\n'
                    VideoService.siteCommand2(data)
                    # VideoService.siteCommand(videoip, '1#102')
                    time.sleep(commonData.LAZY)
                    # VideoService.sendVideoCommand('192.168.3.16','zxplay,1')
                    VideoService.guangmoCommand(videoip, bytes.fromhex(
                        '4D 00 53 00 47 00 5F 00 46 00 50 00 43 00 4D 00 44 00 7C 00 54 00 72 00 61 00 63 00 6B 00 5F 00 50 00 6C 00 61 00 79 00 54 00 72 00 61 00 63 00 6B 00 7C 00 32 00 7C 00 00 00'))

                elif despip=='3':
                    data = '{"ID":0,"CmdType":3,"Data":null}\r\r\n'
                    VideoService.siteCommand2(data)
                    time.sleep(4)
                    data = '{"ID":103,"CmdType":1,"Data":null}\r\r\n'
                    VideoService.siteCommand2(data)
                    # VideoService.siteCommand(videoip, '1#103')
                    # VideoService.sendVideoCommand('192.168.3.16', 'zxplay,2')
                    time.sleep(commonData.LAZY)
                    VideoService.guangmoCommand(videoip, bytes.fromhex(
                        '4D 00 53 00 47 00 5F 00 46 00 50 00 43 00 4D 00 44 00 7C 00 54 00 72 00 61 00 63 00 6B 00 5F 00 50 00 6C 00 61 00 79 00 54 00 72 00 61 00 63 00 6B 00 7C 00 34 00 7C 00 00 00'))

            elif command=='stop':
                """灯光开"""
                try:
                    index = commonData.VIDEO_LIST[int(despip) - 1][4]
                    lines = commonData.VIDEO_LIST[int(despip) - 1][5]
                    lineList = lines.split("#")
                    device = commonData.JD_DICT['devices'][int(index) - 1]
                    for lineNum in lineList:
                        line = int(lineNum)
                        IP = device['device'][line - 1]['ip']
                        port = device['device'][line - 1]['port']
                        dest = device['device'][line - 1]['road']
                        addr = device['device'][line - 1]['addr']
                        cmod = JDService.getSingleCommand(hex(addr), hex(dest - 1), 'FF00')
                        Logger.getLog().logger.info("开灯" + cmod)
                        JDService.sendCommand(IP, port, cmod)
                        time.sleep(0.3)
                except Exception as e:
                    print(e)
                # VideoService.sendVideoCommand(videoip,command)
                data = '{"ID":0,"CmdType":3,"Data":null}\r\r\n'
                VideoService.siteCommand2(data)
                # VideoService.sendVideoCommand('192.168.3.16', 'stop')
                # VideoService.siteCommand(videoip, '2#0')
                VideoService.guangmoCommand(videoip, bytes.fromhex('4D 00 53 00 47 00 5F 00 46 00 50 00 43 00 4D 00 44 00 7C 00 54 00 72 00 61 00 63 00 6B 00 5F 00 53 00 74 00 6F 00 70 00 7C 00 00 00'))
                # VideoService.siteCommand(videoip, '2#0')

            elif command=="voiceadd":
                VideoService.sendVoiceCommnad(videoip,"addvoice")
            elif command=="minusvoice":
                VideoService.sendVoiceCommnad(videoip,"minusvoice")
            elif command=="voiceclose":
                VideoService.sendVoiceCommnad(videoip,"mutevoice")
            elif command=='closelight':
                try:
                    index =commonData.VIDEO_LIST[int(despip)-1][4]
                    lines = commonData.VIDEO_LIST[int(despip)-1][5]
                    lineList = lines.split("#")
                    device = commonData.JD_DICT['devices'][int(index) - 1]
                    for lineNum in lineList:
                        line = int(lineNum)
                        IP = device['device'][line - 1]['ip']
                        port = device['device'][line - 1]['port']
                        dest =device['device'][line - 1]['road']
                        addr = device['device'][line - 1]['addr']
                        cmod = JDService.getSingleCommand(hex(addr), hex(dest - 1), '0000')
                        Logger.getLog().logger.info("关灯"+cmod)
                        JDService.sendCommand(IP, port, cmod)
                        time.sleep(0.2)
                except Exception as e:
                    print(e)
            else:
                VideoService.sendVideoCommand(videoip, command)
        except Exception as e:
            Logger.getLog().logger.error(e)