from log import Logger
import commonData
import struct,socket,time
from JDService import JDService
class ComputService():
    @staticmethod
    def wake_up(mac='DC-4A-3E-78-3E-0A'):
        try:
            MAC = mac
            BROADCAST = "255.255.255.255"
            Logger.getLog().logger.info(':'.join(('唤醒',mac,'网关：',BROADCAST)))
            commonData.SENDSIG.sendText("".join(("开启电脑", mac)))
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
            sock.sendto(send_data, (BROADCAST, 7))
            time.sleep(1)
            sock.sendto(send_data, (BROADCAST, 7))
            time.sleep(1)
            sock.sendto(send_data, (BROADCAST, 7))

        except Exception as e:
            print(e)
            Logger.getLog().logger.error(e.args)

    @staticmethod
    def shutComput(ip,command):
        try:
            Logger.getLog().logger.info('关闭主机'+ip)
            commonData.SENDSIG.sendText('关闭主机'+ip)
            s=socket.socket()
            s.settimeout(3)
            s.connect((ip,8000))
            data='{"type":"cmd","data":"'+command+'"}'
            s.send(bytes(data,encoding='UTF-8'))
            s.close()
        except Exception as e:
            Logger.getLog().logger.error(e)
            commonData.RECSIG.sendText(ip+str(e))

    @staticmethod
    def computForZX(zxcode,comand):
        if zxcode=='0000':
            if comand=='on':
                for c in commonData.TERM_DICT['comput']:
                    ComputService.wake_up(c['MAC'])
                    time.sleep(0.2)
            elif comand=='off':
                for c in commonData.TERM_DICT['comput']:
                    ComputService.shutComput(c['IP'],'shutdown -s -f -t 00')
                    time.sleep(0.2)
        elif zxcode=='1001':
            if comand=='on':
                for i in range(0,5):
                    mac=commonData.TERM_DICT['comput'][i]['MAC']
                    ComputService.wake_up(mac)
                    time.sleep(0.2)
            elif comand=='off':
                for i in range(0,5):
                    ip=commonData.TERM_DICT['comput'][i]['IP']
                    ComputService.shutComput(ip,'shutdown -s -f -t 00')
                    time.sleep(0.2)
        elif zxcode=='1002':
            if comand=='on':
                for i in range(5,6):
                    mac=commonData.TERM_DICT['comput'][i]['MAC']
                    ComputService.wake_up(mac)
                    time.sleep(0.2)
            elif comand=='off':
                for i in range(5,6):
                    ip=commonData.TERM_DICT['comput'][i]['IP']
                    ComputService.shutComput(ip,'shutdown -s -f -t 00')
                    time.sleep(0.2)

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
        time.sleep(0.4)
        cmod = JDService.getSingleCommand(hex(addr), hex(road), '0000')
        JDService.sendCommand(ip, port, cmod)