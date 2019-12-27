# -*- coding: utf-8 -*-
import logging
import time

# CRITICAL	50	严重错误，表明程序已不能继续运行了
# ERROR	    40	严重的问题，程序已不能执行一些功能了
# WARNING	30	有意外，将来可能发生问题，但依然可用
# INFO	    20	证明事情按预期工作
# DEBUG	    10	详细信息，调试问题时会感兴趣。
# logging.basicConfig(level=logging.INFO,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel('INFO')
BASIC_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

BASIC_FORMAT_CMD = '%(message)s'
formatterCMD = logging.Formatter(BASIC_FORMAT_CMD)

# 输出到控制台的 handler
# cmdHandler = logging.FileHandler(filename='WanKeYunApi.log', mode='w')
# 文件输出
# cmdHandler.setFormatter(formatterCMD)
# 控制台输出
cmdHandler = logging.StreamHandler() 
cmdHandler.setLevel('INFO')
# 输出到文件的handler
NowFileTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
fileHandler = logging.FileHandler(filename='WanKeYunApi {NowFileTime}.log'.format(NowFileTime=NowFileTime), mode='w') 
# fileHandler = logging.FileHandler(filename='ZmZ.log'.format(NowFileTime=NowFileTime), mode='w') 
fileHandler.setFormatter(formatter)
fileHandler.setLevel('INFO')

logger.addHandler(cmdHandler)
logger.addHandler(fileHandler)