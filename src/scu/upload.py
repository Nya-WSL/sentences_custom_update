import os
import json
import uuid

def UploadSentence(self):
    from scu.app import ScuNameInput, ScuAuthorInput, ScuSentenceInput
    testText(self)
    SentencesFile = "" # 留空
    author = ScuAuthorInput.value # 获取作者
    JsonName = ScuNameInput.value
    sentence = ScuSentenceInput.value
    if JsonName in ["桑吉","桑吉语录"]:
        if sentence == "":
            SentenceTextError(self)
            return
        SentencesFile = "a.json"
    elif JsonName in ["羽月","羽月语录"]:
        if sentence == "":
            SentenceTextError(self)
            return
        SentencesFile = "b.json"
    elif JsonName in ["楠桐","楠桐语录"]:
        if sentence == "":
            SentenceTextError(self)
            return
        if author == "":
            SentenceAuthorError(self)
            return
        SentencesFile = "c.json"
    else:
        SentenceNameError(self)
        return

    OpenFile = "http://sentence.osttsstudio.ltd:9000/" + SentencesFile
    item_dict = "" # 留空
    f = open(OpenFile, 'r', encoding="utf-8") # 将语言文件写入缓存
    text = f.read() # 读取语言
    f.close() # 关闭语言文件
    content = json.loads(text) # 转为List，List中为字典
    id = len(content) + 1 # 获取字典位数并加1的方式自动更新id
    Uuid = str(uuid.uuid4()) # 基于随机数生成uuid，可能会有极小的概率重复
    if JsonName in ["桑吉","桑吉语录"]:
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
    elif JsonName in ["羽月","羽月语录"]:
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
    elif JsonName in ["楠桐","楠桐语录"]:
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

    with open(OpenFile, 'w', encoding="utf-8") as JsonFile:
        json.dump(content, JsonFile, indent=4, ensure_ascii=False) # 打开并写入json中，保持4格缩进并避免中文乱码
    
    UploadSuccess(self)

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

def testText(self):
    from scu.app import ScuMainWindow
    test = os.getcwd()
    ScuMainWindow.info_dialog("test", f"{test}")