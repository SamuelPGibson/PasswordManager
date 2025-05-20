from tkinter import Frame, Label, messagebox
from chichitk import IconButton

from .info import colors, font_name, font_name_bold, font_size_normal, font_size_header, category_colors


class AccountDisplay(Frame):
    ''' Frame for displaying account information in AccountsPage list
    '''
    def __init__(self, master, name:str, notes:str, category:str, date:str,
                 select_command, delete_command, bg=colors['background3'],
                 active_bg=colors['background4'], hover_bg=colors['background4'],
                 active_bar_color=colors['active_icon'], active_fg_header='#ffffff',
                 active_fg_notes='#ffffff', inactive_fg_header=colors['inactive_icon'],
                 inactive_fg_notes=colors['inactive_icon'], bar_width=5,
                 selected=False):
        Frame.__init__(self, master, bg=bg)
        self.__command = select_command # function called when account is selected - takes account name as input
        self.__delete_command = delete_command
        self.__name = name
        self.__notes = notes
        self.__category = category
        self.__date = date # date that account was created
        self.__selected = selected
        self.__hovering = False
        self.__header_colors = [inactive_fg_header, active_fg_header]
        self.__notes_colors = [inactive_fg_notes, active_fg_notes]
        self.__bar_colors = [[bg, hover_bg], [active_bar_color, active_bar_color]]
        self.__bg_colors = [[bg, hover_bg], [active_bg, active_bg]]
        self.info_max_len = 60 # maximum length of info text displayed under account name - changes based on frame width

        self.bar = Frame(self, width=bar_width)
        self.bar.pack(side='right', fill='y')

        # delete button - only visible when account is selected
        self.DeleteButton = IconButton(self, 'icons\\delete.png',
                                       self.delete_click, bar_height=0,
                                       popup_label='Delete Account',
                                       selectable=False)
        
        body_frame = Frame(self)
        body_frame.pack(side='left', fill='x')

        self.top_frame = Frame(body_frame)
        self.top_frame.pack(side='top', fill='x')
        self.header_label = Label(self.top_frame, text=self.__name,
                                  font=(font_name_bold, font_size_header))
        self.header_label.pack(side='left', padx=6, pady=2)
        self.date_label = Label(self.top_frame, text=self.__date,
                                font=(font_name, font_size_normal))
        self.date_label.pack(side='left', padx=0)

        self.bottom_frame = Frame(body_frame)
        self.bottom_frame.pack(side='bottom', fill='x')
        self.info_label = Label(self.bottom_frame, text=self.get_info_text(),
                                font=(font_name, font_size_normal))
        self.info_label.pack(side='left', padx=14, pady=2)

        self.bind('<Enter>', self.hover_enter)
        self.bind('<Leave>', self.hover_leave)
        self.bind('<Button-1>', self.click)
        for frame in [self.top_frame, self.bottom_frame, self.bar, self.header_label, self.date_label, self.info_label]:
            frame.bind('<Button-1>', self.click)

        self.bind('<Configure>', self.__configure) # to update info text width

        self.config_colors()

    def __configure(self, event=None):
        '''called whenever frame is resized'''
        # the width to text_length ratio probably shouldn't be hard coded
        self.info_max_len = int(self.winfo_width() / 7)
        self.info_label.config(text=self.get_info_text())

    def config_colors(self):
        '''sets colors based on selected status'''
        bg = self.__bg_colors[self.__selected][self.__hovering]
        self.config(bg=bg)
        self.top_frame.config(bg=bg)
        self.bottom_frame.config(bg=bg)
        self.DeleteButton.set_color(bg, which='bg', selected=False, hover=True)
        self.DeleteButton.set_color(bg, which='bg', selected=False, hover=False)
        self.header_label.config(bg=bg, fg=self.__header_colors[self.__selected])
        self.info_label.config(bg=bg, fg=self.__notes_colors[self.__selected])
        self.date_label.config(bg=bg, fg=self.__notes_colors[self.__selected])
        self.bar.config(bg=self.__bar_colors[self.__selected][self.__hovering])
    
    def hover_enter(self, event=None):
        '''called when mouse hovers on frame'''
        self.__hovering = True
        self.config_colors()

    def hover_leave(self, event=None):
        '''called when mouse leaves frame'''
        self.__hovering = False
        self.config_colors()
    
    def click(self, event=None):
        '''called when mouse clicks on account - calls command then selects account'''
        if not self.__selected:
            self.__command(self.__name) # this will deselect all accounts
            self.select()
    
    def select(self):
        '''selects account - if it is not already selected - does not call command'''
        if not self.__selected:
            self.__selected = True
            self.config_colors()
            self.DeleteButton.pack(side='right', padx=2)

    def deselect(self):
        '''deselects account - if it is currently selected'''
        if self.__selected:
            self.__selected = False
            self.config_colors()
            self.DeleteButton.pack_forget()

    def delete_click(self):
        '''
        Purpose:
            called when user clicks delete button
            asks user to confirm if they want to delete the account
            if user responds affirmatively, calls self.__delete_command
        Pre-conditions:
            (none)
        Post-conditions:
            deletes the account permanently if the user says yes
        Returns:
            (none)
        '''
        m = f'Are you sure you want to delete "{self.__name}"? This will delete the account permanently. You cannot undo this action.'
        if messagebox.askyesno(title='Delete Account - Are you sure?', message=m, default='no'):
            self.__delete_command(self.__name)
    
    def set_name(self, name:str):
        '''updates account name'''
        self.__name = name
        self.header_label.config(text=self.__name)

    def set_category(self, category:str):
        '''updates account category'''
        self.__category = category
        self.info_label.config(text=self.get_info_text())

    def set_notes(self, notes:str):
        '''updates account notes'''
        self.__notes = notes
        self.info_label.config(text=self.get_info_text())

    def set_date(self, date:str):
        '''updates account date - date account was created or modified'''
        self.__date = date
        self.date_label.config(text=self.__date)

    def trim_text(self, text:str, max_len:int):
        '''
        Purpose:
            trims texts and adds '...' if it is longer than max_len
            returned text will not be more than max_len characters, including '...'
        Pre-conditions:
            :param text : str - text to trim if necessary
            :param max_len : int - maximum length of text - must be >= 4
        Post-conditions:
            (none)
        Returns:
            :return str - text that has been trimmed if necessary
        '''
        # add functionality to break text at the end of a word (to make it look nicer)
        if len(text) <= max_len:
            return text
        else:
            return text[:max_len - 3] + '...'

    def get_info_text(self):
        '''returns info text in form: "Category - notes"
        if notes are longer than a certain length, notes will be cut off with "..."
        '''
        return self.trim_text(self.__category + ' - ' + self.__notes, self.info_max_len)
    
    def get_name(self) -> str:
        '''returns account name'''
        return self.__name
    
    def get_category(self) -> str:
        '''returns account category'''
        return self.__category

    def get_order_category(self) -> str:
        '''returns account category for sorting'''
        if self.get_category() == 'Other':
            # hackaround way to get 'Other' to appear last in list
            return 'ZZZZZ'
        return self.get_category()
    
    def get_date(self) -> str:
        '''returns account date'''
        return self.__date
    
    def get_date_year(self) -> str:
        '''returns the year of account date as a string, such as "2023"'''
        # date will either be in the form YYYY or MM/DD/YYYY
        return self.__date[-4:]

class Account:
    def __init__(self, Display:AccountDisplay, name:str, username:str,
                 password:str, category:str='Other', notes:str='No Notes',
                 date:str=''):
        '''update to store info about an account'''
        self.__Display = Display
        self.__name = name
        self.__username = username
        self.__password = password
        self.__category = category
        self.__notes = notes
        self.__date = date

    def set_name(self, name:str):
        '''updates account name'''
        self.__name = name
        self.__Display.set_name(name)

    def set_username(self, username:str):
        '''updates account username'''
        self.__username = username

    def set_password(self, password:str):
        '''updates account password'''
        # add functionality to store previous passwords
        self.__password = password

    def set_category(self, category:str):
        '''updates account category'''
        self.__category = category
        self.__Display.set_category(category)

    def set_notes(self, notes:str):
        '''updates account notes'''
        self.__notes = notes
        self.__Display.set_notes(notes)

    def set_date(self, date:str):
        '''updates account date'''
        self.__date = date
        self.__Display.set_date(date)

    def get_display(self):
        '''returns AccountDisplay object associated with account'''
        return self.__Display

    def get_name(self) -> str:
        '''returns account name'''
        return self.__name
    
    def get_username(self) -> str:
        '''returns account username'''
        return self.__username
    
    def get_password(self) -> str:
        '''returns account password'''
        return self.__password
    
    def get_category(self) -> str:
        '''returns account category'''
        return self.__category
    
    def get_notes(self) -> str:
        '''returns account notes'''
        return self.__notes
    
    def get_date(self) -> str:
        '''returns account date'''
        return self.__date

    def get_color(self) -> str:
        '''returns color based on category_colors in info.py'''
        if self.get_category().lower() in category_colors:
            return category_colors[self.get_category().lower()]
        else:
            return category_colors['other']

    def get_info_dict(self):
        '''returns account info as a dictionary
        dictionary keys: ['name', 'username', 'password', 'category', 'notes', 'date']
        '''
        d = {
            'name' : self.get_name(),
            'username' : self.get_username(),
            'password' : self.get_password(),
            'category' : self.get_category(),
            'notes' : self.get_notes(),
            'date' : self.get_date()
        }
        return d

        