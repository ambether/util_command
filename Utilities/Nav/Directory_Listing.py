'''
=========================
==  Directory Listing  ==
=========================
==  3/26/2015          ==
==  Author: @dem4ply   ==
=========================
'''

import os.path          as path
from os import listdir  as ls
from os import chdir    as cd
from os import getcwd

class DirectoryLister:
    _curdir = getcwd()
    _dirs = []
    #_keyed_dir_list was implemented for printing the directories in order.
    #Dictionaries do not provide sorting, so a list and dict are used.
    _keyed_dir_list = []
    _keyed_dirs = {}

        
    def set_dir(dir):
        dirname = dir
        print(dirname)
        if path.isdir(dirname):
            cd(dirname)
            DirectoryLister._curdir = getcwd()
            print('[<  Directory changed to', DirectoryLister.get_curdir())
            return True
        else:
            print('That\'s not a directory.')
            return False
    
    def get_file(pathname):
        p = pathname
        if path.isfile(p):
            return path.relpath(p)
        else:
            print('That\'s not a file.')
            return False 
    
    def get_dir(pathname):
        p = pathname
        if path.isdir(p):
            return path.relpath(p)
        else:
            print('That\'s not a folder.')
            return False
    
    def current_dirs(ignore_files, ignore_dirs, ignore=None):
        raw_dirs = ls()
        raw_dirs.sort(key=str.lower)
        if ignore_files == True:
            raw_dirs = DirectoryLister.remove_files_from_list(raw_dirs)
        elif ignore_dirs == True:
                raw_dirs = DirectoryLister.remove_dirs_from_list(raw_dirs)
                
        if ignore is not None:
            raw_dirs = DirectoryLister.remove_items_from_list(raw_dirs, ignore)
        DirectoryLister._dirs = list(raw_dirs)
    
    def idx_dirs():
        keyed_pairs = []
        for idx, d in enumerate(DirectoryLister._dirs):
            keyed_pairs.append((idx, d))
        keyed_pairs.sort(key=lambda t: t[0])
        
        DirectoryLister._keyed_dir_list = keyed_pairs
        DirectoryLister._keyed_dirs = dict(keyed_pairs)
    
    def idx_list(l):
        keyed_list = []
        for idx, opt in enumerate(l):
            keyed_list.append((idx, opt))
        keyed_list.sort(key=lambda t: t[0])
        
        return dict(keyed_list)
    
    def print_dirs():
        print('\n|  Files and directories:')
        for d in DirectoryLister._dirs:
            print('|  ' + d)
           
    def get_new_list(*,ignore_files=False, ignore_dirs=False, ignore=None):
        DirectoryLister.current_dirs(ignore_files, ignore_dirs, ignore)
        DirectoryLister.idx_dirs()
 
    def get_abs_curdir():
        return path.abspath(DirectoryLister._curdir)
    def get_curdir():
        return DirectoryLister._curdir
    def get_super_dir(abs=False):
        if abs == True:
            return path.abspath('..')
        return path.basename(path.abspath('..'))
    def get_dirs():
        return DirectoryLister._dirs
    def get_keyed_dirs():
        return DirectoryLister._keyed_dirs
            
    def remove_files_from_list(data):
        for d in data:
            if path.isfile(d):
                data.remove(d)
                DirectoryLister.remove_files_from_list(data)
        return(data)        
        
    def remove_dirs_from_list(data):
        for d in data:
            if path.isdir(d):
                data.remove(d)
                DirectoryLister.remove_dirs_from_list(data)
        return(data)
        
    def remove_items_from_list(data, item_list):
        for d in data:
            if d in item_list:
                data.remove(d)
                DirectoryLister.remove_items_from_list(data, item_list)
        return(data)
        
    def remove_data_by_directory(data, directory):
        for d in data:
            if d.startswith(directory):
                data.remove(d)
                DirectoryLister.remove_data_by_directory(data, directory)
        return(data)    
        