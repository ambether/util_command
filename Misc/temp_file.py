from    tempfile   import TemporaryFile
from    subprocess import Popen
import  subprocess

'''
data = ''
with TemporaryFile('w+t') as f:
    line = input('>>> ').strip()
    running = True
    while running:
        if line == 'x':
            running = False
            break
        f.write(line + '\n')
        line = input('>>> ').strip()
    data = f.read()
print(data)
'''

p = Popen('send_stdout.py', shell=True, stdout=subprocess.PIPE)
f = TemporaryFile('w+t')
f.write(p.stdout.read().decode('utf-8'))

data = f.read()
f.close()
print(data)

