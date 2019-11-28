import  json
data='{"type":"init,command","initdata":"comput,jd,touying,video","destip":"192.168","destmac":"mac","data":""}'
t=json.loads(data)
print(type(t))
print(t['type'])
print(t['initdata'])