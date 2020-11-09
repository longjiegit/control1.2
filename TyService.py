"""
投影服务类
"""
import commonData
from log import Logger
import time,hashlib,socket
class TouyingService():
    @staticmethod
    def Pjlink(ip,command):
        try:
            Logger.getLog().logger.info('发送指令到投影'+ip+str(command,'utf-8'))
            commonData.SENDSIG.sendText('发送指令到投影'+ip+str(command,'utf-8'))
            s=socket.socket()
            s.settimeout(5)
            s.connect((ip,4352))
            result=s.recv(1024).decode('UTF-8')
            l = list(result)
            if l[7]=='0':
                s.send(command)
                re=s.recv(1024)
                Logger.getLog().logger.info('投影返回结果')
                Logger.getLog().logger.info(str(re,'utf-8'))
                commonData.RECSIG.sendText('投影返回结果'+str(re,'utf-8'))
        except Exception as e:
            commonData.RECSIG.sendText(ip+str(e))
            Logger.getLog().logger.error(e)
    @staticmethod
    def comm(ip,port,command):
        try:
            Logger.getLog().logger.info('发送指令到投影' + str(command,'utf-8'))
            commonData.SENDSIG.sendText('发送指令到投影' + str(command, 'utf-8'))
            s = socket.socket()
            s.settimeout(3)
            port=int(port)
            s.connect((ip, port))
            s.send(command)
            re=s.recv(1024)
            Logger.getLog().logger.info('投影返回结果')
            Logger.getLog().logger.info(str(re,'utf-8'))
            commonData.RECSIG.sendText('投影返回结果' + str(re, 'utf-8'))
        except Exception as e:
            Logger.getLog().logger.error(e)
    def Panasonic(self,ip,port,command):
        try:
            s=socket.socket()
            s.settimeout(3)
            s.connect((ip,1024))
            result=s.recv(1024).decode('UTF-8')
            l=list(result)
            x='admin'
            y='admin'
            z = l[12] + l[13] + l[14] + l[15] + l[16] + l[17] + l[18] + l[19]
            s1 = ':'.join((x, y, z))
            m = hashlib.md5(s1.encode())
            cmd = m.hexdigest() + command
            s.send(cmd.encode('utf-8'))
            re = s.recv(1024)
            Logger.getLog().logger.info(re)
        except Exception as e:
            Logger.getLog().logger.error(e)
    @staticmethod
    def touyingForZX(zxcode,data):
        if zxcode=='0000':
            if data=='on':
                for ty in commonData.TERM_DICT['touying']:
                    Logger.getLog().logger.info('开启投影机' + ty['IP'])
                    TouyingService.Pjlink(ty['IP'],b'%1POWR 1\r')
                    time.sleep(0.5)
            elif data=='off':
                for ty in commonData.TERM_DICT['touying']:
                    Logger.getLog().logger.info('关闭投影机' + ty['IP'])
                    TouyingService.Pjlink(ty['IP'], b'%1POWR 0\r')
                    time.sleep(0.5)
        elif zxcode=='1001':
            if data=='on':
                for i in range(0,16):
                    ip=commonData.TERM_DICT['touying'][i]['IP']
                    Logger.getLog().logger.info('开启投影机' + ip)
                    TouyingService.Pjlink(ip, b'%1POWR 1\r')
                    time.sleep(0.5)
            elif data=='off':
                for i in range(0,16):
                    ip=commonData.TERM_DICT['touying'][i]['IP']
                    Logger.getLog().logger.info('关闭投影机' + ip)
                    TouyingService.Pjlink(ip, b'%1POWR 0\r')
                    time.sleep(0.5)
        elif zxcode=='1002':
            if data=='on':
                for i in range(16,17):
                    ip=commonData.TERM_DICT['touying'][i]['IP']
                    Logger.getLog().logger.info('开启投影机' + ip)
                    TouyingService.Pjlink(ip, b'%1POWR 1\r')
                    time.sleep(0.5)
            elif data=='off':
                for i in range(16,17):
                    ip=commonData.TERM_DICT['touying'][i]['IP']
                    Logger.getLog().logger.info('关闭投影机' + ip)
                    TouyingService.Pjlink(ip, b'%1POWR 0\r')
                    time.sleep(0.5)