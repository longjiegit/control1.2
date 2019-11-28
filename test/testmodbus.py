import socket,struct,time
import binascii
from binascii import *
from crcmod import *
import time
import selectors, socket, threading

def crc16(x, invert):
    a = 0xFFFF
    b = 0xA001
    for byte in x:
        a ^= ord(byte)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()

    return s[4:6] + s[2:4] if invert == True else s[2:4] + s[4:6]
def crc16Add(read):
    # crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    crc16=crcmod.predefined.mkCrcFun("modbus")

    data = read.replace(" ", "")
    readcrcout = hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    elif len(str_list)==4:
        str_list.insert(2,'0')
        str_list.insert(2,'0')
    crc_data = "".join(str_list)
    read = read.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4]
    # print('CRC16校验:', crc_data[4:] + ' ' + crc_data[2:4])
    # print('增加Modbus CRC16校验：>>>', read)
    return read


command='1C05000'
on='FF00'
off='0000'
 # 创建默认的selectors对象
sel = selectors.DefaultSelector()
# 负责监听“有数据可读”事件的函数
def read(conn, mask):
    data = conn.recv_into() # Should be ready
    if data:
        print(data)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()
# 创建socket对象
s = socket.socket()
# 连接远程主机
s.connect(('192.168.2.200', 4196))
# 设置该socket是非阻塞的
# s.setblocking(False)
# 使用sel为s的EVENT_READ事件注册read监听函数
# sel.register(s, selectors.EVENT_READ, read)    # ①
s = socket.socket()
# 连接远程主机
s.connect(('192.168.2.200', 4196))

def aa():
    for i in range(2,-1,-1):

        print(i)
        c = command + str(i)
        data = crc16Add(c+on)
        a_bytes = bytes.fromhex(data)
        s.sendall(a_bytes)
        time.sleep(3)
        d = s.recv(1024)
        print(d)
aa()
def bb():
    while True:
        d=s.recv(1024)
        print(d)
# threading.Thread(target=bb, args=()).start()
# threading.Thread(target=aa, args=()).start()

# while True:
#     # 获取事件
#     events = sel.select()
#     for key, mask in events:
#         # key的data属性获取为该事件注册的监听函数
#         callback = key.data
#         # 调用监听函数, key的fileobj属性获取被监听的socket对象
#         callback(key.fileobj, mask)



