# -*- coding: utf-8 -*-
import WanKeYunApi

def main():
    onething = WanKeYunApi.WanKeYunApi()
    bok = onething.LoginEx(user="你的账号",passwd="你的密码")
    if bok is False:
        return
    bok = onething.GetUSBInfo()
    if bok is False:
        return
    bok = onething.RemoteDlLogin()
    if bok is False:
        return
    bok = onething.GetRemoteDlInfo()
    if bok is False:
        return
    # --------------------------------------------------------------------------------
    # bok, mediaInfo = onething.UrlResolve('ed2k://|file|%E9%BB%84%E7%9F%B3.Yellowstone.2018.S01E07.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.WEB.720P-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|559753916|bdb7746c12f23558420a1bfd610e8bb5|h=xavxscmhtkwu4bl52jiqnmow6pa6ntdf|/')
    # --------------------------------------------------------------------------------
    JobList = []
    OneJob = {
        "filesize": 0,
        "name": '黄石.Yellowstone.2018.S01E07.中英字幕.WEB.720P-人人影视.mp4',
        "url" : 'ed2k://|file|%E9%BB%84%E7%9F%B3.Yellowstone.2018.S01E07.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.WEB.720P-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|559753916|bdb7746c12f23558420a1bfd610e8bb5|h=xavxscmhtkwu4bl52jiqnmow6pa6ntdf|/',
    }
    OneJob2 = {
        "filesize": 0,
        "name": '黄石.Yellowstone.2018.S01E08.中英字幕.WEB.720P-人人影视.mp4',
        "url" : 'ed2k://|file|%E9%BB%84%E7%9F%B3.Yellowstone.2018.S01E08.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.WEB.720P-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|472873520|c273bf00703b45225f2056393d6de87f|h=yq4vc2vndh2fnqdiwnhnqapwh7xcvlrw|/',
    }
    OneJob3 = {
        "filesize": 0,
        # "name": '【幻櫻字幕組】【一拳超人 第二季 ONE PUNCH MAN S2】【OVA】【02】【BIG5_MP4】【1280X720】.mp4',
        "name": '123.mp4',
        "url" : "magnet:?xt=urn:btih:UK32AE3T2R3UOBAPDVZJ6W35T7DRSFGJ&dn=&tr=http%3A%2F%2F104.238.198.186%3A8000%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.prq.to%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=https%3A%2F%2Ft-115.rhcloud.com%2Fonly_for_ylbud&tr=http%3A%2F%2Ftracker1.itzmx.com%3A8080%2Fannounce&tr=http%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker1.itzmx.com%3A8080%2Fannounce&tr=udp%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce"
    }
    JobList.append(OneJob)
    JobList.append(OneJob2)
    JobList.append(OneJob3)
    # --------------------------------------------------------------------------------
    # 创建批量下载任务示例，原生，需要自己填入，需要下载到那个磁盘
    # 一般就是磁盘 0
    # partitionID = 0
    # rootPath = onething.user_info["usb_info"][1]['partitions'][partitionID]['path']
    # remoteLocation = rootPath + self.defaultPath
    # remoteLocation = remoteLocation.lower()
    # onething.CreateTasks(JobList, remoteLocation)
    # --------------------------------------------------------------------------------
    # 当玩客云关机再开机的时候，需要恢复为下载完成的任务，也可以操作暂停正在下载的任务
    # 查询下载的任务列表，下载完毕的也在内，需要过滤
    # nowDownloadingList = onething.user_info["remote_download_list"]["tasks"]
    # for oneTask in nowDownloadingList:
    #     iprogress = int(oneTask["progress"])
    #     if iprogress == 10000:
    #         pass
    #     else:
    #         # onething.StartRemoteDl(oneTask["id"])
    #         onething.PauseRemoteDl(oneTask["id"])
    # --------------------------------------------------------------------------------
    # 创建批量下载任务，扩展，会判断
    onething.AddDownloadTasks(JobList)
    # --------------------------------------------------------------------------------
    print("Done.")

if __name__ == "__main__":
    main()
