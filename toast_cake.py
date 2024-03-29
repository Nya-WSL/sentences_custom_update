'''
Author: Nya-WSL
Copyright © 2024 by Nya-WSL All Rights Reserved. 
Date: 2024-02-25 19:18:52
LastEditors: 狐日泽
LastEditTime: 2024-03-06 13:58:10
'''

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg, ArgStr
from configs.path_config import DATA_PATH

import os
import json
import datetime

__zx_plugin_name__ = "画饼"
__plugin_usage__ = """
usage：
    不知道你更爱吃开发组画的饼还是自己给开发组画饼（bushi
    指令：
        开炉
        画饼 馅料
        出炉
""".strip()
__plugin_des__ = "谁不爱画饼呢（"
__plugin_cmd__ = ["画饼", "开炉"]
__plugin_version__ = 0.3
__plugin_author__ = "Nya-WSL"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["画饼", "开炉"],
}

cmd = on_command("画饼", priority=5, block=True)
check_cmd = on_command("开炉", priority=5, block=True)
del_cmd = on_command("出炉", priority=5, block=True)

ScuDataPath = DATA_PATH / "scu"
CakePath = ScuDataPath / "cake.json"

if not ScuDataPath.exists():
    os.mkdir(ScuDataPath)

if not os.path.exists(CakePath):
    with open(CakePath, "w", encoding="utf-8") as f:
        f.write(r"{}")

@cmd.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    if len(msg) < 1:
        await cmd.finish("请输入馅料!")
    else:
        with open(CakePath, "r", encoding="utf-8") as f:
            CakeData = json.loads(f.read())
        key = f"{(len(CakeData) + 1)},{event.group_id},{event.sender.nickname},{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        CakeData[key] = msg[0]
        with open(CakePath, "w", encoding="utf-8") as f:
            json.dump(CakeData, f, ensure_ascii=False, indent=4)
        await cmd.finish("新饼进炉辣!")

@check_cmd.handle()
async def _():
    with open(CakePath, "r", encoding="utf-8") as f:
        CakeData = json.loads(f.read())
    cake = []
    for key,value in CakeData.items():
        key = str(key).split(",")
        cake.append(f"{key[0]} | {value} | {key[2]} | {str(key[3]).split('_')[0]}")
    cake = str(cake).replace("'", "").replace("[", "").replace("]", "").replace(", ", "\n").replace("\"", "")
    await check_cmd.finish(f"""当前总画饼数：{len(CakeData)}

尚未出炉的饼：
{cake}""")

def get_key(d, value):
    return [k for k, v in d.items() if v == value]

with open(CakePath, "r", encoding="utf-8") as f:
    CakeData = json.loads(f.read())
    dict_values = str(CakeData.values()).replace("dict_values(['", "").replace("', '", "\n").replace("'])", "")

@del_cmd.got("flag", prompt=f"""请选择要出炉的饼:
{dict_values}""")
async def _(flag: str = ArgStr("flag")):
    with open(CakePath, "r", encoding="utf-8") as f:
        CakeData = json.loads(f.read())
    values = str(CakeData.values()).replace("dict_values(", "").replace(")", "")
    if flag in values:
        key = get_key(CakeData, flag)
        del_cake = CakeData.pop(str(key).replace("['", "").replace("']", ""), "不存在的饼")
        if del_cake != "不存在的饼":
            with open(CakePath, "w", encoding="utf-8") as f:
                json.dump(CakeData, f, ensure_ascii=False, indent=4)
            await del_cmd.finish(f"{del_cake}已出炉！")
        else:
            await del_cmd.finish(f"没画过的饼怎么出炉？")