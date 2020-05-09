from log import Logger
import socket
class UdpServer():
    def startServer(self):
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
        while True:
            try:
                content = s.recv(1024).decode('utf-8')
                Logger.getLog().logger.info(content)
                if(content=='open1'):
                   continue
                elif(content=='open2'):
                    continue
                elif(content=='open3'):
                    continue
                elif(content=='open4'):
                    continue
                elif (content == 'close1'):
                    continue
                elif (content == 'close2'):
                    continue
                elif (content == 'close2'):
                    continue
                elif (content == 'close2'):
                    continue
            except Exception as e:
                Logger.getLog().logger.info(e)
                print(e)