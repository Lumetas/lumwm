import subprocess

def system(arr):
    return subprocess.run(arr, capture_output=True).stdout.decode().strip().strip('\n')
def xdotool(arr):
    return system(['xdotool'] + arr)
def showed_windows():
    return xdotool(['search', '--onlyvisible', '.']).split('\n')



works = showed_windows()
while 1:
    neworks = showed_windows()
    if works != neworks:
        if neworks == ['']: continue
        lastindex = neworks[len(neworks) - 1]
        xdotool(["windowfocus", lastindex])
        works = neworks
