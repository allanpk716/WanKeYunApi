# -*- coding: utf-8 -*-
import logging
import time
import os

# CRITICAL	50	严重错误，表明程序已不能继续运行了
# ERROR	    40	严重的问题，程序已不能执行一些功能了
# WARNING	30	有意外，将来可能发生问题，但依然可用
# INFO	    20	证明事情按预期工作
# DEBUG	    10	详细信息，调试问题时会感兴趣。
# logging.basicConfig(level=logging.INFO,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')

class LogHelper(object):
    def __init__(self, iName, cmdLevel = 'INFO', fileLevel = 'INFO'):
        logger = logging.getLogger(iName)
        logger.setLevel('DEBUG')
        BASIC_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

        # 控制台输出
        cmdHandler = logging.StreamHandler() 
        cmdHandler.setLevel(cmdLevel)

        # 输出到文件的handler
        NowFileTime = time.strftime("%Y-%m-%d_%H-%M-%S" + iName, time.localtime()) #  %H-%M-%S
        nowdirs = 'Logs\\'
        if not os.path.exists(nowdirs):
            os.makedirs(nowdirs)
        fileHandler = logging.FileHandler(filename= nowdirs + '{NowFileTime}.log'.format(NowFileTime=NowFileTime), mode='a') 
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(fileLevel)

        logger.addHandler(cmdHandler)
        logger.addHandler(fileHandler)
        
        self.logger = logger