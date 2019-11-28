import selectors,socket,threading,time,struct
import json,commonData
from log import Logger
from commonservice import ComputService as coms,TouyingService as tys,JDService as jds,VideoService as vs
class TablePad():
    def __init__(self):
        self.touying= commonData.TERM_DICT['touying']
        self.comput=commonData.TERM_DICT['comput']

    def get_host_ip(self):
        """
        查询本机ip地址
        :return:
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            Logger.getLog().logger.info(ip)
        finally:
            s.close()

        return ip
    def start(self):
        Logger.getLog().logger.info('启动socket')
        # 创建默认的selectors对象
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.sock.bind((self.get_host_ip(), 9080))
        self.sock.listen()
        # 设置该socket是非阻塞的
        self.sock.setblocking(False)
        # 使用sel为sock的EVENT_READ事件注册accept监听函数
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)  # ①
        # 采用死循环不断提取sel的事件
        while True:
            events = self.sel.select()
            for key, mask in events:
                # key的data属性获取为该事件注册的监听函数
                callback = key.data
                # 调用监听函数, key的fileobj属性获取被监听的socket对象
                callback(key.fileobj, mask)
    def accept(self,sockt,mask):
        conn, addr = self.sock.accept()
        # 使用socket_list保存代表客户端的socket
        conn.setblocking(False)
        print(conn)
        # 使用sel为conn的EVENT_READ事件注册read监听函数
        self.sel.register(conn, selectors.EVENT_READ, self.read)  # ②
    def read(self,skt,mask):
        try:
            # 读取数据
            data = skt.recv(1024).decode('utf-8')

            jsondata=json.loads(data)
            req_type=jsondata['type']
            Logger.getLog().logger.info('接口数据请求')
            Logger.getLog().logger.info(jsondata)
            if req_type=='init':
               initdata=jsondata['initdata']
               print(initdata)
               if initdata=='comput':
                   b = ','.join([str(x) for x in self.comput])
                   skt.send(b.encode('utf-8') + b'\n')
               elif initdata=='touying':
                   b = ','.join([str(x) for x in self.touying])
                   skt.send(b.encode('utf-8') + b'\n')
               elif initdata=='jd':
                   skt.send(commonData.ALL_JD.encode('utf-8')+b'\n')
               elif initdata=='video':
                   skt.send(commonData.REMOTE_VIDEO.encode('utf-8') + b'\n')
            elif req_type=='command':
                commobj=jsondata['commObj']
                print("控制目标："+commobj)
                if commobj=='comput':
                    destip=jsondata['destip']
                    recdata=jsondata['data']
                    destmac=jsondata['destmac']
                    if recdata=='on':
                        t1 = threading.Thread(target=coms.wake_up, args=(destmac,))
                        t1.start()
                    else:
                        command = 'shutdown -s -t 00'
                        t1 = threading.Thread(target=coms.shutComput, args=(destip, command,))
                        t1.start()
                elif commobj=='touying':
                    destip = jsondata['destip']
                    print(destip)
                    recdata = jsondata['data']
                    if recdata=='on':
                        t1 = threading.Thread(target=tys.Pjlink, args=(destip,b'%1POWR 1\r',))
                        t1.start()
                    else:
                        t1 = threading.Thread(target=tys.Pjlink, args=(destip, b'%1POWR 0\r',))
                        t1.start()
                elif commobj=='jd':
                    recdata = jsondata['data']
                    if recdata=='on':
                        t = threading.Thread(target=jds.keyOpen, args=(commonData.ALL_LIST,))
                        t.start()
                    else:
                        t = threading.Thread(target=jds.keyClose, args=(commonData.ALL_LIST,))
                        t.start()
                elif commobj=='video':
                    destip=jsondata['destip']
                    recdata=jsondata['data']
                    t=threading.Thread(target=vs.videoPlay,args=(destip,recdata,))
                    t.start()
                elif commobj=='socket':
                    recdata=jsondata['data']
                    t=threading.Thread(target=jds.socketONandOFF,args=(recdata,))
                    t.start()
                elif commobj=='light':
                    recdata=jsondata['data']
                    t=threading.Thread(target=jds.lightONandOFF,args=(recdata,))
                    t.start()

            else:
                # 如果该socket已被对方关闭，关闭该socket，
                # 并从socket_list列表中删除
                print('关闭', skt)
                self.sel.unregister(skt)
                skt.close()
            # 如果捕捉到异常, 将该socket关闭，并从socket_list列表中删除
        except Exception as e:
            Logger.getLog().logger.error(e)
            self.sel.unregister(skt)
            skt.close()

