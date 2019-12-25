import json,codecs
from log import Logger
global ALL_LIST
ALL_LIST=[]
global JD_DICT
global TERM_DICT
global VIDEO_LIST
VIDEO_LIST=[]
global ALL_JD
ALL_JD=''
global REMOTE_VIDEO
REMOTE_VIDEO=''
global REGIST



with open("c.json", 'r', encoding='utf-8') as load_f:
        # data = load_f.read().decode(encoding='gbk').encode(encoding='utf-8')
    content=load_f.read()
    if content.startswith(u'\ufeff'):
        TERM_DICT=json.loads(content.encode('utf8')[3:].decode('utf8'))
    else:
        TERM_DICT = json.loads(content)

    Logger.getLog().logger.info("加载终端数据完成")
with open("jd.json", 'r', encoding='utf-8') as load_f:
    content = load_f.read()
    if content.startswith(u'\ufeff'):
        JD_DICT = json.loads(content.encode('utf8')[3:].decode('utf8'))
    else:
        JD_DICT = json.loads(content)
    Logger.getLog().logger.info("加载继电器数据完成")
with codecs.open("videoPlay.txt", 'r', 'utf-8', buffering=True) as f:
    for line in f:
        if line != '\r\n':
            l = line.replace("\r\n", '')
            REMOTE_VIDEO+=l
            REMOTE_VIDEO+=';'
            list = l.split(',')
            VIDEO_LIST.append(list)
    Logger.getLog().logger.info('加载播放器数据完成')
with codecs.open('./lib/zl.txt','r','utf-8',buffering=True) as f:
    for line in f:
        print(line)
        if line !='\r\n':
            REGIST=line
    Logger.getLog().logger.info("加载注册数据完成")