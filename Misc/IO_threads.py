from subprocess import Popen
import subprocess
from time import sleep
from sys import stdin, stdout
from queue import Queue
from threading import Thread, Event
from Menu import SimpleMenu

#Sentinel:  A generic object to pass into the queue to tell the threads to stop.
_sentinel = object()

def Main():
    menu = SimpleMenu()
    q = Queue()
    p = Producer(menu)
    c = Consumer()

    t1 = Thread(target=p.go, args=(q,))
    t2 = Thread(target=c.go, args=(q,))
    t1.start()
    t2.start()
    
class Producer:
    def __init__(self, menu):
        
        self.scriptName = menu.runMenu()
        print(self.scriptName, '<<<')
        
    def go(self, out_q, args=None):
        if args is not None:
            cmd = self.scriptName + ' ' + ' '.join(args)
        else:
            cmd = self.scriptName
        #print(cmd)
        #process_Producer = Popen(cmd, shell=True, stdout=stdout, stderr=subprocess.PIPE)
        process_Producer = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=stdout)
        while True:
            line = process_Producer.stdout.readlines()
            for l in line:
                evt = Event()
                out_q.put((l, evt))

            if process_Producer.poll() is not None:
                break
            evt.wait()
        out_q.put((_sentinel, evt))

            

 
class Consumer:
    def __init__(self):
        pass
    
    def go(self, in_q):
        c_ticks = 0
        _running = True
        while _running is True:
            data, evt = in_q.get()
            c_ticks += 1
            evt.set()
            if data is _sentinel:
                in_q.put(_sentinel)
                _running = False
                break
            if data is not '':
                print(data)
        print(str(c_ticks))
Main()



