# -*- coding: utf-8 -*-

appVersion="2.6.0"

apiAccountUrl_root = "https://account.onethingpcs.com/"
loginUrl = apiAccountUrl_root+"user/login?appversion={0}".format(appVersion)

apiControlUrl_root = "https://control.onethingpcs.com/"
listPeerURL = apiControlUrl_root + "listPeer?"
peerUSBInfoUrl = apiControlUrl_root + "getUSBInfo?"

apiRemoteDlUrl_root = "https://control-remotedl.onethingpcs.com/"
urlResolveUrl = apiRemoteDlUrl_root + "urlResolve?"
loginRmoteDlUrl = apiRemoteDlUrl_root + "login?"
listRemoteDlInfoUrl = apiRemoteDlUrl_root + "list?"
createTaskUrl = apiRemoteDlUrl_root + "createTask?"
startTaskUrl = apiRemoteDlUrl_root + "start?"
pauseTaskUrl = apiRemoteDlUrl_root + "pause?"
delTaskUrl = apiRemoteDlUrl_root + "del?"

