import os
f = open('pid.txt','w')
pid = os.getpid()
f.write(str(pid))
f.close()
i = 0
while True:
    print(i)
    i += 1    