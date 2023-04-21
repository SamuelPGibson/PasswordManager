from tkinter import Frame, Label
from chichitk import CheckEntry, IconButton

from difflib import get_close_matches

from .info import colors, font_name, font_size_normal

# enhance search algorithm - build on top of get_close_matches()

class SearchBar(Frame):
    def __init__(self, master, results:list, show_accounts_command, show_all_command,
                 bg:str=colors['background0'], entry_bg:str=colors['background2'], menu_hover_bg=colors['background4'],
                 label_fg=colors['inactive_icon'], entry_fg='#ffffff', max_results=5):
        '''search bar to search existing accounts
        
        Parameters
        ----------
            master : tk.Frame - parent frame
            command : 1 argument function (str) - called with account name when an account is selected
            results : list of str - list of all accounts
            show_accounts_command : 1 argument function (list of str) - called with list of account names on each keystroke
            show_all_command : 0 argument function - called when search bar is cleared (with X button)
        '''
        Frame.__init__(self, master, bg=bg)
        self.__show_accounts_command = show_accounts_command
        self.__show_all_command = show_all_command
        self.__results = results # list of str -  of possible seach results
        self.__max_results = max_results # maximum number of results to display at once

        search_label = Label(self, text='Search ', bg=bg, fg=label_fg, font=(font_name, font_size_normal))
        search_label.pack(side='left')

        # using check_function is a manipulation of the intended purpose (but it works)
        # check_function is for checking if text is good (returns bool) - called with every keystroke
        self.Entry = CheckEntry(self, allowed_chars=None, max_len=None,
                                bg=entry_bg, fg=entry_fg, width=20,
                                check_function=self.update_search)
        self.Entry.pack(side='left')
        #self.Entry.bind('<FocusOut>', lambda e: self.__show_all_command())

        XButton = IconButton(self, 'icons\\close.png', self.x_click,
                             popup_label='Clear Search', bar_height=0,
                             selectable=False, inactive_bg=bg)
        XButton.pack(side='left', padx=2)

    def set_results(self, results:list):
        '''
        Purpose:
            updates list of possible search results
        Pre-conditions:
            :param results : list - possible search results
        Post-conditions:
            (none)
        Returns:
            (none)
        '''
        self.__results = results

    def x_click(self):
        '''
        Purpose:
            called when X beside search bar is clicked
            removes text from search bar and calls self.__show_all_command
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            (none)
        '''
        self.Entry.clear()
        self.__show_all_command()

    def update_search(self, text:str, cutoff=0.25):
        '''
        Purpose:
            to update search results based on text typed in search bar
            called with each keystroke in search bar
        Pre-conditions:
            :param text : str - current text in search bar
            :param cutoff : float between 0 and 1 - possibilities that don't score at least that similar to word are ignored
        Post-conditions:
            (none)
        Returns:
            :return bool - True if there is at least one result, otherwise False
        '''
        if text == '':
            self.__show_all_command()
            return
        search_results = get_close_matches(text, self.__results, n=self.__max_results, cutoff=cutoff)
        self.__show_accounts_command(search_results)
        return True
    
