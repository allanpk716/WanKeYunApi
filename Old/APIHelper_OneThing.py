# -*- coding: utf-8 -*-
import requests
import json
from urllib.parse import urljoin
import random
import ipaddress

appVersion = "1.6.2"
apiAccountUrl = "https://account.onethingpcs.com"
apiControlUrl = "https://control.onethingpcs.com"
apiRemoteDlUrl = "https://control-remotedl.onethingpcs.com"

# MD5函数
def md5(s):
    import hashlib
    return hashlib.md5(s.encode('utf-8')).hexdigest().lower()

# 获取pwd值（密码MD5后加密再取MD5值）
def GetPwd(passwd):
    s = md5(passwd)
    s = s[0:2] + s[8] + s[3:8] + s[2] +s[9:17] + s[27] + s[18:27] + s[17] + s[28:]
    return md5(s)

# 获取sign值
def GetSign(body, k=''):
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

nowIp = rip()

# 登陆
def Login(phone, userPwd, deviceid_phone, imeiId):
    try:
        headers = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            "cache-control": "no-cache"
        }
        pwd = GetPwd(userPwd)
        body = dict(deviceid = deviceid_phone, 
                    imeiid = imeiId, 
                    phone = phone, 
                    pwd = pwd, 
                    account_type = '4')
        sign, nouse = GetSign(body)
        body = dict(deviceid = deviceid_phone, imeiid = imeiId, phone = phone, pwd = pwd, account_type = '4', sign = sign)
        nowUrl = apiAccountUrl + '/user/login?appversion={appVersion}'.format(appVersion=appVersion)
        cookies = None
        r = requests.post(url = nowUrl, data = body, verify = False, headers = headers, cookies = cookies, timeout = 10)
        if r.ok == False:
            return False, r.reason, None

        sessionid = r.cookies.get('sessionid')
        userid = r.cookies.get('userid')

        return True, sessionid, userid
    except Exception as ex:
        return False, str(ex), None

# 获取设备信息
def ListPeer(sessionid, userid):
    try:
        nowHeader = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            'cache-control': "no-cache"
        }
        body = {
            'X-LICENCE-PUB' : '1',
            "appversion" : appVersion,
            'ct' : '2',
            'v' : '3',
        }
        sign, nouse = GetSign(body, sessionid)
        nowUrl = apiControlUrl + '/listPeer?X-LICENCE-PUB=1&appversion={appVersion}&ct=2&v=3&sign={sign}'.format(appVersion=appVersion, sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid)
        r = requests.get(url=nowUrl, headers=nowHeader, cookies=cookies, timeout=MytimeOut)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']

        devicesInfo = tmpJson['result'][1]['devices']
        
        return True, devicesInfo
    except Exception as ex:
        return False, str(ex)

# 获取硬盘信息
def GetUSBInfo(mydeviceId, sessionid, userid):
    try:
        headers = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            # 'Content-Type': 'text/plain'
            # 'Content-Type': 'application/json'
        }

        body = {
            'appversion' : appVersion,
            'ct' : '1',
            'deviceid' : mydeviceId,
            'v' : '1'
        }
        sign, signInput = GetSign(body, sessionid)
        requestUrl = apiControlUrl  + "/getUSBInfo?{signInput}sign={sign}".format(signInput=signInput, sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid) # , origin='1'
        r = requests.get(url=requestUrl, headers=headers, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']
        return True, tmpJson
    except Exception as ex:
        return False, str(ex)

# 解析下载地址
def UrlResolve(mypid, sessionid, userid, dl_url):
    try:
        headers = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            # 'Content-Type': 'text/plain'
            'Content-Type': 'application/json'
        }
        j_url = {
            'url' : dl_url
        }
        body = json.dumps(j_url)
        requestUrl = apiRemoteDlUrl  + "/urlResolve?pid={mypid}&v=1".format(mypid=mypid)
        cookies = dict(sessionid=sessionid, userid=userid) # , origin='1'
        r = requests.post(url=requestUrl, data=body, headers=headers, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, r.msg
        return True, tmpJson['msg']
    except Exception as ex:
        return False, str(ex)

#    JobList:
#       OneJob = {
#            "filesize":filesize,
#            "name": filename,
#            "url" : url,
#       }
def CreateTask(mypid, sessionid, userid, JobList, remoteLocation):
    try:
        headers = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            'Content-Type': 'application/json'
        }

        tempList = []
        for OneJob in JobList:        
            tempList.append(OneJob)
            
        data = {
            'path': remoteLocation,
            'tasks': tempList
        }

        body = json.dumps(data)

        requestUrl = apiRemoteDlUrl  + "/createTask?pid={mypid}&v=2&ct=32".format(mypid=mypid)
        cookies = dict(sessionid=sessionid, userid=userid) # , origin='1'
        r = requests.post(url=requestUrl, data=body, headers=headers, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']
        
        return True, tmpJson
        
    except Exception as ex:
        False, ex

def RemoteDlLogin(mypid, sessionid, userid):
    try:
        nowHeader = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            'cache-control': "no-cache"
        }
        body = {
            "pid" : mypid,
            'v' : '1',
            'ct' : '32',
        }
        sign, nouse = GetSign(body, sessionid)
        nowUrl = apiRemoteDlUrl + '/login?' +  nouse + 'sign={sign}'    \
                                        .format(
                                            # mypid=mypid, 
                                            sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid)
        r = requests.get(url=nowUrl, headers=nowHeader, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']
        
        return True, tmpJson
   
    except Exception as ex:
        False, ex

# 获取下载列表，有效        0  
def GetRemoteDlInfo(mypid, sessionid, userid, strType):
    try:
        nowHeader = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            'cache-control': "no-cache"
        }
        body = {
            "pid" : mypid,
            'v' : '2',
            'ct' : '32',
            'pos' : '0',
            'number' : '100',
            'type' : strType,
            'needUrl' : '0',
        }
        sign, nouse = GetSign(body, sessionid)
        # nowUrl = apiRemoteDlUrl + '/list?ct=32&needUrl=0&number=100&pid={mypid}&pos=0&type={strType}&v=2&sign={sign}'    \
        nowUrl = apiRemoteDlUrl + '/list?' + nouse +  'sign={sign}'    \
                                        .format(
                                            # mypid=mypid, 
                                            # strType=strType, 
                                            sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid)
        r = requests.get(url=nowUrl, headers=nowHeader, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']
        
        return True, tmpJson
   
    except Exception as ex:
        False, ex

# 有效
def StartRemoteDl(mypid, sessionid, userid, taskid):
    try:
        nowHeader = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            'cache-control': "no-cache"
        }
        body = {
            "pid" : mypid,
            'v' : '1',
            'ct' : '32',
            'tasks' : taskid + "_9",
        }
        sign, nouse = GetSign(body, sessionid)
        # nowUrl = apiRemoteDlUrl + '/start?ct=32&pid={mypid}&tasks={taskid}&v=1&sign={sign}'    \
        nowUrl = apiRemoteDlUrl + '/start?' + nouse + 'sign={sign}'    \
                                        .format(
                                            # mypid=mypid, 
                                            # taskid=taskid, 
                                            sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid)
        r = requests.get(url=nowUrl, headers=nowHeader, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']
        
        return True, tmpJson
   
    except Exception as ex:
        False, ex

# 有效
def RestoreRemoteDl(mypid, sessionid, userid, taskid):
    try:
        nowHeader = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            'cache-control': "no-cache"
        }
        body = {
            "pid" : mypid,
            'v' : '1',
            'ct' : '32',
            'tasks' : taskid + "_9",
        }
        sign, nouse = GetSign(body, sessionid)
        # nowUrl = apiRemoteDlUrl + '/restore?ct=32&pid={mypid}&tasks={taskid}&v=1&sign={sign}'    \
        nowUrl = apiRemoteDlUrl + '/restore?' + nouse + 'sign={sign}'    \
                                        .format(
                                            # mypid=mypid, 
                                            # taskid=taskid, 
                                            sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid)
        r = requests.get(url=nowUrl, headers=nowHeader, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']
        
        return True, tmpJson
   
    except Exception as ex:
        False, ex

# 暂停，有效
def PauseRemoteDl(mypid, sessionid, userid, taskid):
    try:
        nowHeader = {
            'user-agent': "Mozilla/5.0",
            'Proxy-Client-IP' : nowIp,
            'cache-control': "no-cache"
        }
        body = {
            "pid" : mypid,
            'v' : '1',
            'ct' : '32',
            'tasks' : taskid + "_9",
        }
        sign, nouse = GetSign(body, sessionid)
        # nowUrl = apiRemoteDlUrl + '/pause?ct=32&pid={mypid}&tasks={taskid}&v=1&sign={sign}'    \
        nowUrl = apiRemoteDlUrl + '/pause?' + nouse +'sign={sign}'    \
                                        .format(
                                            # mypid=mypid, 
                                            # taskid=taskid, 
                                            sign=sign)
        cookies = dict(sessionid=sessionid, userid=userid)
        r = requests.get(url=nowUrl, headers=nowHeader, cookies=cookies, timeout=10)
        if r.ok == False:
            return False, r.reason
        tmpJson = r.json()
        if tmpJson['rtn'] != 0:
            return False, tmpJson['msg']
        
        return True, tmpJson
   
    except Exception as ex:
        False, ex