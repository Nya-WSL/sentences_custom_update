import PySimpleGUIWeb as sg

def Upload():
    print()

# Define the window's contents
layout = [[sg.Text("语录名称")],
          [sg.Input(key='-SentenceName-')],
          [sg.Text("语录作者")],
          [sg.Input(key='-SentenceAuthor-')],
          [sg.Text("语录内容")],
          [sg.Input(key='-Sentence-')],
          [sg.Button('上传语录', key='-Upload-')],
          [sg.Text(size=(40,1), key='-SentenceText-')]]

# Create the window
window = sg.Window('Nya-WSL | 语录上传系统', layout, web_port=5555)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == '-Upload-':
        Upload()
    # Output a message to the window
    window['-SentenceText-'].update('成功将' + values['-SentenceAuthor-'] + '说的' + values['-Sentence-'] + '上传至' + values['-SentenceName-'] + '语录')

# Finish up by removing from the screen
window.close()