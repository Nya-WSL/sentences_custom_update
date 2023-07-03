import os
import sys
import json
import uuid
import socket
from urllib import request
from ftplib import FTP, error_perm

url = "http://sentence.osttsstudio.ltd:9000/"

def UploadSentence(self):
    from scu.app import ScuNameInput, ScuAuthorInput, ScuSentenceInput
    global SentencesFile
    JsonUrl = "" # 留空
    SentencesFile = "" # 留空
    JsonName = ScuNameInput.value
    if JsonName == "桑吉":
        JsonUrl = url + "a.json" # 语录的获取url
        request.urlretrieve(JsonUrl,"a_local.json") # 下载语录到程序目录
        SentencesFile = "a.json" # 更新后的语录文件名，与服务器上的文件名保持一致
    elif JsonName == "羽月":
        JsonUrl = url + "b.json"
        request.urlretrieve(JsonUrl,"b_local.json")
        SentencesFile = "b.json"
    elif JsonName == "楠桐":
        JsonUrl = url + "c.json"
        request.urlretrieve(JsonUrl,"c_local.json")
        author = ScuAuthorInput.value # 获取作者
        SentencesFile = "c.json"
    else:
        SentenceNameError(self)
        return

    sentence = ScuSentenceInput.value
    item_dict = "" # 留空
    OpenJsonFile = "" # 留空
    if JsonName == "桑吉":
        if sentence == "":
            SentenceTextError(self)
            return
        OpenJsonFile = "a_local.json" # 与上方request的文件名一致
    if JsonName == "羽月":
        if sentence == "":
            SentenceTextError(self)
            return
        OpenJsonFile = "b_local.json"
    if JsonName == "楠桐":
        if sentence == "":
            SentenceTextError(self)
            return
        if author == "":
            SentenceAuthorError(self)
            return
        OpenJsonFile = "c_local.json"
    f = open(OpenJsonFile, 'r', encoding="utf-8") # 将语言文件写入缓存
    text = f.read() # 读取语言
    f.close() # 关闭语言文件
    content = json.loads(text) # 转为List，List中为字典
    id = len(content) + 1 # 获取字典位数并加1的方式自动更新id
    Uuid = str(uuid.uuid4()) # 基于随机数生成uuid，可能会有极小的概率重复
    if JsonName == "桑吉":
        item_dict = {
    "id": f"{id}", # 新的id，通过此方式写入双引号
    "uuid": f"{Uuid}", # 新的uuid，通过此方式写入双引号
    "hitokoto": f"{sentence}", # 需要添加的语录将填入这里，通过此方式写入双引号
    "type": "a",
    "from": "桑吉Sage",
    "from_who": "桑吉Sage",
    "creator": "桑吉Sage",
    "creator_uid": "1",
    "reviewer": "1",
    "commit_from": "web",
    "created_at": "1626590063",
    "length": "19"
} # 需添加的对象
    elif JsonName == "羽月":
        item_dict = {
    "id": f"{id}",
    "uuid": f"{Uuid}",
    "hitokoto": f"{sentence}",
    "type": "b",
    "from": "羽月ちい",
    "from_who": "羽月ちい",
    "creator": "羽月ちい",
    "creator_uid": "1",
    "reviewer": "1",
    "commit_from": "web",
    "created_at": "1626590063",
    "length": "19"
}
    elif JsonName == "楠桐":
        item_dict = {
    "id": f"{id}",
    "uuid": f"{Uuid}",
    "hitokoto": f"{sentence}",
    "type": "c",
    "from": f"{author}", # 填入作者，通过此方式写入双引号
    "from_who": f"{author}",
    "creator": f"{author}",
    "creator_uid": "1",
    "reviewer": "1",
    "commit_from": "web",
    "created_at": "1626590063",
    "length": "19"
}
    content.append(item_dict) # 将字典追加入列表

    with open(SentencesFile, 'w', encoding="utf-8") as JsonFile:
        json.dump(content, JsonFile, indent=4, ensure_ascii=False) # 打开并写入json中，保持4格缩进并避免中文乱码

    host = "150.158.171.157"
    port = 21
    username = ""
    password = ""

    ftp = FtpConnect(host, port, username, password)
    # 避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
    ftp.voidcmd('TYPE I')
    UploadFile(ftp, SentencesFile) # 上传文件
    ftp.close()
    if os.path.exists(OpenJsonFile):
        os.remove(OpenJsonFile)
    if os.path.exists(SentencesFile):
        os.remove(SentencesFile)
    UploadSuccess(self)

def FtpConnect(host, port, username, password):
    ftp = FTP()
    ftp.set_debuglevel(2) # 调试级别2
    ftp.encoding = 'utf-8' # 解决中文编码问题，默认是latin-1
    try:
        ftp.connect(host, port)
        ftp.login(username, password)
        print(ftp.getwelcome()) # 打印欢迎信息
    except(socket.error, socket.gaierror): # 连接错误
        ConnectError = print("ERROR: cannot connect [{}:{}]" .format(host, port))
        ConnectError = f"ERROR: cannot connect [{host}:{port}]"
        sys.exit(ConnectError)
    except error_perm: # 认证错误
        print("ERROR: user Authentication failed ")
        AuthError = "ERROR: user Authentication failed "
        sys.exit(AuthError)
    return ftp

def UploadFile(ftp, localpath):
    """
    上传文件
    :param ftp:
    :param SentencesFile:
    :param localpath:
    :return:
    """
    bufsize = 1024 # 缓冲区大小
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + SentencesFile, fp, bufsize)  # 上传文件
    fp.close()

def SentenceNameError(self):
    from scu.app import ScuMainWindow
    ScuMainWindow.error_dialog(
        "语录名称错误",
        "该语录不存在，请检查！"
    )

def SentenceTextError(self):
    from scu.app import ScuMainWindow
    ScuMainWindow.error_dialog(
        "语录内容错误",
        "上传内容为空，请检查！"
    )

def SentenceAuthorError(self):
    from scu.app import ScuMainWindow
    ScuMainWindow.error_dialog(
        "语录作者错误",
        "作者为空，请检查！"
    )

def UploadSuccess(self):
    from scu.app import ScuMainWindow, ScuNameInput, ScuAuthorInput, ScuSentenceInput
    if ScuAuthorInput.value == "":
        ScuMainWindow.info_dialog(
            "语录上传成功",
            f"已成功将'{ScuSentenceInput.value}'上传至'{ScuNameInput.value}语录'，如有任何问题请与我们联系，联系方式：support@nya-wsl.com",
)
    else:
        ScuMainWindow.info_dialog(
            "语录上传成功",
            f"已成功将'{ScuAuthorInput.value}'说的'{ScuSentenceInput.value}'上传至'{ScuNameInput.value}语录'，如有任何问题请与我们联系，联系方式：support@nya-wsl.com",
)