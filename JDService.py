from log import Logger
import commonData,time,socket
from binascii import *
from crcmod import *
class JDService():

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
                commonData.SENDSIG.sendText("".join(("开灯", cmod)))
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
            commonData.RECSIG.sendText(str(re))
        except Exception as e:
            commonData.RECSIG.sendText(comd+str(e))
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