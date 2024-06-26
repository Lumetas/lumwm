
import os
import subprocess
import json
import sys

# Объявление стандартных переменных путей
home = os.path.expanduser('~')
path_lumwmc_str = home + "/lumwm_modules/modules_data/liblumwmc"
path_lumwmc = [path_lumwmc_str]


# Обявление вспомогательных функций
def system(arr):
    return subprocess.run(arr, capture_output=True).stdout.decode().strip().strip('\n')
def xdotool(arr):
    return system(['xdotool'] + arr)
def lumwmc(str):
    return system(path_lumwmc + [str])
def kill(pid):
    system(['kill', pid])



if (len(sys.argv) >= 3):
    argument2 = sys.argv[2]
else:
    argument2 = False




# Функция переключения рабочих столов
def change_workspace(new_space):
    f = open(f"{home}/.config/lumwm/data/workspace.json", 'r')
    file = f.read()
    f.close()
    obj = json.loads(file)
    current = obj["current"]
    windows = lumwmc("showed_windows").split('\n')
    obj[current] = windows
    for window in windows:
        #print(window)
        os.system(f"xdotool windowunmap {window}")
    obj['current'] = new_space
    if (new_space in obj.keys()):
        windows = obj[new_space]
        for window in windows:
            os.system(f"xdotool windowmap {window}")
    f = open(f"{home}/.config/lumwm/data/workspace.json", "w")
    a = json.dumps(obj)
    f.write(a)
    f.close()


# Функция для изменения фокуса окна
def focus_window_to(number):
    windows = lumwmc("showed_windows").split('\n')
    print(windows)
    if (len(windows) == 1 and windows[0] == ''):
        exit()
    focus_window = lumwmc("focus_window_id")
    if focus_window in windows:
        index = windows.index(focus_window) + 1
        new_index = index + number
        if len(windows) < new_index:
            new_index = new_index % len(windows)
        if new_index < 0:
            new_index = new_index % len(windows)
            new_index = len(windows) - new_index
        if new_index == 0:
            new_index = len(windows)

        xdotool(["windowfocus", windows[new_index - 1]])

    else:
        xdotool(["windowfocus", windows[0]])

# Переключение рабочих столов
if (len(sys.argv) > 1 and sys.argv[1] == 'go_to_workspace'):
    change_workspace(sys.argv[2])
    focus_window_to(0)


