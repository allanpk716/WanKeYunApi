# -*- coding: utf-8 -*-

import json
from urllib.parse import urljoin

import requests

from . import Config, CommonUtils, LogHelper

requests.packages.urllib3.disable_warnings()

class WanKeYunApi:
    requestSession = requests.session()
    user_info = {}

    def __init__(self, defPath="/onecloud/tddownload"):
        self.nowIP = CommonUtils.rip()
        self.defaultPath = defPath
        self.requestSession.headers = {
            'user-agent': "MineCrafter3/{appVersion} (iPhone; iOS 12.4.1; Scale/3.00)".format(appVersion=Config.appVersion),
            'Proxy-Client-IP' : self.nowIP,
            "cache-control": "no-cache"
        }
    
    def SaveUserInfo(self):
        CommonUtils.SaveUserInfo(self.user_info)
    
    def LoadUserInfo(self):
        tmp = CommonUtils.LoadUserInfo()
        if tmp is None:
            return False
        self.user_info = tmp[0]
        return True

    def SaveCookie(self, result):
        # 保持cookie有效
        if result.cookies.get_dict():        
            self.requestSession.cookies.update(result.cookies)
        CommonUtils.SaveCookie(self.requestSession)

    def LoadCookie(self):
        tmp = CommonUtils.LoadCookie()
        if tmp is None:
            return False
        self.requestSession.cookies = tmp
        return True

    def ReCacheInfo(self):
        self.LoadCookie()
        self.LoadUserInfo()

    # 封装 Login，支持缓存登陆
    def LoginEx(self, user, passwd):
        # 先尝试读取缓存
        self.ReCacheInfo()
        # 尝试读取一次 Peer 信息，如果失败，那么就重新登陆
        if self.ListPeer() is False:
            LogHelper.logger.info("Need ReLogin.")
            if self.Login(user, passwd) is False:
                return False

            if self.ListPeer() is True:
                return True
            else:
                LogHelper.logger.info("LoginEx Error.")
                return False
        
        LogHelper.logger.info("Login From Cache Info Succeed.")
        return True
    
    # 登陆
    def Login(self, user, passwd):
        try:
            login_data = CommonUtils.GenerateBody(
                deviceid=CommonUtils.Get_Device_MD5(user), 
                imeiid=CommonUtils.Get_IMEI_MD5(user), 
                phone=user, 
                pwd=CommonUtils.Get_Pwd(passwd),
                account_type='4'
            )
            result = self.requestSession.post(Config.loginUrl, data=login_data, verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("iRet") == 0:
                    self.user_info["login"] = temp.get("data")
                    self.user_info["sessionid"] = self.requestSession.cookies.get("sessionid")
                    self.user_info["userid"] = self.requestSession.cookies.get("userid")
                    self.SaveCookie(result)
                    self.SaveUserInfo()
                    LogHelper.logger.info("Login Succeed.")
                    return True
                else:
                    LogHelper.logger.info("Login Failed iRet != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("Login Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("Login: {0}".format(error))
        return False
    
    def ListPeer(self):
        try:
            ListPeerDir = {
                'X-LICENCE-PUB':'1',
                'appversion':Config.appVersion, 
                'v':"2", 
                'ct':"9"
            }
            peer_data = CommonUtils.Get_Params(
                ListPeerDir,
                self.user_info.get("sessionid"), 
                True
            )
            result = self.requestSession.get(Config.listPeerURL + peer_data, verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    self.user_info["all_peer_info"] = temp.get("result")[1]
                    self.SaveCookie(result)
                    self.SaveUserInfo()
                    LogHelper.logger.info("ListPeer Succeed.")
                    return True
                else:
                    LogHelper.logger.info("ListPeer Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("ListPeer Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("ListPeer: {0}".format(error))
        return False
    
    # 获取所有端的设备信息
    def Get_PeerInfo(self, nums=0):  
        try:
            result = self.user_info.get("all_peer_info")
            if result:
                temp = result["devices"]
                if len(temp) > nums and nums >=0:
                    return temp[nums]
        except Exception as error:
            LogHelper.logger.error("Get_PeerInfo : {0}".format(error))
        return False
    
    # 获取任一对端的ID
    def Get_PeerID(self, nums = 0):  
        try:
            result = self.user_info.get("all_peer_info")
            if result:
                temp = result["devices"]
                if len(temp) > nums and nums >=0:
                    return temp[nums].get("peerid")
        except Exception as error:
            LogHelper.logger.error("Get_PeerID : {0}".format(error))
        return False
    
    # 获取任一对端的设备ID
    def Get_PeerDeviceID(self, nums = 0):  
        try:
            result = self.user_info.get("all_peer_info")
            if result:
                temp = result["devices"]
                if len(temp) > nums and nums >=0:
                    return temp[nums].get("device_id")
        except Exception as error:
            LogHelper.logger.error("Get_PeerDeviceID: {0}".format(error))
        return False
    
    # 获取硬盘信息
    def GetUSBInfo(self):
        try:
            usbInfoDir = {
                'X-LICENCE-PUB':'1',
                'appversion': Config.appVersion, 
                'v': "2", 
                'ct': "9",
                "deviceid" : self.Get_PeerDeviceID()
            }
            peer_data = CommonUtils.Get_Params(usbInfoDir, 
                                                self.user_info.get("sessionid"), 
                                                True
                                            )
            result = self.requestSession.get(Config.peerUSBInfoUrl + peer_data, verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    self.user_info["usb_info"] = temp.get("result")
                    self.SaveCookie(result)
                    self.SaveUserInfo()
                    LogHelper.logger.info("GetUSBInfo Succeed.")
                    return True
                else:
                    LogHelper.logger.info("GetUSBInfo Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("GetUSBInfo Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("GetUSBInfo: {0}".format(error))
        return False

    # 远程下载登陆
    def RemoteDlLogin(self):
        try:
            remote_dl_data = CommonUtils.Get_Params(dict(pid=self.Get_PeerID(), 
                                                        appversion=Config.appVersion, 
                                                        v="1", 
                                                        ct="32"
                                                    ),
                                                    self.user_info.get("sessionid"), 
                                                    True
            )
            result = self.requestSession.get(Config.loginRmoteDlUrl + remote_dl_data, verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    del temp["rtn"]
                    self.user_info["remote_download_login"] = temp
                    self.SaveCookie(result)
                    self.SaveUserInfo()
                    LogHelper.logger.info("RemoteDlLogin Succeed.")
                    return True
                else:
                    LogHelper.logger.info("RemoteDlLogin Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("RemoteDlLogin Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("RemoteDlLogin:{0}".format(error))
        return False

    # 获取对端远程下载列表
    def GetRemoteDlInfo(self):
        try:
            peerid = self.Get_PeerID()
            remote_dl_data = CommonUtils.Get_Params(dict(pid=peerid, 
                                                            # appversion=Config.appVersion, 
                                                            ct="31",
                                                            v="2", 
                                                            pos="0", 
                                                            number="100",
                                                            type="4",
                                                            needUrl="0"
                                                    ),
                                                    self.user_info.get("sessionid"), 
                                                    True
            )
            result = self.requestSession.get(Config.listRemoteDlInfoUrl + remote_dl_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    del temp["rtn"]
                    self.user_info["remote_download_list"] = temp
                    self.SaveCookie(result)
                    self.SaveUserInfo()
                    LogHelper.logger.info("GetRemoteDlInfo Succeed.")
                    return True
                else:
                    LogHelper.logger.info("GetRemoteDlInfo Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("GetRemoteDlInfo Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("GetRemoteDlInfo:{0}".format(error))
        return False

    # 解析下载地址
    def UrlResolve(self, dl_url): 
        try:
            post_data = {
                'url' : dl_url
            }
            result = self.requestSession.post(Config.urlResolveUrl+ "pid={0}&ct=31&v=1".format(self.Get_PeerID()), 
                                            data=post_data,
                                            verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    LogHelper.logger.info("UrlResolve Succeed.")
                    return True, temp
                else:
                    LogHelper.logger.info("UrlResolve Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("UrlResolve Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("UrlResolve: {0}".format(error))
        return False, None

    #-------------------------------------------------------------------------------------
    # 创建下载任务
    #    JobList:
    #       OneJob = {
    #            "filesize":filesize,
    #            "name": filename,
    #            "url" : url,
    #       }
    def CreateTasks(self, JobList, remoteLocation):
        try:
            peerid = self.Get_PeerID()
            tempList = []
            for OneJob in JobList:        
                tempList.append(OneJob)
            data = {
                'path': remoteLocation,
                'tasks': tempList
            }
            remote_dl_data = json.dumps(data)
            result = self.requestSession.post(Config.createTaskUrl + "pid={0}&v=1&ct=31".format(peerid),
                                                headers = {
                                                    "Content-Type": "application/json"
                                                }, 
                                                data=remote_dl_data
            )
            if result.status_code == 200:
                tempJson = result.json()
                if tempJson.get("rtn") == 0:
                    self.SaveCookie(result)
                    self.SaveUserInfo()
                    LogHelper.logger.info("CreateTask Succeed.")
                    return True, tempJson
                else:
                    LogHelper.logger.info("CreateTask Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("CreateTask Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("CreateTask:{0}".format(error))
        return False, None

    # 恢复任务下载
    def StartRemoteDl(self, taskid):
        try:
            peerid = self.Get_PeerID()
            UrlContent = Config.startTaskUrl + "pid={0}&ct=31&v=1&tasks={1}".format(peerid, taskid + '_9')
            result = self.requestSession.get(UrlContent, 
                                                headers = {
                                                    "Content-Type": "application/x-www-form-urlencoded"
                                                }, 
                                                verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    LogHelper.logger.info("StartRemoteDl Succeed.")
                    return True, temp
                else:
                    LogHelper.logger.info("StartRemoteDl Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("StartRemoteDl Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("StartRemoteDl: {0}".format(error))
        return False, None

    # 暂停任务下载
    def PauseRemoteDl(self, taskid):
        try:
            peerid = self.Get_PeerID()
            UrlContent = Config.pauseTaskUrl + "pid={0}&ct=31&v=1&tasks={1}".format(peerid, taskid + '_0')
            result = self.requestSession.get(UrlContent, 
                                                headers = {
                                                    "Content-Type": "application/x-www-form-urlencoded"
                                                }, 
                                                verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    LogHelper.logger.info("PauseRemoteDl Succeed.")
                    return True, temp
                else:
                    LogHelper.logger.info("PauseRemoteDl Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("PauseRemoteDl Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("PauseRemoteDl: {0}".format(error))
        return False, None

    # 暂停任务下载
    def DelRemoteDl(self, taskid):
        try:
            peerid = self.Get_PeerID()
            UrlContent = Config.pauseTaskUrl + "pid={0}&ct=31&v=1&tasks={1}&deleteFile=true&recycleTask=false".format(peerid, taskid + '_9')
            result = self.requestSession.get(UrlContent, 
                                                headers = {
                                                    "Content-Type": "application/x-www-form-urlencoded"
                                                }, 
                                                verify=False)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    LogHelper.logger.info("PauseRemoteDl Succeed.")
                    return True, temp
                else:
                    LogHelper.logger.info("DelRemoteDl Failed rtn != 0 : {0}".format(result.text))
            else:
                LogHelper.logger.info("DelRemoteDl Failed status_code : {0} -- {1}".format(result.status_code, result.reason))
        except Exception as error:
            LogHelper.logger.error("DelRemoteDl: {0}".format(error))
        return False, None
    
    #-------------------------------------------------------------------------------------
    #    JobList:
    #       OneJob = {
    #            "filesize":filesize,
    #            "name": filename,      这个名称最好是对应的，因为后面下载会以这个来命名
    #            "url" : url,
    #       }
    #   注意，这个函数下载的时候默认的是第一个硬盘，usb_info --> ['partitions'][0]
    def AddDownloadTasks(self, JobList, partitionId=0):
        try:
            partitionPath = self.user_info["usb_info"][1]['partitions'][partitionId]
            rootPath = partitionPath['path']
            remoteLocation = rootPath + self.defaultPath
            remoteLocation = remoteLocation.lower()
            # 总容量
            capacity = partitionPath['capacity']
            # 已使用
            used = partitionPath['used']
            # 剩余
            free2Use = int(capacity) - int(used)
            if free2Use <= 0:
                LogHelper.logger.warn("AddDownloadTasks: Disk {0} is Full".format(partitionId))
                return False
            # 当玩客云关机再开机的时候，需要恢复为下载完成的任务，也可以操作暂停正在下载的任务
            # 查询下载的任务列表，下载完毕的也在内，需要过滤
            nowDownloadingList = self.user_info["remote_download_list"]["tasks"]
            for oneTask in nowDownloadingList:
                iprogress = int(oneTask["progress"])
                if iprogress == 10000:
                    pass
                else:
                    self.StartRemoteDl(oneTask["id"])
            # 确认下载任务
            confirmJobList = []
            # 下载任务的总大小
            allDownloadFileSize = 0
            # 经过验证，重新构建一个有效的下载队列
            for oneJob in JobList:
                # 解析单个下载文件信息
                bok, mediaInfo = self.UrlResolve(oneJob['url'])
                if bok == False:
                    LogHelper.logger.warn("AddDownloadTasks: " + oneJob['name'] + ' False.')
                    continue
                taskInfo = mediaInfo['taskInfo']
                allDownloadFileSize = allDownloadFileSize + int(taskInfo['size'])
                # 如果解析出来的是 BT 任务，则需要填充一下结构，BT 任务不建议改名
                if len(mediaInfo.get("infohash")):
                    if 'size' in taskInfo == False:
                        LogHelper.logger.warn("AddDownloadTasks: " + oneJob['name'] + " Can't Find Size.")
                        continue
                    if 'name' in taskInfo and taskInfo['name'] == '':
                        LogHelper.logger.warn("AddDownloadTasks: " + oneJob['name'] + " Cant't Find Name By Url.")
                        continue
                    oneJob["filesize"] = taskInfo['size']
                    oneJob['name'] = taskInfo['name']
                    oneJob["infohash"]=mediaInfo["infohash"]
                    oneJob["url"]=taskInfo["url"]
                confirmJobList.append(oneJob)

            # 判断下载任务是否超过余量
            if allDownloadFileSize > free2Use:
                LogHelper.logger.warn("AddDownloadTasks: There's not enough space to download")
                return False
            # 提交下载任务
            bok, taskResultList = self.CreateTasks(confirmJobList, remoteLocation)
            if bok == False:
                return False
            
            for oneTask in taskResultList['tasks']:
                if oneTask['msg'] == 'repeat_task':
                    LogHelper.logger.warn('TaskExsit' + " -- " + oneTask['name'])
                    continue
                if oneTask['result'] != 0:
                    LogHelper.logger.warn('result != 0' + " -- " + oneTask['name'])
                    continue
                LogHelper.logger.info('AddedTask' + " -- " + oneTask['name'])

            LogHelper.logger.info("AddDownloadTasks Succeed.")
            return True
        except Exception as error:
            LogHelper.logger.error("AddDownloadTasks: {0}".format(error))
        return False
        