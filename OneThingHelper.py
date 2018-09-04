# -*- coding: utf-8 -*-
import APIHelper_OneThing
#-------------------------------------------------------------------------------------
userPhone = '你的账号'
userPwd = '你的密码'
#-------------------------------------------------------------------------------------
# 虚拟出来的手机信息
# 16 位
deviceid_phone = '反正随机个16位就得了'
# 15 位
imeiId =   '同上15位'
#-------------------------------------------------------------------------------------
JobList = []
#-------------------------------------------------------------------------------------
# 可以指定 下载的路径，前面的盘符会在下面的代码补上去。
defaultPath = "/onecloud/tddownload"
#-------------------------------------------------------------------------------------
#    JobList:
#       OneJob = {
#            "filesize":filesize,
#            "name": filename,      这个名称最好是对应的，因为后面下载会以这个来命名
#            "url" : url,
#       }
def AddDownloadTask(userPhone, userPwd, deviceid_phone, imeiId, JobList, defaultPath, IsFilmFile = True):
    # 登录
    bok, sessionid, userid = APIHelper_OneThing.Login(userPhone, userPwd, deviceid_phone, imeiId)
    if bok == False:
        return False, "Error Login -- " + sessionid
    # 获取设备信息
    bok, devicesInfo = APIHelper_OneThing.ListPeer(sessionid, userid)
    if bok == False:
        return False, "Error ListPeer -- " + devicesInfo
    mypid = devicesInfo[0]['peerid']
    mydeviceId = devicesInfo[0]['device_id']
    # 获取硬盘信息
    bok, usbInfo = APIHelper_OneThing.GetUSBInfo(mydeviceId, sessionid, userid)
    if bok == False:
        return False, "Error GetUSBInfo -- " + usbInfo

    rootPath = usbInfo['result'][1]['partitions'][0]['path']
    # 总容量
    capacity = usbInfo['result'][1]['partitions'][0]['capacity']
    # 已使用
    used = usbInfo['result'][1]['partitions'][0]['used']
    # 剩余
    free2Use = int(capacity) - int(used)
    if free2Use <= 0:
        return False, "There's not enough space to download"

    # 查询有哪些任务，然后把失败、暂停的开始
    bok, dlInfo = APIHelper_OneThing.RemoteDlLogin(mypid, sessionid, userid)
    if bok == False:
        return False, "Error RemoteDlLogin -- " + dlInfo
    bok, dlInfo = APIHelper_OneThing.GetRemoteDlInfo(mypid, sessionid, userid, '0')
    if bok == False:
        return False, "Error GetRemoteDlInfo -- " + dlInfo
    for dl_one in dlInfo['tasks']:
        
        bok, dlState = APIHelper_OneThing.StartRemoteDl(mypid, sessionid, userid, dl_one['id'])
        if bok == False:
            print('恢复任务失败 -- ' + dl_one['name'])
            print(dlState)

    remoteLocation = rootPath + defaultPath

    remoteLocation = remoteLocation.lower()

    confirmJobList = []
    # 可以下载其他东西
    if IsFilmFile == True:
        # 经过验证，重新构建一个有效的下载队列
        
        for oneJob in JobList:
            # 解析单个下载文件信息
            bok, mediaInfo = APIHelper_OneThing.UrlResolve(mypid, sessionid, userid, oneJob['url'])
            if bok == False:
                print("Error UrlResolve -- " + mediaInfo)
                continue
            taskInfo = mediaInfo['taskInfo']
            if 'size' in taskInfo == False:
                print("Error UrlResolve -- Can't Read Size.")
                continue
            if 'name' in taskInfo and taskInfo['name'] == '':
                print("Error UrlResolve -- Cant't Find Job By Url.")
                continue

            oneJob["filesize"] = taskInfo['size']
            confirmJobList.append(oneJob)
    else:
        confirmJobList = JobList

    # 创建下载任务
    # mypid, sessionid, userid, 
    # JobList, remoteLocation
    bok, taskResultList = APIHelper_OneThing.CreateTask(mypid, sessionid, userid, 
                                        confirmJobList, remoteLocation)
    if bok == False:
        return False, "Error CreateTask -- " + taskResultList

    for oneTask in taskResultList['tasks']:
        if oneTask['msg'] == 'repeat_task':
            print('任务存在' + " -- " + oneTask['name'])
            continue
        if oneTask['result'] != 0:
            print('result != 0' + " -- " + oneTask['name'])
            continue

        print('任务添加成功.' + " -- " + oneTask['name'])

    return True, "Done."

# OneJob = {
#     "filesize": 0,
#     "name": '6a23cae9532b90a50d76101a688791f5edf1e716_ONE_PUNCH_MAN_01_12_OVA01_06_OAD_BDrip_BIG5_MP4_1280X720.torrent',
#     "url" : 'https://bt.agefans.com/torrent/6a23cae9532b90a50d76101a688791f5edf1e716_ONE_PUNCH_MAN_01_12_OVA01_06_OAD_BDrip_BIG5_MP4_1280X720.torrent?xxx=b8',
# }

# OneJob = {
#     "filesize": 0,
#     "name": '黄石.Yellowstone.2018.S01E07.中英字幕.WEB.720P-人人影视.mp4',
#     "url" : 'ed2k://|file|%E9%BB%84%E7%9F%B3.Yellowstone.2018.S01E07.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.WEB.720P-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|559753916|bdb7746c12f23558420a1bfd610e8bb5|h=xavxscmhtkwu4bl52jiqnmow6pa6ntdf|/',
# }

# OneJob2 = {
#     "filesize": 0,
#     "name": '黄石.Yellowstone.2018.S01E08.中英字幕.WEB.720P-人人影视.mp4',
#     "url" : 'ed2k://|file|%E9%BB%84%E7%9F%B3.Yellowstone.2018.S01E08.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.WEB.720P-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|472873520|c273bf00703b45225f2056393d6de87f|h=yq4vc2vndh2fnqdiwnhnqapwh7xcvlrw|/',
# }

# OneJob3 = {
#     "filesize": 0,
#     "name": '',
#     "url" : 'magnet:?xt=urn:btih:502351a0c2d1bd0eb2f6b29f1b2c93b03f5aabe5&tr=udp://9.rarbg.to:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=http://tr.cili001.com:8070/announce&tr=http://tracker.trackerfix.com:80/announce&tr=udp://open.demonii.com:1337&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://p4p.arenabg.com:1337&tr=wss://tracker.openwebtorrent.com&tr=wss://tracker.btorrent.xyz&tr=wss://tracker.fastcast.nz',
# }
#JobList.append(OneJob)
#JobList.append(OneJob2)
# JobList.append(OneJob3)

# bok, Error = AddDownloadTask(userPhone, userPwd, deviceid_phone, imeiId, JobList, defaultPath)
#if bok == False:
 #   print(Error)
#print('All Done.')