from cmd import Cmd
from ..Nav.Directory_Listing import DirectoryLister as D
from subprocess import Popen, PIPE
from ..General.TakeAndVerifyInput import CheckPyFile as verifyPy
from ..General.TakeAndVerifyInput import FileExists
from ..General.Catch_Err import CatchErr
from ..Zip.PackageInZip import Zipper
from ..Nav import Nav_Menu
import time
import os

class IncludeDiagCmd(Cmd):
    def __init__(self):
        #Initialize the superclass.
        super(IncludeDiagCmd, self).__init__()
        #Set a default filename for the logfile.
        self.logfile = 'um.L'
    
    
    ''' newLogFile
        Create a new file, or format an existing one.
    '''
    def newLogFile(self, log):
        #Open the file in write mode.
        f = open(log, 'w')
        #Print nothing to the file. This will overwrite any data in the file, leaving essentially a blank file.
        f.write('')
        f.close()
    
    ''' longestLine
        Find the longest line in a body of text.
    '''
    def longestLine(self, data):
        lenLongest = 0
        idxLongest = 0
        data = data.split('\n')
        for idx, line in enumerate(data):
            if len(line) > lenLongest:
                lenLongest = len(line)
                idxLongest = idx
        return ((lenLongest, idxLongest))
    
    '''
        A method prefixed by 'do_' is executed when the string following 'do_' is given as a command in the main loop.
    '''
 
    def do_readlog(self, log=''):
        '    Reads what is set to the current logfile unless another filename is specified as an arg.\n    Note: large lines may cause ugly formatting in console.\n    Format: readlog (<logfile>)'
        #If no filename argument was given, use the class's default logfile.
        if log is '':
            log = self.logfile
        #Make sure the file exists. Can't read a nonexistant file.
        if(FileExists(log)):
            print('    Printing log file', '\'' + log + '\'.')
            #Open the file in read mode.
            f = open(log, 'r')
            data = f.readlines()
            f.close()
            #Print out the lines.
            for line in data:
                print(line.rstrip())
        #Can't find that file.
        else:
            print('That file does not exist.')
        
    def do_formatlog(self, log=''):
        '    Deletes the contents of the logfile. If no logfile exists, creates a logfile.\n    Format: formatlog (<logfile>)'
        #If no filename argument was given, use the class's default logfile.
        if log is '':
            log = self.logfile
            
        #Find out if the file even exists.
        if(os.path.isfile(log)):
            #Make sure this is what the user really wants to do!!
            #Assume it was not intended (to prevent loss of data).
            confirmed = False
            
            #Loop until a valid y/n answer has been supplied.
            while confirmed is False:
                print('Are you sure you want to wipe the log file?\n(Y/N)')
                confirm = input(self.prompt)
                if confirm.strip().lower() == 'y' or confirm.strip().lower() == 'yes':
                    #Set the object's logfile to the one specified if it's different than the current logfile.
                    if log is not self.logfile:
                        self.logfile = log
                    #Format the file.
                    self.newLogFile(log)
                    print('\nLog file', log, 'has been wiped.\n')
                    #Safe to exit method now.
                    confirmed = True
                
                elif confirm.strip().lower() == 'n' or confirm.strip().lower() == 'no':
                    #Do nothing. Safe to exit method now.
                    confirmed = True
                #Was not a valid y/n answer.
                else:
                    print('\nSorry, that command is not recognized.\n')
                    
        #File doesn't exist yet. Create file and make the object reference the file if it isn't already.
        else:
            if log is not self.logfile:
                self.logfile = log
            self.newLogFile(log)
            print('\nLog file was created.\n')
                    
    def do_exec(self, args):
        '    Executes a python script inside of a subprocess.\n    Writes the results to the current logfile.\n    Format: exec <scriptname> ([args])'
        #'FF' is the arg 'From File'. This arg retrieves the scriptname / args from file.
        #This should execute as long as the first two non-space characters are 'ff'. 
        if args[:2].strip().lower() == 'ff':
            #Read the scriptname.
            r = open('runScript_fileToRun.txt', 'r')
            scriptToExec = r.read().strip()
            r.close()
                
            #Read the args.
            a = open('runScript_Args.txt', 'r') 
            argsFromFile = a.read().strip()
            a.close()
            
            argsFromFile = argsFromFile.split()
            args = []
            for arg in argsFromFile:
                args.append(arg)
            
            #Insert the scriptname at the beginning of the list.
            args.insert(0, scriptToExec)
        
        else:
            #Split args into a list.
            args = args.split(' ')
            #args[0] is the name of the script to execute.
            scriptToExec = args[0]  
        #Make sure the script exists.
        if verifyPy(scriptToExec) is True:
            #The command should start with the python executable. %pythonpath%python is specific to @dem4ply's setup.
            cmdlist = ['%pythonpath%python']
            
            #Append, then remove the scriptname from args.
            cmdlist.append(args.pop(0))
            
            #Append the remaining args to cmdlist.
            for arg in args:
                cmdlist.append(arg)
            #Put the entirety of the command into a tuple.
            cmd = tuple(cmdlist)
            
            #Open the logfile in append mode.
            f = open(self.logfile, 'a')
            
            #Start the subprocess to run the command. Use a shell to run the command, and pipe the stdout and stderr.
            p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            
            #Inform the user that an attempt at executing the script is being had.
            print('Executing ' + scriptToExec)
            #Execute the script, and pipe the stdout / stderr to local variables.
            stdout,stderr = p.communicate()
            #Let the user know that the script finished executing.
            print('...done.')
            
            #The output is in bytes. Decoding it to utf-8 will let it work as strings.
            out_text = stdout.decode('utf-8')
            err_text = stderr.decode('utf-8')
            
            #In order to place a border around the report, the longest line in the report must be determined.
            lenTxt_1 = self.longestLine(out_text)[0]     #Find the longest line in out_text.
            lenTxt_2 = self.longestLine(err_text)[0]     #Find the longest line in err_text.
            
            titleLine = '==  Diagnostic file entry for ' + os.path.basename(scriptToExec)
            #Find the largest of lenTxt_1, lenTxt_2, and len(titleLine)
            widthReport = max(lenTxt_1, lenTxt_2, len(titleLine))
            
            #Obtain the time the script was run at.
            localTime = time.localtime()
            #Get the raw clock time and put in a list, format [h(h), m(m)]
            rawclocktime = [localTime[3], localTime[4]]
            #If the hours is only a single digit, change it to the format hh.
            if len(str(rawclocktime[0])) < 2:
                rawclocktime[0] = '0' + str(rawclocktime[0])
            #If the minutes is only a single digit, change it to the format mm
            if len(str(rawclocktime[1])) < 2:
                rawclocktime[1] = '0' + str(rawclocktime[1])
            
            #Format the date to be format d(d)/M(M)/yyyy.
            date = '/'.join((str(localTime[2]), str(localTime[1]), str(localTime[0])))
            #Format the clocktime to be format hh:mm.
            clocktime = ':'.join((str(rawclocktime[0]), str(rawclocktime[1])))
            #Join date and clocktime together with a comma and space in between, as well as the lefthand part of the border.
            datetime = '==  ' + ', '.join((date, clocktime))
            
            #Create a border to go at the top / bottom of the report. It should be the same length as the longest line.
            i = 0
            border = '===='
            while i < widthReport:
                border = border + '='
                i += 1
            
            #Append the titleLine and datetime to the beginning of the output.
            data = titleLine + '\n' + datetime + '\n'
            if len(out_text) > 0:
                data = data + out_text
            if len(err_text) > 0:
                data = data + err_text
            
            #Print a border.
            f.write(border + '\n')
            #Split the data into seperate lines.
            data = data.split('\n')
            
            for idx, line in enumerate(data):    
                wSpaceLen = (widthReport) - len(line)
                spaces = ''
                i = 0
                #If the index is 2, it should print a border to seperate the datetime from the out_text / err_text.
                if idx is 2:
                    f.write(border + '\n')
                while i < wSpaceLen:
                    spaces = spaces + ' '
                    i += 1
                #Don't print a linebreak on the last line.
                if idx is len(data) - 1:
                    f.write(line + spaces + '  ==')
                else:
                    f.write(line + spaces + '  ==\n')
            f.write('\n' + border + '\n\n')
        #Could not verify the existence of the script.    
        else:
            print('Sorry, that\'s a bad script name.\n')
    
    def do_ff(self, args=None):
        '    A quick shortcut for running exec ff'
        args = 'ff'
        CatchErr(self.do_exec, args)
            
            
            
            
            
class IncludeNavCmd(IncludeDiagCmd):
    def __init__(self):
        #Initialize the superclass.
        super(IncludeNavCmd, self).__init__()
        self.files      = []
        self.folders    = []
        self.base_directory = D.get_abs_curdir()
   
    def do_ls(self, args=None):
        if args == 'file':
            if len(self.files) > 0:
                for f in self.files:
                    print('|    ' + f.strip()) 
            else:
                print('No files have been added yet.')
        elif args == 'folder':
            if len(self.folders) > 0:
                for f in self.folders:
                    print('|    ' + f.strip())
            else:
                print('No folders have been added yet.')
        else:
            D.get_new_list()
            D.print_dirs()
        
    ''' do_chdir
        Change the current working directory(cwd).
        Implements the Nav_Menu UI.
    '''
    def do_chdir(self, args=None):
        #Get a current list of directories.
        D.get_new_list(ignore_files=True)
        
        pane = Nav_Menu.OptionPane(D._keyed_dirs)
        pane.add_option(0, -50, '../')
        
        print('Select a Directory from one of the below (case-sensitive):')
        #Attempt to change the directory based on the user's input.
        dir_changed = pane.act(func=D.set_dir)
        
    ''' do_addfile
        Add a file from the cwd to a list of files. This list is used to create
            zip archives.
    '''
    def do_addfolder(self, args=None):
        D.get_new_list(ignore_files=True, ignore=self.folders)
        pane = Nav_Menu.OptionPane(D._keyed_dirs)
        print('Select a folder from the current directory:')
        
        isfolder = pane.act(func=D.get_dir)
        if isfolder:
            for root, dirs, files in os.walk(isfolder):
                if not root in self.folders:
                    self.folders.append(root)
                for f in files:
                    if not os.path.join(root, f) in self.files:
                        self.files.append(os.path.join(root, f))
                
    def do_addfile(self, args=None):
        #Get a current list of files, excluding the files that have already been added to the list.
        D.get_new_list(ignore_dirs=True, ignore=self.files)
        pane = Nav_Menu.OptionPane(D._keyed_dirs)
        print('Select a file from the current directory:')
        
        #Attempt to get the file nominated by the user.
        isfile = pane.act(func=D.get_file)
        if isfile:
            if not self.files.__contains__(isfile):
                #Append the selected file to the list of files.
                self.files.append(isfile)
                print('    File', isfile, 'was added to the list.')
            else:
                print('    File', isfile, 'was already in the list.') 
                
    def do_remv(self, args=None):
        has_folders = False 
        has_files = False
        
        if len(self.folders) > 0:
            has_folders = True
        
        if len(self.files) > 0:
            has_files = True
        
        if has_folders and has_files:
            verified = False
            while verified == False:
                ipt = input('Remove a\n[a] folder, \n-or-\n[b] file?\n[>  ').lower().strip()
                if ipt == 'a':
                    keyed_folders = D.idx_list(self.folders)
                    pane = Nav_Menu.OptionPane(keyed_folders)
                    remv_folder = pane.act(func=D.get_dir)
                    if remv_folder:
                        if remv_folder in self.folders:
                            self.files = D.remove_data_by_directory(self.files, remv_folder)
                            self.folders = D.remove_data_by_directory(self.folders, remv_folder)
                    verified = True
                    
                elif ipt == 'b':
                    keyed_files = D.idx_list(self.files)
                    pane = Nav_Menu.OptionPane(keyed_files)
                    remv_file = pane.act(func=D.get_file)
                    if remv_file:
                        self.files.remove(remv_file)
                    verified = True  
                    
        elif has_folders:
            keyed_paths = D.idx_list(self.folders)
            pane = Nav_Menu.OptionPane(keyed_paths)
            remv_folder = pane.act(func=D.get_dir)
            if remv_folder:
                if remv_folder in self.folders:
                    self.files = D.remove_data_by_directory(self.files, remv_folder)
                    self.folders = D.remove_data_by_directory(self.folders, remv_folder)
        
        elif has_files:
            keyed_paths = D.idx_list(self.files)
            pane = Nav_Menu.OptionPane(keyed_paths)
            remv_file = pane.act(func=D.get_file)
            if remv_file:
                self.files.remove(remv_file)
            
        else:
            print('No files or folders have been added yet.')
    
    ''' do_zip
        Put the contents of the list of files into a zip archive.
    '''
    def do_zip(self, args=None):
        project_title = input('    What would you like to name the archive?\n[> ').strip()
        #Create a Zipper.
        z = Zipper()
        main_file = None
        nom_main_file = input('Would you like to nominate a file as the __main__ file? (Y/N)\n[> ').strip()
        if nom_main_file.lower() == 'n' or nom_main_file == '':
            print('Continuing...')
        elif nom_main_file.lower() == 'y':
            #Make an indexed list of the files.
            keyed_files = D.idx_list(self.files)
            pane = Nav_Menu.OptionPane(keyed_files)
            
            #Have the user select one of the files from the list.
            main_file = pane.act(func=D.get_file)
        print('  Writing files to zip archive...')
        #Write the zip archive
        z.writeZip(project_title, self.base_directory, self.files, main_file)
        print('  ...Done.')
        #Write the readme file.
        z.writeReadme()
        #Write the batch file (as needed).
        z.writeBatFile()

        
class UtilityCmd(IncludeNavCmd):
    def __init__(self):
        super(UtilityCmd, self).__init__()
        #Change the prompt string to '[>  '.
        self.prompt = '[> '
    
    def preloop(self):
        #Print a welcome message before starting the command loop.
        print('Welcome to Utility Commander V_00 (3/26/2015)')
    
    def do_kill(self, args=None):
        print('\n\'script is kill\'')
        print('\'no\'')
        quit()
