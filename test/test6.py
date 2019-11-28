import os,time
#打开时间
os.system('C:\\Users\\Public\\Desktop\\ZLVirCom.lnk')


def end_program(pro_name):
    os.system('%s%s' % (r"taskkill /F /IM ",pro_name))
#关闭时间
time.sleep(10)
end_program("ZLVirCom.exe")
os.system('C:\\Users\\Public\\Desktop\\腾讯QQ.lnk')
end_program("QQ.exe")

