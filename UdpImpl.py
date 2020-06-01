from log import Logger
import socket,commonservice,time
class UdpServer():
    def startServer(self):
        Logger.getLog().logger.info('upd监听程序启动')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s1.connect(('8.8.8.8', 80))
            ip = s1.getsockname()[0]
        except Exception as e:
            print(e.args)
        finally:
            s1.close()
        # 将socket绑定到本机IP和端口
        s.bind((ip, 8100))
        # 服务端开始监听来自客户端的连接
        ip2="192.168.1.200"
        port2=4196
        while True:
            try:
                content = s.recv(1024).decode('utf-8')
                Logger.getLog().logger.info(content)
                if(content=='open1'):
                   addr=3
                   road=3
                   cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                   commonservice.JDService.sendCommand(ip2, port2, cmod)
                   time.sleep(0.2)
                   road==2
                   cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                   commonservice.JDService.sendCommand(ip2, port2, cmod)
                   time.sleep(0.2)
                   road=1
                   cmod=commonservice.JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
                   commonservice.JDService.sendCommand(ip2, port2, cmod)
                elif(content=='open2'):
                    addr = 3
                    road=1
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                    time.sleep(0.2)
                    road=3
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                    time.sleep(0.2)
                    road = 2
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                elif(content=='open3'):
                    addr = 3
                    road=1
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                    time.sleep(0.2)
                    road=2
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                    time.sleep(0.2)
                    road = 3
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), 'FF00')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                elif (content == 'close'):
                    addr = 3
                    road = 1
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                    time.sleep(0.2)
                    road=2
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                    time.sleep(0.2)
                    road=3
                    cmod = commonservice.JDService.getSingleCommand(hex(addr), hex(road), '0000')
                    commonservice.JDService.sendCommand(ip2, port2, cmod)
                    time.sleep(0.2)
            except Exception as e:
                Logger.getLog().logger.info(e)
                print(e)