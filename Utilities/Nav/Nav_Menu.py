'''
========================
==  Nav_Menu          ==
========================
==  3/26/2015         ==
==  Author: @dem4ply  ==
========================
'''

from ..General.Catch_Err import CatchErr
from .Directory_Listing import DirectoryLister as DL
import os


class OptionPage:
    _max_lines = 52
    def __init__(self, num, options={}):
        self.option_dict = options
        self.option_list = list(options.items())
        if len(self.option_list) > OptionPage._max_lines:
            self.option_list = self.option_list[0:51]
        self.num = num
    
    def has_key(self, key):
        return self.option_dict.keys().__contains__(key)
    
    def get_value(self, key):
        return self.option_dict[key]
    
    def add_key(self, key, value):
        self.option_list.append((key, value))
        self.option_dict = dict(self.option_list)
        
    def write_options(self):
        for o in self.option_list:
            #Print a menu with options[a,z]...
                #Each o in option_list is a tuple of ((unicode_ord_num, path)).
            if(o[0] <= 25 and o[0] >= 0):
                print('|\t[' + chr(o[0] + 97) + '] - ' + o[1])
            #(Print the command to go up a level in the directories).
            elif(o[0] == -50):
                super_dir = DL.get_super_dir()
                print('|\t[' + chr(o[0] + 97) + '] - ' + 'Go up one directory to \\'+super_dir+'\\')
            #...and [A, Z].
            elif(o[0] > 25): 
                print('|\t[' + chr(o[0] + 39) + '] - ' + o[1])
                
    def set_options(self, options):
        self.options = options
    
    
    
class Book:
    def __init__(self):
        self.pages = []
        self.length = 0
        
    def add_page(self, page):
        self.pages.append(page)
        self.length += 1
        
    def page(self, num):
        self.pages[num].write_options()
    
    def get_page(self, num):
        return self.pages[num]
    
    def generate_pages():
        pass
    
    def print_all_pages(self):
        for p in self.pages:
            p.write_options()
            print('\n')
            
            
            
class OptionBook(Book):
    def __init__(self):
        super(OptionBook, self).__init__()
        
    def add_option(self, page, key, value):
        if len(self.pages) > 0:
            self.pages[page].add_key(key, value)
        else:
            p = OptionPage(0)
            self.add_page(p)
            self.pages[0].add_key(key, value)
    
    #Create a book by taking a dictionary, cutting it up into as many equal
    #   parts of 52 it can, and then create a page for each equal group and the leftover.
    def generate_pages(self, opt_dict):
        #Making the dictionary into a list allows it to be sorted.
        options = list(opt_dict.items())
        #Sort by the first item in each tuple.
        options.sort(key=lambda t: t[0])
        
        #Page number starts at index 0.
        page_num = 0
        
        #The number of options integer-divided by 52 will give the number of full pages.
        no_of_full_pages = len(options) // 52
        #The number of options modded by 52 gives any leftover options.
        remaining_lines = len(options) % 52
        
        #Create and append the full pages.
        while page_num < no_of_full_pages:
            #Iterate through options in slices of 52.
            next_options = options[page_num * 52: (page_num+1) * 52]
            #For each item on the list, mod the first value by 52 to give it a value of [0, 52).
            for i in range(0,len(next_options)):
                next_options[i] = ((next_options[i][0]%52, next_options[i][1]))
            #Make the slice of options into a dict for the page.
            d = dict(next_options)
            p = OptionPage(page_num, d)
            self.add_page(p)
            page_num += 1
            
        #Only create the page for leftovers if there are any.
        if remaining_lines > 0:
            #Slice from options starting at the first leftover value and go until the end.
            next_options = options[-(remaining_lines):]
            #For each item on the list, mod the first value by 52 to give it a value of [0, 52).
            for i in range(0, len(next_options)):
                next_options[i] = ((next_options[i][0]%52, next_options[i][1]))
            #Make the slice of options into a dict for the page.
            d = dict(next_options)
            p = OptionPage(page_num, d)
            self.add_page(p)
            
            
            
class BookViewer:
    def __init__(self, book):
        self.book = book
        self.current_page = 0
        
    def view(self):
        self.book.page(self.current_page)
    
    def get_option(self, choice):
        if not len(choice) == 1:
            print('exiting...')
            return False
            
        choice = CatchErr(ord, choice)
        
        idx_offset = 97
        if choice <= 90 and choice >= 65:
            idx_offset = 39
            
        if self.book.get_page(self.current_page).has_key(choice - idx_offset):
            option = self.book.get_page(self.current_page).get_value(choice - idx_offset)
            return option
        else:
            print('There\'s no option',choice, 'on this page.')
        
    def turn_page(self, dx):
        if(self.has_page(self.current_page + dx)):
            self.current_page += dx
    
    def has_page(self, page_num):
        if page_num >= 0 and page_num < self.book.length:
            return True
        else:
            return False
    
    def act(self, func):
        finished = False
        
        while finished is False:
            back = False
            forward = False
            print('Page', str(self.current_page+1),'/', str(len(self.book.pages))) 
            self.view()
            if self.has_page(self.current_page - 1):
                print('|\t[' + '<,' + '] - ' + 'Go back a page')
                back = True
            if self.has_page(self.current_page + 1):
                print('|\t[' + '>.' + '] - ' + 'Go forward a page') 
                forward = True
            choice = input('[>\t').strip()
            if (choice == '<' or choice == ',') and back == True:
                self.turn_page(-1)
            elif (choice == '>' or choice == '.') and forward == True:
                self.turn_page(1)
            else:
                option_value = CatchErr(self.get_option, choice)
                if option_value == False:
                    return False
                return CatchErr(func, option_value)
                
    
    
class OptionPane:
    def __init__(self, gen_dict):
        book = OptionBook()
        book.generate_pages(gen_dict)
        self.viewer = BookViewer(book)
    
    def act(self, *, func):
        return self.viewer.act(func)
        
    def add_option(self, page, key, value):
        self.viewer.book.add_option(page, key, value)