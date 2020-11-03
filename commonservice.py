from log import Logger
import commonData,time
from TyService import TouyingService
from JDService import  JDService
from ComputerService import ComputService

class Common():
    @staticmethod
    def keyOpen(all_list):
        '''先开电，然后投影，最后开电脑'''
        Logger.getLog().logger.info("打开电源")
        commonData.SENDSIG.sendText("打开电源")
        devices = commonData.JD_DICT['devices']
        for i in range(0, 2):
            for d in range(len(devices)):
                dev = devices[d]['device']
                for t in dev:
                    ip = t['ip']
                    port = t['port']
                    addr = t['addr']
                    road = t['road'] - 1
                    cmod = JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
                    JDService.sendCommand(ip, port, cmod)
                    time.sleep(0.3)
        time.sleep(30)
        Logger.getLog().logger.info("打开投影")
        commonData.SENDSIG.sendText("打开投影")
        for i in range(0, 2):
            for ty in commonData.TERM_DICT['touying']:
                if (ty['IP'] != '192.168.3.37'):
                    Logger.getLog().logger.info('开启投影机' + ty['IP'])
                    TouyingService.Pjlink(ty['IP'], b'%1POWR 1\r')
                    # TouyingService.comm(ty['IP'],4196,bytes.fromhex('02 50 4F 4E 03'))
                    time.sleep(0.5)
        time.sleep(30)

        '''电脑全开'''
        Logger.getLog().logger.info("打开电脑")
        commonData.SENDSIG.sendText("打开电脑")
        for i in range(0, 2):
            for c in commonData.TERM_DICT['comput']:
                # checksocket = socket.socket()
                # checksocket.settimeout(2)
                # intstatus = checksocket.connect_ex((c['IP'], 5800))
                # if (intstatus == 10035):
                #     ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
                ComputService.wake_up(c['MAC'])
                time.sleep(0.2)

    @staticmethod
    def keyClose(all_list):
        '''一键全关只能关闭电脑，然后关闭投影，间隔4分钟后，最后继电器'''
        Logger.getLog().logger.info("关闭电脑")
        commonData.SENDSIG.sendText("关闭电脑")
        for c in commonData.TERM_DICT['comput']:
            # checksocket = socket.socket()
            # checksocket.settimeout(2)
            # intstatus = checksocket.connect_ex((c['IP'], 5800))
            # if(intstatus == 0 or intstatus==10061):
            #     ComputService.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            ComputService.shutComput(c['IP'], 'shutdown -s -f -t 00')
            time.sleep(0.4)

        time.sleep(30)
        Logger.getLog().logger.info("关闭投影")
        commonData.SENDSIG.sendText("关闭投影")
        for i in range(0, 2):
            for ty in commonData.TERM_DICT['touying']:
                Logger.getLog().logger.info('关闭投影机' + ty['IP'])
                # TouyingService.comm(ty['IP'], 4196,bytes.fromhex('02 50 4F 46 03'))
                TouyingService.Pjlink(ty['IP'], b'%1POWR 0\r')
                time.sleep(0.5)
        Logger.getLog().logger.info('等待50秒')
        time.sleep(300)
        Logger.getLog().logger.info("关闭电源")
        commonData.SENDSIG.sendText("关闭电源")
        for i in range(0, 2):
            for d in range(len(commonData.JD_DICT['devices'])):
                dev = commonData.JD_DICT['devices'][d]['device']
                for t in dev:
                    ip = t['ip']
                    port = t['port']
                    addr = t['addr']
                    road = t['road'] - 1
                    if not (addr == 1 and road == 7):
                        cmod = JDService.getSingleCommand(hex(addr), hex(road), '0000')
                        JDService.sendCommand(ip, port, cmod)
                        time.sleep(0.3)


