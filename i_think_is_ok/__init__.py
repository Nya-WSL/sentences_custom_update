'''
Author: Nya-WSL
Copyright © 2023 by Nya-WSL All Rights Reserved. 
Date: 2023-09-25 21:46:47
LastEditors: 狐日泽
LastEditTime: 2023-10-28 15:31:05
'''
from nonebot import on_keyword, on_message
from services.log import logger
from nonebot.adapters.onebot.v11 import MessageEvent
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
from utils.utils import get_message_text
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from pathlib import Path
import os
import gc
import re
import json
import random
import fnmatch

__zx_plugin_name__ = "我觉得行"
__plugin_cmd__ = ["我觉得行"]
__plugin_version__ = 0.1
__plugin_author__ = "Nya-WSL"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["楠桐语录"],
}
__plugin_type__ = ("语录", 1)
__plugin_usage__ = """
usage：
    A：我觉得行
    bot：你行不了一点
    
install：
    只有group_list.json中存在的群才会触发，该文件初次运行将会自动生成
    除了我觉得行功能以外，其他用户限定功能发送人qq号或者id需要存在于user_list.json中相关的键的值（值可以是列表指定多个用户，也可以是字符串指定单个用户）才能触发
    打断复读功能仅受group_list限制不受用户限制
""".strip()

class Fudu:
    def __init__(self):
        self.data = {}

    def append(self, key, content):
        self._create(key)
        self.data[key]["data"].append(content)

    def clear(self, key):
        self._create(key)
        self.data[key]["data"] = []
        self.data[key]["is_repeater"] = False

    def size(self, key) -> int:
        self._create(key)
        return len(self.data[key]["data"])

    def check(self, key, content) -> bool:
        self._create(key)
        return self.data[key]["data"][0] == content

    def _create(self, key):
        if self.data.get(key) is None:
            self.data[key] = {"is_repeater": False, "data": []}

_fudu_list = Fudu()

send_img = on_keyword({"yhm", "樱花妹", "我觉得行"}, priority=5, block=True)
fudu = on_message(permission=GROUP, priority=999)

ImagePath = IMAGE_PATH / "scu/easter_egg"
ResourcesPath = Path() / "custom_plugins" / "i_think_is_ok"
ImgPath = ResourcesPath / "img"
GroupListPath = ResourcesPath / "group_list.json"
UserListPath = ResourcesPath / "user_list.json"

if not os.path.exists(ImagePath):
    os.mkdir(ImagePath)
    os.system(f"cp -rf {ImgPath}/* {ImagePath}")

if not GroupListPath.exists():
    with open(GroupListPath, "w", encoding="utf-8") as gl:
        gl.write(r"[]")

if not UserListPath.exists():
    with open(UserListPath, "w", encoding="utf-8") as ul:
        UserList = {
        "yhm": ["0000000000"],
        "example": "example"
}
        json.dump(UserList, ul, ensure_ascii=False, indent=4)

@send_img.handle()
async def _(event: MessageEvent):
    with open(GroupListPath, "r", encoding="utf-8") as gl:
        GroupList = json.load(gl)
    with open(UserListPath, "r", encoding="utf-8") as ul:
        UserList = json.load(ul)
    print(UserList)
    if f"{event.group_id}" in GroupList:
        # 用户限定功能1
        if f"{event.user_id}" in UserList["yhm"]:
            if re.search("yhm", str(event.message)) or re.search("樱花妹", str(event.message)):
                ImgList = fnmatch.filter(os.listdir(ImagePath), "asahi*.*")
                RandomImg = random.choice(ImgList)
                result = image(ImagePath / RandomImg)
                await send_img.send(result)
                flush = gc.collect()
                print(f"已成功清理内存：{flush}")
        # 全局功能，不限用户
        if f"{event.message}" == "我觉得行":
            length = len(os.listdir(ImagePath))
            if length == 0:
                logger.warning(f"彩蛋图库为空，调用取消！")
                await send_img.finish("哥们没活了呜呜呜")
            result = image("scu/easter_egg/" + "1.jpg")
            await send_img.send(result)
            flush = gc.collect()
            print(f"已成功清理内存：{flush}")

@fudu.handle()
async def _(event: GroupMessageEvent):
    with open(GroupListPath, "r", encoding="utf-8") as gl:
        GroupList = json.load(gl)
    if f"{event.group_id}" in GroupList:
        if event.is_tome():
            return
        msg = get_message_text(event.json())
        if not msg:
            return
        add_msg = msg + "|-|"
        if _fudu_list.size(event.group_id) == 0:
            _fudu_list.append(event.group_id, add_msg)
        elif _fudu_list.check(event.group_id, add_msg):
            _fudu_list.append(event.group_id, add_msg)
        else:
            _fudu_list.clear(event.group_id)
            _fudu_list.append(event.group_id, add_msg)
        if _fudu_list.size(event.group_id) >= 2:
            _fudu_list.clear(event.group_id)
            if random.random() < 0.7:
                await fudu.finish(msg)
            else:
                await fudu.finish(image("scu/easter_egg/" + "fudu.jpg"))