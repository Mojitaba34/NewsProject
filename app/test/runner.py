import subprocess as s 

def killProcess(pid):
    s.Popen('TASKKILL /F /PID {0}'.format(pid),shell=True)

f = open('pid.txt','r')
da = f.read()
print(da)
killProcess(da)