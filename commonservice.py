import time,struct,socket,threading
from binascii import *
from crcmod import *
from log import Logger
import commonData
class ComputService():
    @staticmethod
    def wake_up(mac='DC-4A-3E-78-3E-0A'):
        try:

            MAC = mac
            BROADCAST = "255.255.255.255"
            Logger.getLog().logger.info(':'.join(('唤醒',mac,'网关：',BROADCAST)))
            if len(MAC) != 17:
                raise ValueError("MAC address should be set as form 'XX-XX-XX-XX-XX-XX'")
            mac_address = MAC.replace("-", '')
            data = ''.join(['FFFFFFFFFFFF', mac_address * 20])  # 构造原始数据格式
            send_data = b''

            # 把原始数据转换为16进制字节数组，
            for i in range(0, len(data), 2):
                send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])


        # 通过socket广播出去，为避免失败，间隔广播三次

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # sock.sendto(send_data, (BROADCAST, 7))
            # time.sleep(1)
            sock.sendto(send_data, (BROADCAST, 7))
            # time.sleep(1)
            # sock.sendto(send_data, (BROADCAST, 7))

        except Exception as e:
            print(e)
            Logger.getLog().logger.error(e.args)

    @staticmethod
    def shutComput(ip,command):
        try:
            Logger.getLog().logger.info('关闭主机'+ip)
            s=socket.socket()
            s.settimeout(3)
            s.connect((ip,8000))
            data='{"type":"cmd","data":"'+command+'"}'
            s.send(bytes(data,encoding='UTF-8'))
            s.close()
        except Exception as e:
            Logger.getLog().logger.error(e)

    @staticmethod
    def computForZX(zxcode,comand):
        if zxcode=='1001':
            print('1001')
            c = commonData.TERM_DICT['comput'][0]
            if comand=='on':
                ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            else:
                ComputService.shutComputfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
        elif zxcode=='1002':
            print('1002')
            c = commonData.TERM_DICT['comput'][1]
            if comand == 'on':
                ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            else:
                ComputService.shutComputfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
        elif zxcode=='1003':
            print('1003')
            c = commonData.TERM_DICT['comput'][2]
            if comand == 'on':
                ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            else:
                ComputService.shutComputfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
        elif zxcode=='1004':
            print('1004')
            c = commonData.TERM_DICT['comput'][3]
            if comand == 'on':
                ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            else:
                ComputService.shutComputfromJd(c['ip2'], c['port2'], c['addr'], c['road'])
                # ComputService.shutComput(c['IP'], 'shutdown -s -f -t 00')
        elif zxcode=='1005':
            print('1005')
            c = commonData.TERM_DICT['comput'][4]
            if comand == 'on':
                ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            else:
                ComputService.shutComputfromJd(c['ip2'], c['port2'], c['addr'], c['road'])
        elif zxcode=='1006':
            print('1006')
            c1 = commonData.TERM_DICT['comput'][10]
            c2=commonData.TERM_DICT['comput'][5]
            c3=commonData.TERM_DICT['comput'][7]
            c4=commonData.TERM_DICT['comput'][8]
            c5=commonData.TERM_DICT['comput'][9]
            if comand == 'on':
                ComputService.wake_upfromJd(c2['ip2'], c2['port2'], c2['addr'], c2['road'])
                time.sleep(0.2)
                ComputService.wake_upfromJd(c3['ip2'], c3['port2'], c3['addr'], c3['road'])
                time.sleep(0.2)
                ComputService.wake_upfromJd(c4['ip2'], c4['port2'], c4['addr'], c4['road'])
                time.sleep(0.2)
                ComputService.wake_upfromJd(c5['ip2'], c5['port2'], c5['addr'], c5['road'])
                time.sleep(0.2)
                ComputService.wake_upfromJd(c1['ip2'], c1['port2'], c1['addr'], c1['road'])
                time.sleep(0.2)
            else:
                ComputService.shutComputfromJd(c2['ip2'],c2['port2'],c2['addr'],c2['road'])
                time.sleep(0.2)
                ComputService.shutComputfromJd(c3['ip2'], c3['port2'], c3['addr'], c3['road'])
                time.sleep(0.2)
                ComputService.shutComputfromJd(c4['ip2'], c4['port2'], c4['addr'], c4['road'])
                time.sleep(0.2)
                ComputService.shutComputfromJd(c5['ip2'], c5['port2'], c5['addr'], c5['road'])
                time.sleep(0.2)
                ComputService.shutComputfromJd(c1['ip2'], c1['port2'], c1['addr'], c1['road'])
                time.sleep(0.2)
        elif zxcode=='1007':
            print('1007')
            c = commonData.TERM_DICT['comput'][6]
            if comand == 'on':
                ComputService.wake_upfromJd(c['ip2'], c['port2'], c['addr'], c['road'])
            else:
                ComputService.shutComputfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
    @staticmethod
    def wake_upfromJd(ip,port,addr,road):
        road = road - 1
        cmod = JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
        JDService.sendCommand(ip, port, cmod)
        time.sleep(0.4)
        cmod = JDService.getSingleCommand(hex(addr), hex(road), '0000')
        JDService.sendCommand(ip, port, cmod)

    @staticmethod
    def shutComputfromJd(ip, port, addr, road):
        road = road - 1
        cmod = JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
        JDService.sendCommand(ip, port, cmod)
        time.sleep(0.3)
        cmod = JDService.getSingleCommand(hex(addr), hex(road), '0000')
        JDService.sendCommand(ip, port, cmod)
class TouyingService():
    @staticmethod
    def Pjlink(ip,command):
        try:
            Logger.getLog().logger.info('发送指令到投影'+str(command,'utf-8'))
            s=socket.socket()
            s.settimeout(3)
            s.connect((ip,4352))
            result=s.recv(1024).decode('UTF-8')
            l = list(result)
            if l[7]=='0':
                s.send(command)
                re=s.recv(1024)
                Logger.getLog().logger.info('投影返回结果')
                Logger.getLog().logger.info(str(re,'utf-8'))
        except Exception as e:
            Logger.getLog().logger.error(e)
    @staticmethod
    def comm(ip,port,command):
        try:
            Logger.getLog().logger.info('发送指令到投影' + str(command,'utf-8'))
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip, port))
            s.send(command)
            re=s.recv(1024)
            Logger.getLog().logger.info('投影返回结果')
            Logger.getLog().logger.info(str(re,'utf-8'))
        except Exception as e:
            Logger.getLog().logger.error(e)
    @staticmethod
    def touyingForZX(zxcode,data):
        if zxcode=='1001':
            ty = commonData.TERM_DICT['comput'][0]
            if data=='on':
                TouyingService.comm(ty['IP'],ty['MAC'],'')
            elif data=='off':
                TouyingService.comm(ty['IP'], ty['MAC'], '')

class VideoService():

    @staticmethod
    def sendVideoCommand(despip,command):
        try:
            Logger.getLog().logger.info(':'.join(('播放器IP',despip,'指令',command)))
            s = socket.socket()
            s.settimeout(3)
            s.connect((despip,9050))
            s.send(command.encode('utf-8') + b'\n')
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

                VideoService.sendVideoCommand(videoip,command)
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
                VideoService.sendVideoCommand(videoip,command)
            else:
                VideoService.sendVideoCommand(videoip, command)
        except Exception as e:
            Logger.getLog().logger.error(e)
class JDService():
    @staticmethod
    def keyOpen(all_list):
        '''先开电，然后投影，最后开电脑'''
        Logger.getLog().logger.info("打开电源")
        devices = commonData.JD_DICT['devices']
        for d in range(len(devices)):
            dev = devices[d]['device']
            for t in dev:
                ip=t['ip']
                port=t['port']
                addr = t['addr']
                road = t['road'] - 1
                cmod = JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
                JDService.sendCommand(ip,port,cmod)
                time.sleep(0.3)

        Logger.getLog().logger.info("打开投影")
        for ty in commonData.TERM_DICT['touying']:
            Logger.getLog().logger.info('开启投影机'+ty['IP'])
            TouyingService.Pjlink(ty['IP'],b'%1POWR 1\r')

        '''电脑全开'''
        Logger.getLog().logger.info("打开电脑")
        for c in commonData.TERM_DICT['comput']:
            ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            time.sleep(0.1)

    @staticmethod
    def keyClose(all_list):
        '''一键全关只能关闭电脑，然后关闭投影，间隔4分钟后，最后继电器'''
        Logger.getLog().logger.info("关闭电脑")
        for c in commonData.TERM_DICT['comput']:
            ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
        Logger.getLog().logger.info("关闭投影")
        for ty in  commonData.TERM_DICT['touying']:
            Logger.getLog().logger.info('关闭投影机' + ty['IP'])
            TouyingService.Pjlink(ty['IP'], b'%1POWR 0\r')
        Logger.getLog().logger.info('等待50秒')
        time.sleep(50)
        Logger.getLog().logger.info("关闭电源")
        for d in range(len( commonData.JD_DICT['devices'])):
            dev =  commonData.JD_DICT['devices'][d]['device']
            for t in dev:
                ip = t['ip']
                port = t['port']
                addr = t['addr']
                road = t['road'] - 1
                if (addr==2) and (road==2):
                    print("no close")
                else:
                    cmod = JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    JDService.sendCommand(ip, port, cmod)
                    time.sleep(0.3)
    @staticmethod
    def socketONandOFF(data):
        if data=='on':
            dev =  commonData.JD_DICT['devices'][1]['device']
            for t in dev:
                ip=t['ip']
                port=t['port']
                addr = t['addr']
                road = t['road'] - 1
                cmod = JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
                JDService.sendCommand(ip,port,cmod)
                time.sleep(0.3)
        elif data=='off':
            dev = commonData.JD_DICT['devices'][1]['device']
            for t in dev:
                ip = t['ip']
                port = t['port']
                addr = t['addr']
                road = t['road'] - 1
                cmod = JDService.getSingleCommand(hex(addr), hex(road), '0000')
                JDService.sendCommand(ip, port, cmod)
                time.sleep(0.3)

    @staticmethod
    def lightONandOFF(data):
        if data == 'on':
            dev = commonData.JD_DICT['devices'][0]['device']
            for t in dev:
                ip = t['ip']
                port = t['port']
                addr = t['addr']
                road = t['road'] - 1
                cmod = JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
                JDService.sendCommand(ip, port, cmod)
                time.sleep(0.3)
        elif data == 'off':
            dev = commonData.JD_DICT['devices'][0]['device']
            for t in dev:
                ip = t['ip']
                port = t['port']
                addr = t['addr']
                road = t['road'] - 1
                cmod = JDService.getSingleCommand(hex(addr), hex(road), '0000')
                JDService.sendCommand(ip, port, cmod)
                time.sleep(0.3)
    @staticmethod
    def getSingleCommand(addr,dest,onOFF):
        s1='0500'
        return "".join((JDService.hexToString(addr),s1,JDService.hexToString(dest),onOFF))
    @staticmethod
    def getMutilCommand(addr,num,onOFF='0100'):
        s1='0F000000'
        return "".join((JDService.hexToString(addr),s1,JDService.hexToString(num),onOFF))
    @staticmethod
    def hexToString(str):
        str_list = list(str)
        if len(str_list)==3:
            str_list.insert(2, '0')
        return "".join(str_list[2:])
    @staticmethod
    def sendCommand(ip,port,comd):
        try:
            data =JDService.crc16Add(comd)
            Logger.getLog().logger.info(data)
            a_bytes = bytes.fromhex(data)
            print(a_bytes)
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip,port))
            s.send(a_bytes)
            '''还需要读取返回值'''
            re=s.recv(1024)
            Logger.getLog().logger.info('继电器返回')
            Logger.getLog().logger.info(re)
        except Exception as e:
            Logger.getLog().logger.error(e)
        # aa = ''.join(['%02x' % b for b in re])
        # act_name=act_name+"响应"
        # res=":".join((time.strftime('%Y-%m-%d %H:%M:%S'),act_name,aa))
    @staticmethod
    def crc16Add(read):
        # crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        crc16 = crcmod.predefined.mkCrcFun("modbus")

        data = read.replace(" ", "")
        readcrcout = hex(crc16(unhexlify(data))).upper()
        str_list = list(readcrcout)
        if len(str_list) == 5:
            str_list.insert(2, '0')  # 位数不足补0
        elif len(str_list) == 4:
            str_list.insert(2, '0')
            str_list.insert(2, '0')
        crc_data = "".join(str_list)
        read = read.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4]
        return read
