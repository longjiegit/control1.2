import codecs
global ALL_LIST
ALL_LIST=[]
with codecs.open("../allopenorshut", 'r', 'utf-8', buffering=True) as f:
    for line in f:
        if line!='\r\n':
            l=line.replace("\r\n",'')
            list=l.split(',')
            ALL_LIST.append(list)
    print(ALL_LIST)
