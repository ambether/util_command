''' 
=============================
==  Take and Verify Input  ==
=============================
==  3/13/2015              ==
==  Author: @dem4ply       ==
=============================
'''
import os   #OS is useful for working with file paths, etc.  
import re   #Import Regular Expression.

import builtins

''' Input
    Override the builtin function to better support the Diagnostic Tool.
'''
def input(prompt=None):
    if prompt is not None:
        print(prompt)
    i = builtins.input()
    return i 

''' GetAndCheckFilePython
    A function to take string input from a user and check to see if the file exists at
    the given path, and with the .Py file extension.
'''
def GetAndCheckFilePython():
    verified = False
    while verified is False:
        filepath = input("path: ")
        filepath = str(filepath).strip('\r')
        absFilepath = os.path.abspath(filepath)
        absDir = os.path.dirname(absFilepath)
        
        filename = os.path.basename(filepath).split()
        filename = str(filename).strip('[')
        filename = str(filename).strip(']')
        filename = str(filename).strip('\'')
        
        if(os.path.isdir(absDir)):
            if(os.path.isfile(absFilepath)):
                fileExtension = re.search('(.+?)(\.py)', filename)
                if(fileExtension):
                    verified = True
                else:
                    print("Wrong extension\n")
            else:
                print("No file\n")
        else:
            print("No directory\n")
    return absFilepath

def CheckPyFile(filepath=''):
    verified = False
    absFilepath = os.path.abspath(filepath)
    absDir = os.path.dirname(absFilepath)
    
    filename = os.path.basename(filepath)
    
    if(os.path.isdir(absDir)):
        if(os.path.isfile(absFilepath)):
            fileExtension = re.search('(.+?)(\.py)', filename)
            if(fileExtension):
                verified = True
            else:
                print('Wrong extension.\n')
        else:
            print('No such file.\n')
    else:
        print('No such directory.\n')
    return verified
      
def CheckGenericFile(input='', message=None):
    verified = False
    filepath = input.strip()
    if message is not None:
        print(message, filepath, '<<<')
    else:
        print('Filepath:', filepath, '<<<') 
    absFilepath = os.path.abspath(filepath)
    absDir = os.path.dirname(absFilepath)
    
    filename = os.path.basename(filepath)
    filename = str(filename).strip('[')
    filename = str(filename).strip(']')
    filename = str(filename).strip('\'')
    
    if(os.path.isdir(absDir)):
        if(os.path.isfile(absFilepath)):
            print('Found it.\n')
            fileExtension = re.search('.+?(\.[\w]+?)', filename)
            if(fileExtension):
                verified = True
            else:
                print('That\'s not a valid filename!!\n')
        else:
            print('No such file...\n')
    else:
        print('No such directory...\n')
    if verified is True:
        return absFilepath
    else:
        return False
    
def FileExists(input='', message=None):
    verified = False
    filepath = input
    
    if message is not None:
        print(message, filepath)
    else:
        print('Filepath:', filepath)
    
    absFilepath = os.path.abspath(filepath)
    absDir = os.path.dirname(absFilepath)
    
    filename = os.path.basename(filepath)
    filename = filename.strip()
    
    if(os.path.isdir(absDir)):
        if(os.path.isfile(absFilepath)):
            verified = True
        else:
            print('File does not exist.')
    else:
        print('Directory does not exist.')
    
    return verified
     
 