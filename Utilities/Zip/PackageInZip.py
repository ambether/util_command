'''
=============================
==  Package Into Zip V1.2  ==
=============================
==  3/17/2015              ==
==  Author: @dem4ply       ==
=============================
'''
from zipfile    import ZipFile
from sys        import argv
import time
import os
import re

class Zipper:
    def __init__(self):
        self.zip_name = ''
        self.bat_name = ''
        self.path_name = ''
        self.has_main = False

    def writeZip(self, proj_name, target, file=None, nom_main=None):
        if file is None:
            #Get and write the time and error to the logfile.
            getlocaltime = time.localtime()
            exectime = "[{0}:{1}:{2}]".format(
                getlocaltime[3],
                getlocaltime[4],
                getlocaltime[5]
                )
            self.writeErrLog(exectime + '\tNo arguments were supplied!!\n\n')
            return 1
            
        self.zip_name = proj_name
        #Set path_name.
        self.path_name = os.path.join(target, self.zip_name)        
        #Create the folder to write to.
        if not os.path.isdir(self.path_name):
            print('Creating dir', self.path_name)
            os.mkdir(self.path_name)

        #Add .zip to the name to get the filename of the .zip file.
        self.zip_name = '.'.join((self.zip_name, 'zip'))
        
        #Open a zip file in write mode.
        z = ZipFile(os.path.join(self.path_name, self.zip_name), 'w')       
        
        #For each filename in file, write the file to the zip.
        for f in file:
            try:
                if os.path.basename(f).lower() == 'main.py' or os.path.basename(f) == nom_main:
                    z.write(f, arcname='__main__.py')
                    self.has_main = True
                else:
                    z.write(f)
            except Exception as e:
                #Get and write the time and error to the logfile.
                getlocaltime = time.localtime()
                exectime = "[{0}:{1}:{2}]".format(
                    getlocaltime[3],
                    getlocaltime[4],
                    getlocaltime[5]
                    )
                self.writeErrLog(exectime + '\t' + str(e) + '\n\n')
        #Close the file-like object.
        z.close()
    
    def writeBatFile(self):
        #Only create a .bat file if the archive has a __main__.py file.
        if self.has_main:
            #Write a simple .bat file to run the generated .zip file as a python script.
            #   This .bat file will take command-line - arguments from args.txt.
            text = "{0}\n{1}\n{2}\n{3}\n{4} {5} {6}\n{7} ".format(
                '@echo off',
                'set /p args=<args.txt',
                'set filename=' + self.zip_name,
                'echo Executing %filename%!!',
                'C:\\ISMPython\\V3_2\\Python ',
                '%filename%',
                '%args%',
                'pause'
                )
            self.bat_name = self.zip_name[:-4] + '.bat'
            f = open(os.path.join(self.path_name, self.bat_name), 'w')
            f.write(text)
            f.close()
            if not os.path.isfile(os.path.join(self.path_name, 'args.txt')):
                self.writeArgsFile()
                print('args.txt file written.\n')
            print('.bat file written.\n')
        else:
            #No use executing a plain old archive...
            pass
            
    def writeArgsFile(self):
        f = open(os.path.join(self.path_name, 'args.txt'), 'w')
        f.close()
        
    def writeErrLog(self, line=''):
        f = open('Err.log', 'a')
        f.write(line)
        f.close()
        
    def writeReadme(self):
        if self.has_main:
            text = "{0}\n{1}\n{2}\n{3}".format(
                'The file ' + self.zip_name + ' contains all of the files specified by PackageInZip.py.',
                'This archive will be runnable as a python script.',
                'If you would like to provide run-time arguments to the script, write them in the args.txt file.',
                'Once you\'ve set up the project as you like, execute the ' + self.bat_name + ' file to run the project with the supplied args.'
                )     
        else:
            text = 'The file ' + self.zip_name + ' contains all of the files specified by PackageInZip.py.'
        f = open(os.path.join(self.path_name, 'readme.txt'), 'w')
        f.write(text)
        f.close()
        print('Readme file written.\n')