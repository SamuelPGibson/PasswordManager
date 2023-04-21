from tkinter import Frame, Label
from chichitk import CheckEntry, TextBox, IconButton
from pandas.io import clipboard


from .info import font_name, font_name_bold, font_size_header, font_size_small, font_size_normal


class EntryField(Frame):
    ''' Frame to show/edit an account field, such as username or password
        Label and entry box are in inner frame so they will always be centered
        width of inner frame is determined by width of entry box - entry_width
        if info_text == '' then info frame will never be created - cannot call set_info_text()
    '''
    def __init__(self, master, title:str, bg:str, entry_bg:str,
                 fg='#ffffff', info_fg='#ffffff', info_text='',
                 active=False, copy_button=True, allowed_chars=None,
                 default_text='', hide_char=None, max_len=None, entry_width=40,
                 justify='left', inactive_justify='center',
                 font_size=font_size_normal):
        '''
        hide_char : str or None - character to display in entry box instead of text - such as '*' for password entry
        '''
        Frame.__init__(self, master, bg=bg)
        self.__active = active # True when entry box is editable
        self.__entry_justify, self.__inactive_entry_justify = justify, inactive_justify

        frame = Frame(self, bg=bg)
        frame.place(relx=0.5, rely=0.5, anchor='center') # centered inside parent frame

        # Label Frame
        label_frame = Frame(frame, bg=bg)
        label_frame.pack(side='top', fill='x')
        self.__Title = Label(label_frame, text=title, bg=bg, fg=fg,
                             font=(font_name_bold, font_size_header))
        self.__Title.pack(side='left')

        # Entry Frame
        entry_frame = Frame(frame, bg=bg)
        entry_frame.pack(side='top')
        self.__Entry = CheckEntry(entry_frame, default=default_text,
                                  allowed_chars=allowed_chars, max_len=max_len,
                                  justify=justify, bg=entry_bg, fg=fg,
                                  disabled_bg=bg, width=entry_width,
                                  hide_char=hide_char, check_function=None,
                                  font_size=font_size)
        self.__Entry.pack(side='left')
        if copy_button:
            self.__Copy = IconButton(entry_frame, 'icons\\copy.png',
                                     lambda: clipboard.copy(self.get_text()),
                                     bar_height=0, selectable=False, inactive_bg=bg,
                                     popup_label='Copy', click_popup='Copied!')
            self.__Copy.pack(side='right')

        # Info Frame
        if info_text != '':
            info_frame = Frame(frame, bg=bg)
            info_frame.pack(side='top', fill='x')
            self.__Info = Label(info_frame, text=info_text, bg=bg, fg=info_fg,
                                font=(font_name, font_size_small))
            self.__Info.pack(side='left')

        if not self.__active:
            self.set_inactive()

    def get_entry(self):
        '''returns Entry widget'''
        return self.__Entry

    def set_active(self):
        '''sets entry box state so that it is interactable'''
        self.__active = True
        self.__Entry.config(state='normal', justify=self.__entry_justify)

    def set_inactive(self):
        '''sets entry box state so that it is uninteractable'''
        self.__active = False
        self.__Entry.config(state='disabled', justify=self.__inactive_entry_justify)

    def set_title(self, title:str):
        '''
        Purpose:
            updates field title
        Pre-conditions:
            :param title: str - new field title
        Post-conditions:
            changes field title - discards old title
        Returns:
            (none)
        '''
        self.__Title.config(text=title)

    def set_text(self, text:str, select=False, focus=False):
        '''
        Purpose:
            updates text in entry box
        Pre-conditions:
            :param text: str - new text in entry box
            :param select: bool - if True, select new text in entry box
            :param focus: bool - if True, entry box takes focus
        Post-conditions:
            changes text in entry box - discards old text
        Returns:
            (none)
        '''
        self.__Entry.config(state='normal') # entry box must be interactable to add text
        self.__Entry.activate(text=text, select=select, focus=focus)
        if not self.__active: # set back to disabled if necessary
            self.__Entry.config(state='disabled')

    def set_info_text(self, info_text:str):
        '''
        Purpose:
            updates info text
        Pre-conditions:
            :param info_text: str - text to display below entry box
            can only be called if an info frame was created
            that is info_text was initialize not as as empty string
        Post-conditions:
            changes text below entry box
        Returns:
            (none)
        '''
        self.__Info.config(text=info_text)

    def get_text(self):
        '''
        Purpose:
            gets text from entry box
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return : str - text from entry box - could be empty string ''
        '''
        return self.__Entry.get()

class BoxField(Frame):
    ''' Frame to show/edit text
    
        Label and text box are in inner frame so they will always be centered
        Width of inner frame is determined by width of entry box - entry_width
    '''
    def __init__(self, master, title:str, bg:str, entry_bg:str, fg='#ffffff',
                 info_fg='#ffffff', info_text='', active=False, default_text='',
                 entry_width=40, entry_height=4, wrap='none', line_numbers_labels=True):
        '''
        if info_text == '' then info frame will never be created - cannot call set_info_text()
        '''
        Frame.__init__(self, master, bg=bg)
        self.__active = active

        frame = Frame(self, bg=bg)
        frame.place(relx=0.5, rely=0.5, anchor='center') # centered inside parent frame

        # Label Frame
        label_frame = Frame(frame, bg=bg)
        label_frame.pack(side='top', fill='x')
        self.__Title = Label(label_frame, text=title, bg=bg, fg=fg,
                             font=(font_name_bold, font_size_header))
        self.__Title.pack(side='left')

        # Entry Frame
        entry_frame = Frame(frame, bg=bg)
        entry_frame.pack(side='top')
        self.__Entry = TextBox(entry_frame, bg=entry_bg, fg=fg, disabled_bg=bg,
                               width=entry_width, height=entry_height,
                               font_name=font_name, font_size=font_size_normal,
                               wrap=wrap, check_blank_lines=False,
                               check_consecutive_spaces=False,
                               line_numbers_labels=line_numbers_labels)
        self.__Entry.pack(side='left')
        self.__Entry.clear_insert(default_text)

        # Info Frame
        if info_text != '':
            info_frame = Frame(frame, bg=bg)
            info_frame.pack(side='top', fill='x')
            self.__Info = Label(info_frame, text=info_text, bg=bg, fg=info_fg,
                                font=(font_name, font_size_small))
            self.__Info.pack(side='left')

        if not self.__active:
            self.set_inactive()

    def get_entry(self):
        '''returns Entry widget'''
        return self.__Entry

    def set_active(self):
        '''sets entry box state so that it is interactable'''
        self.__active = True
        self.__Entry.set_active()

    def set_inactive(self):
        '''sets entry box state so that it is uninteractable'''
        self.__active = False
        self.__Entry.set_inactive()

    def set_title(self, title:str):
        '''
        Purpose:
            updates field title
        Pre-conditions:
            :param title: str - new field title
        Post-conditions:
            changes field title - discards old title
        Returns:
            (none)
        '''
        self.__Title.config(text=title)

    def set_text(self, text:str, select=False, focus=False):
        '''
        Purpose:
            updates text in entry box
        Pre-conditions:
            :param text: str - new text in entry box
            :param select: bool - if True, select new text in entry box
            :param focus: bool - if True, entry box takes focus
        Post-conditions:
            changes text in entry box - discards old text
        Returns:
            (none)
        '''
        self.__Entry.set_active() # entry box must be interactable to add text
        self.__Entry.clear_insert(text)
        if not self.__active: # set back to disabled if necessary
            self.__Entry.set_inactive()

    def set_info_text(self, info_text:str):
        '''
        Purpose:
            updates info text
        Pre-conditions:
            :param info_text: str - text to display below entry box
            can only be called if an info frame was created
            that is info_text was initialize not as as empty string
        Post-conditions:
            changes text below entry box
        Returns:
            (none)
        '''
        self.__Info.config(text=info_text)

    def get_text(self):
        '''
        Purpose:
            gets text from entry box
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return : str - text from entry box - could be empty string ''
        '''
        return self.__Entry.get()

