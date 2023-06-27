import os
import uuid
import json
import PySimpleGUIWeb as sg

sg.theme("Light Grey 4")

def Upload():
    path = os.getcwd() + "/scu" # 语录的路径
    if not os.path.exists(path):
        os.mkdir(path)
    JsonPath = "" # 留空
    SentencesFile = "" # 留空
    choose = values['-SentenceName-']
    if choose == "桑吉":
        JsonPath = "/root/senteces/sentences/a.json" # 语录文件
        os.system(f"cp -r {JsonPath} {path}/")
        SentencesFile = "a.json" # 更新后的语录文件名
    elif choose == "羽月":
        JsonPath = "/root/senteces/sentences/b.json"
        os.system(f"cp -r {JsonPath} {path}/")
        SentencesFile = "b.json"
    elif choose == "楠桐":
        author = values['-Author-'] # 获取作者
        JsonPath = "/root/senteces/sentences/c.json"
        os.system(f"cp -r {JsonPath} {path}/")
        SentencesFile = "c.json"
    else:
        window['-OutPut-'].update('该语录[' + values['-SentenceName-'] + ']不存在！', text_color="red")

    sentence = values['-Sentence-']
    item_dict = "" # 留空
    f = open(f"{path}/{SentencesFile}", 'r', encoding="utf-8") # 将语言文件写入缓存
    text = f.read() # 读取语言
    f.close() # 关闭语言文件
    content = json.loads(text) # 转为List，List中为字典
    id = len(content) + 1 # 获取字典位数并加1的方式自动更新id
    Uuid = str(uuid.uuid4()) # 基于随机数生成uuid，可能会有极小的概率重复
    if choose == "1":
        item_dict = {
    "id": f"{id}", # 新的id，通过此方式写入双引号
    "uuid": f"{Uuid}", # 新的uuid，通过此方式写入双引号
    "hitokoto": f"{sentence}", # 需要添加的语录将填入这里，通过此方式写入双引号
    "type": "a",
    "from": "资本家聚集地",
    "from_who": "桑吉Sage",
    "creator": "桑吉Sage",
    "creator_uid": "1",
    "reviewer": "1",
    "commit_from": "web",
    "created_at": "1626590063",
    "length": "19"
} # 需添加的对象
    elif choose == "2":
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
    elif choose == "3":
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

    with open(f"{path}/tmp/{SentencesFile}", 'w', encoding="utf-8") as JsonFile:
        json.dump(content, JsonFile, indent=4, ensure_ascii=False) # 打开并写入json中，保持4格缩进并避免中文乱码
    os.system(f"cp -r {path}/tmp/{SentencesFile} /scu/")

# Define the window's contents
layout = [[sg.Text("语录名称")],
          [sg.Input(key='-SentenceName-')],
          [sg.Text("语录作者")],
          [sg.Input(key='-Author-')],
          [sg.Text("语录内容")],
          [sg.Input(key='-Sentence-')],
          [sg.Button('上传语录', key='-Upload-', size=(8,1))],
          [sg.Text(size=(40,1), key='-OutPut-')]]

# Create the window
window = sg.Window('Nya-WSL | 语录上传系统v1.0.0', layout, web_port=5555, font=('萝莉体 第二版', 18, 'normal'))

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == '-Upload-':
        Upload()
    # Output a message to the window
    window['-OutPut-'].update('成功将' + values['-Author-'] + '说的' + values['-Sentence-'] + '上传至' + values['-SentenceName-'] + '语录')

# Finish up by removing from the screen
window.close()