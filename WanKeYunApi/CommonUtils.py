# -*- coding: utf-8 -*-
import os
import hashlib
import random
import ipaddress
import json
import codecs
import requests

userInfoFileName = 'userInfo.json'
cookieFileName = "cookies.txt"

# MD5函数
def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest().lower()

# 获取pwd值（密码MD5后加密再取MD5值）
def Get_Pwd(passwd):
    s = md5(passwd)
    s = s[0:2] + s[8] + s[3:8] + s[2] +s[9:17] + s[27] + s[18:27] + s[17] + s[28:]
    return md5(s)

# 获取sign值
def Get_Sign(body, k=''):
    l = []
    while len(body) != 0:
        v = body.popitem()
        l.append(v[0]+ '=' + v[1])
    l.sort()
    t = 0
    s = ''
    while t != len(l):
        s = s + l[t] + '&'
        t = t+1
    signInput = s + 'key=' + k
    sign = md5(signInput)
    return sign, s

# random ip
def rip():
	ip = '.'.join([str(int(''.join(
	[str(random.randint(0, 2)), 
	 str(random.randint(0, 5)), 
	 str(random.randint(0, 5))]
	))) 
	for _ in range(4)])
	if ipaddress.IPv4Address(ip).is_global:
		return ip
	else:
		return rip()

# 构建发送的 body
def GenerateBody(**kwargs):
    result = {}
    for key in kwargs.keys():
        result[key] = kwargs[key]
    sign = Get_Sign(result)
    for key in kwargs.keys():
        result[key] = kwargs[key]
    result['sign'] = sign[0]
    return result

def Get_IMEI_MD5(s):
    return md5(s)[0:16]

def Get_Device_MD5(s):
    return md5(s)[:14]

def Get_Params(data, sessionid, is_get=False):
    temp =[]
    result = {}
    for key in data.keys():
        if key == "pwd":
            temp.append(key+"="+Get_Pwd(data["pwd"]))
            result[key] = Get_Pwd(data[key])
        else:
            temp.append(key+"="+data[key])
            result[key] = data[key]
    sign = Get_Sign(result,sessionid)
    sign = sign[0]
    gstr = '&'.join(temp)
    if gstr:
        gstr += "&"
    key = "key="+sessionid
    estr=gstr+key+"&"

    return estr+"sign="+ sign if not is_get else gstr +"sign=" + sign

def SaveUserInfo(userInfo):
    with codecs.open(userInfoFileName, 'w', 'utf-8') as outf:
        json.dump(userInfo, outf, ensure_ascii=False)
        outf.write('\n')

def LoadUserInfo():
    if os.path.exists(userInfoFileName) == False:
        return None
    userInfo = []
    with codecs.open(userInfoFileName, "r", "utf-8") as f:
        for line in f:
            dic = json.loads(line)
            userInfo.append(dic)
    return userInfo

def SaveCookie(session):
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    with open(cookieFileName, "w") as fp:
        json.dump(cookies, fp)

def LoadCookie():
    if os.path.exists(cookieFileName) == False:
        return None
    with open(cookieFileName, "r") as fp:
        load_cookies = json.load(fp)
    return requests.utils.cookiejar_from_dict(load_cookies)
