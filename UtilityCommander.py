'''
=========================
==  Utility Commander  ==
=========================
==  3/26/2015          ==
==  Author: @dem4ply   ==
=========================
'''

def main():
    from Utilities.CommandType.Cmd_Types import UtilityCmd
    u = UtilityCmd()
    u.cmdloop()
    
if __name__ == '__main__':
    main()