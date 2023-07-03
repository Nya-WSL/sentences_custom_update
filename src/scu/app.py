import os
import toga
import datetime
from toga.style import Pack
from scu.upload import UploadSentence
from toga.style.pack import COLUMN, ROW

WorkDir = "logs"
if not os.path.exists("logs"):
    os.mkdir(WorkDir)
# 错误处理
class LogPetion():
    def __init__(self):
        import traceback
        import logging
# logging的基本配置
        DebugTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 获取错误时间
        logging.basicConfig(
            filename=f'{WorkDir}/scu_debug_{DebugTime}.txt',              # 当前文件写入位置
            format='%(asctime)s %(levelname)s \n %(message)s',             # 格式化存储的日志格式
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
# 写入日志
        logging.debug(traceback.format_exc())

class scu(toga.App):
    try:
        def startup(self):
            global ScuNameInput
            global ScuAuthorInput
            global ScuSentenceInput
            global ScuMainWindow
            MainBox = toga.Box(style=Pack(direction=COLUMN))

            SentenceNameLabel = toga.Label(
                "语录名称：",
                style=Pack(padding=(0, 5))
            )
            self.NameInput = toga.TextInput(style=Pack(flex=1))
            ScuNameInput = self.NameInput

            SentenceAuthorLabel = toga.Label(
                "语录作者：",
                style=Pack(padding=(0, 5))
            )
            self.AuthorInput = toga.TextInput(style=Pack(flex=1))
            ScuAuthorInput = self.AuthorInput

            SentenceLabel = toga.Label(
                "语录内容：",
                style=Pack(padding=(0, 5))
            )
            self.SentenceInput = toga.TextInput(style=Pack(flex=1))
            ScuSentenceInput = self.SentenceInput

            SentenceNameBox = toga.Box(style=Pack(direction=ROW, padding=5))
            SentenceAuthorBox = toga.Box(style=Pack(direction=ROW, padding=5))
            SentenceBox = toga.Box(style=Pack(direction=ROW, padding=5))
            SentenceNameBox.add(SentenceNameLabel)
            SentenceNameBox.add(self.NameInput)
            SentenceAuthorBox.add(SentenceAuthorLabel)
            SentenceAuthorBox.add(self.AuthorInput)
            SentenceBox.add(SentenceLabel)
            SentenceBox.add(self.SentenceInput)

            button = toga.Button(
                "上传语录",
                on_press=UploadSentence,
                style=Pack(padding=5)
            )

            MainBox.add(SentenceNameBox)
            MainBox.add(SentenceAuthorBox)
            MainBox.add(SentenceBox)
            MainBox.add(button)

            self.main_window = toga.MainWindow(title="Nya-WSL | 语录上传系统v" + self.version, size=(400, 300))
            self.main_window.content = MainBox
            self.main_window.show()
            ScuMainWindow = self.main_window
            return self
    except:
        LogPetion()

def main():
    return scu()