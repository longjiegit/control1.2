from IPy import IP
input_IP = '192.168.3.12'
list1 = input_IP.split('.')
if len(list1) != 4:
  print ("您输入的ip地址不合法，请重新输入！")
  exit()
for i in list1:
  if i.isdigit() == True and int(i) >=0 and int(i) <= 255:
    pass
  else:
    print("您输入的ip地址不合法，请重新输入！")
    exit()
input_Netmask = "255.255.255.0"
list2 = input_Netmask.split('.')
if len(list2) != 4:
  print("您输入的子网掩码不合法，请重新输入!")
  exit()
for i in list2:
  if i.isdigit() == True and int(i) >=0 and int(i) <= 255:
    pass
  else:
    print ("您输入的子网掩码不合法，请重新输入!")
    exit()
print ("您所在的网段为:%s" % len(IP(input_IP)))
