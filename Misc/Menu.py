import builtins

''' Input
    Override the builtin function to better support multi-thread I/O.
def input(prompt=None):
    if prompt is not None:
        print(prompt, end='')
    i = builtins.input()
    return i 
'''
    
''' GenericMenu
    A class to put together a menu for viewing in a command window (shell, bash, etc.).
    Primarily made up of Option-subclass objects.
'''
class GenericMenu:
    def __init__(self, options=None):
        if options is not None:
            self.options = options
        else:
            options = []
        #Always has an option to kill the program.
        self.__k = KillProgram()
        self.addOption(self.__k)
        #Sort the Options in descending order based on the first arg of each Option.
        self.options = sortOptionList(self.options)
        
        #Create a dictionary, comprised of arg: OptionName pairs.
        argList = []
        for option in self.options:
            for arg in option.getArg():
                #Should be no duplicate args.
                if not argList.__contains__(arg):
                    argList.append((arg, option))
        self.keys = dict(argList)
    
    ''' runMenu
        runMenu starts a loop that continues running until the exit command is given.
        Prints the menu options, prompts for input, and attempts to execute commands based on input.
    '''
    def runMenu(self):
        exit_program = False
        while exit_program is False:
            if self.__k.state() is True:
                exit_program = True
                break
            print('Type the number or letter that coresponds to the command you wish to execute.')
            self.printMenu()
            userCommand = input('>>> ').strip()
            userCommand = userCommand.lower()
            print(userCommand, '<<<')
            
            if self.keys.__contains__(userCommand):
                print('Executing', self.keys[userCommand].getName() + '.')
                self.keys[userCommand].execute()
            else:
                print('Sorry,', userCommand, 'is not a recognized command.')
                continue
        quit()    
        
    ''' PrintMenu
        A function to print the write the menu to stdout (print) in the format: 
    
        '   ##################
        '   ##  menu opt 1  ##
        '   ##  menu opt 2  ##
        '   ##  menu opt... ##
        '   ##  menu opt n  ##
        '   ##################    
    '''
    def printMenu(self):
        #Print a border around the options.
        longestLine = self.findLongestLine()[0]
        lenOfTitle = longestLine + 8
        
        #Generate the string for the top and bottom borders.
        border = ''
        i = 0
        while i < lenOfTitle:
            border = border + '#'
            i += 1
        print(border)       
        #Print an option with the format '##  option[_..._]##' where [_..._] is an amount of whitespace 
        #   needed to match the length of the longest line.
        for option in self.options:
            wSpaceLen = lenOfTitle - len(str(option)) - 6
            spaces = ''
            i = 0
            while i < wSpaceLen:
                spaces = spaces + ' '
                i += 1
            print('##  ' + str(option) + spaces + '##')
        print(border + '\n')
    
    ''' addOption
        Adds an option to the menu.
    '''
    def addOption(self, option):
        self.options.append(option)
    
    ''' findLongestLine
        Finds the longest line possible to print out of the options.
        Useful for purposes of printing the menu.
    '''
    def findLongestLine(self):
        lenLongest = 0        
        idxLongest = 0
        for index, option in enumerate(self.options):
            lenOption = len(str(option))            
            if(lenOption > lenLongest):
                lenLongest = lenOption       
                idxLongest = index
        return (lenLongest, index)
  
class SimpleMenu(GenericMenu):
    def __init__(self):
        self.__i = TakeInput()
        args = [self.__i]
        super(SimpleMenu, self).__init__(args)
        
    def runMenu(self):
        return self.__i.execute()  
  
''' Option
    A class containing two main fields; A name field and a list of args. This is useful for creating menus.
'''  
class Option(object):
    def __init__(self, name='', args=[]):
        self.name = name
        self.args=[]
        self.setArgs(args)
        
    ''' getName
        Returns the name of the Option.
    '''
    def getName(self):
        return self.name
    
    ''' getArg
        If idx is None, getArg returns the entire list of args.
        If idx is not None, return the arg at index(idx).
    '''
    def getArg(self, idx=None):
        if idx is not None:
            return self.args[idx]
        else:
            return self.args
    
    ''' addArg
        Appends an argument onto args.
    '''
    def addArg(self, arg): 
        self.args.append(str(arg))
    
    ''' resetArgs
        Reset the args list for this Option.
    '''
    def resetArgs(self, args=None):
        self.args = list()
    
    ''' setArgs
        Set the args field to a nominated list, making sure that the args are converted to strings.
    '''
    def setArgs(self, args=[]):
        for arg in args:
            self.addArg(arg)
        
    ''' GetOptionAsTuple
        A method that returns a tuple consisting of the name of the Option and a list of the args.
    '''
    def GetOptionAsTuple(self):
        return ((self.name, self.args))
                
    ''' __str__
        A so-called 'To-string' method. Defines how an Option object should be converted to str.
    '''
    def __str__(self):
        noOfArgs = len(self.args)        
        if noOfArgs > 1:
            outString = str(self.args[0]) + '.) ' + self.name + ' ('
            i = 1
            while i < noOfArgs:
                if self.args[i] is not self.args[-1]:
                    outString = outString + str(self.args[i]) + ', '
                else:
                    outString = outString + str(self.args[i])
                i += 1
            outString = outString + ')'
        else:
            outString = str(self.args[0]) + '.) ' + self.name
        return outString

def sortOptionList(options=[]):
    sortedOptions = sorted(options, key=lambda r: r.args[0])
    return sortedOptions        
        
''' BoundFunction
    A subclass of Option, exists to abstract Option in a more readable manner.
'''
class BoundFunction(Option):
    def __init__(self, name='', args=[]):
        super(BoundFunction, self).__init__(name, args)
   
    def execute(self):
        pass

class TakeInput(BoundFunction):
    def __init__(self, args=['1']):
        super(TakeInput, self).__init__('TakeInput', args)
      
    def execute(self):
        line = input('Write the thing:\n>>> ').strip()
        return line
        
''' KillProgram
    A BoundFunction to exit the script.
'''        
class KillProgram(BoundFunction):
    def __init__(self, args=['4', 'q', 'quit']):
        super(KillProgram, self).__init__('Quit', args)
        self.fired = False
        
    def execute(self):
        self.fired = True
         
    def state(self):
        return self.fired
