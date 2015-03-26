'''
========================
==  Catch Error       ==
========================
==  3/17/2015         ==
==  Author: @dem4ply  ==
========================
'''

from time import localtime

def CatchErr(func, *args):
    try:
        if args:
            return func(*args)
        else:
            return func()
    except Exception as e:
        t = localtime()
        t_h = str(t[3])
        t_m = str(t[4])
        t_s = str(t[5])
            
        t_l = [t_h, t_m, t_s]
        
        for t_i in t_l:
            if len(t_i) < 2:
                t_l[t_l.index(t_i)] = str('0' + t_i)
        txt = '[{0}:{1}:{2}]'.format(
            t_l[0],
            t_l[1],
            t_l[2]
            )
        f = open('err.log', 'a')
        f.write(txt + '\t' + str(e) + '\n\n')
        f.close()
        print('Something was invalid. Please try something else.')
        print(txt + '\t' + str(e))
    
