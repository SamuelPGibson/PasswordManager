from tkinter import Toplevel, Frame, Label, messagebox
from chichitk import CheckEntry, CheckButton, IconButton, ToggleLabelButton, RangeLabel
from pandas.io import clipboard
import random

from .info import ascii_lowercase, ascii_uppercase, digits, punctuation
from .info import colors, font_name, font_name_bold, font_size_normal, font_size_header


def brighten(hex_code:str, fact:float):
    '''brightens hex_code by fact
    hex_code will be moved fact % of the way closer to full brightness
    
    :param hex_code: string - hex code in form "#0b0d34" or "0b0d34"
    :param fact: float between -1 and 1 - negative fact makes hex_code darker
    '''
    l = (hex_code[1:3], hex_code[3:5], hex_code[5:]) # split hex code into rgb components
    fact = max(-1, min(1, fact))
    if fact >= 0: # increase brightness
        values = [int(h, base=16) + (255 - int(h, base=16)) * fact for h in l]
    else: # decrease brightness
        values = [int(h, base=16) * (1 + fact) for h in l]
    return '#' + ''.join([f'{hex(int(round(v, 0)))[2:]:0>2}' for v in values])


class GeneratorFrame(Frame):
    def __init__(self, master, bg:str, top_bg:str=colors['background0'],
                 fg:str='#ffffff', sep_width=2):
        '''frame to generate random passwords'''
        Frame.__init__(self, master, bg=bg)

        # Top Label
        main_label = Label(self, text='Password Generator', bg=top_bg, fg=fg,
                           font=(font_name_bold, font_size_header))
        main_label.pack(side='top', fill='x')

        # Edge Dividers
        Frame(self, bg=top_bg, width=sep_width).pack(side='left', fill='y')
        Frame(self, bg=top_bg, width=sep_width).pack(side='right', fill='y')

        # Main Frame
        frame = Frame(self, bg=bg)
        frame.pack(side='top', fill='both')
        for row in range(7):
            frame.grid_rowconfigure(row, weight=1)
        pad = 2 # first and last columns are only for padding
        frame.grid_columnconfigure(0, weight=pad)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        frame.grid_columnconfigure(4, weight=pad)

        length_label = Label(frame, text='Password Length', bg=bg, fg=fg,
                             font=(font_name, font_size_normal))
        length_label.grid(row=0, column=1, sticky='nsew')
        self.RangeLabels = RangeLabel(frame, bg=bg, min_val=1, max_val=100,
                                      default_min=15, default_max=30, step=1,
                                      reference_width=5, fg='#ffffff',
                                      hover_bg=brighten(bg, 0.1))
        self.RangeLabels.grid(row=0, column=2, columnspan=2, sticky='nsew')

        self.UpperCase = CharacterSelect(frame, 'Uppercase', ascii_uppercase, bg,
                                         1, col_start=1, selected=True, active=True)
        self.LowerCase = CharacterSelect(frame, 'Lowercase', ascii_lowercase, bg,
                                         2, col_start=1, selected=True, active=True)
        self.Numbers = CharacterSelect(frame, 'Numbers', digits, bg, 3,
                                       selected=True, col_start=1, active=True)
        self.SpecialChars = CharacterSelect(frame, 'Special Chars', punctuation,
                                            bg, 4, col_start=1, selected=True, active=True)

        # Entry Box
        result_frame = Frame(frame, bg=bg)
        result_frame.grid(row=5, column=0, columnspan=5, sticky='nsew')
        inner_result_frame = Frame(result_frame, bg=bg)
        inner_result_frame.pack()
        self.Entry = CheckEntry(inner_result_frame, justify='center',
                                bg=colors['background4'], fg='#ffffff',
                                width=40, editable=False)
        self.Entry.pack(side='left')
        CopyButton = IconButton(inner_result_frame, 'icons\\copy.png',
                                lambda: clipboard.copy(self.Entry.get()),
                                bar_height=0, selectable=False, inactive_bg=bg,
                                popup_label='Copy', click_popup='Copied!')
        CopyButton.pack(side='right')

        button_frame = Frame(frame, bg=bg)
        button_frame.grid(row=6, column=0, columnspan=5, sticky='nsew')
        self.Generate = IconButton(button_frame, 'icons\\edit.png',
                                   self.generate_password, 'Generate', bar_height=0,
                                   selectable=False, inactive_bg=bg)
        self.Generate.pack()

    def generate_password(self):
        '''generates password and puts it in the EntryBox
        gets status of CharacterSelect objects to determine which characters to include
        '''
        Chars = [self.UpperCase, self.LowerCase, self.Numbers, self.SpecialChars]
        characters = ''.join([C.get_characters() for C in Chars])
        if characters == '': # no characters to choose from
            m = 'No characters selected! There must be at least one character selected to generate a password.'
            messagebox.showerror(title='Password Generator Error', message=m)
            return
        password = ''.join([random.choice(characters) for _ in range(random.randint(*self.RangeLabels.get()))])
        self.Entry.config(state='normal') # must be normal in order in insert text
        self.Entry.activate(text=password, select=False, focus=False)
        self.Entry.config(state='disabled') # set back to disabled

class CharacterSelect:
    def __init__(self, master, label:str, characters:str, bg:str, row:int, col_start:int=0, fg='#ffffff',
                 selected=True, active=True, check_box_padx=3, check_box_pady=3):
        '''frame for selecting a category of characters, such as "uppercase", "lowercase", or "numbers"'''
        self.__label = label
        category_label = Label(master, text=label, bg=bg, fg=fg, font=(font_name, font_size_normal))
        category_label.grid(row=row, column=col_start, sticky='nsew')
        self.__all_characters = characters # pass to edit window
        self.__characters = characters # set by edit window

        self.CheckBox = CheckButton(master, lambda b: None, inactive_bg=bg,
                                    active_bg=bg, inactive_fg='#888888', active_fg='#ffffff',
                                    bar_height=0, selected=selected, active=active)
        self.CheckBox.grid(row=row, column=col_start + 1, padx=check_box_padx, pady=check_box_pady)

        self.EditButton = IconButton(master, 'icons\\edit.png',
                                     self.open_edit_window, label='Edit',
                                     bar_height=0, selectable=False, inactive_bg=bg)
        self.EditButton.grid(row=row, column=col_start + 2)

    def open_edit_window(self):
        '''called when edit button is clicked - open window to toggle individual characters'''
        Window = CharacterWindow(self.__all_characters, self.__characters, self.__label)
        Window.wait_window()
        self.__characters = Window.get_selected_characters()

    def get_characters(self):
        '''returns all selected characters as a single string'''
        if not self.CheckBox.get():
            return ''
        return self.__characters

class CharacterWindow(Toplevel):
    ''' Popup window to select/deselect characters
    '''
    def __init__(self, all_characters:list, selected_characters:list, title:str, columns=5, w_fact=0.25, h_fact=0.5,
                 bg=colors['background2'], footer_bg=colors['background0'], button_pad=3):
        Toplevel.__init__(self)
        self.iconbitmap('lock_icon.ico')
        self.configure(bg=bg)
        self.title(title)

        # set window size
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = int(sw * w_fact), int(sh * h_fact)
        self.geometry(f'{w}x{h}+{sw // 2 - w // 2}+{sh // 2 - h // 2}')

        # Footer
        footer_frame = Frame(self, bg=footer_bg)
        footer_frame.pack(side='bottom', fill='x')
        Button = IconButton(footer_frame, 'icons\\check.png', self.destroy, label='Ok',
                            bar_height=0, selectable=False, inactive_bg=footer_bg)
        Button.pack(side='right', padx=2)
        SelectButton = IconButton(footer_frame, 'icons\\checkbox.png',
                                  self.select_all, label='Select All', bar_height=0,
                                  selectable=False, inactive_bg=footer_bg)
        DeselectButton = IconButton(footer_frame, 'icons\\box.png',
                                    self.deselect_all, label='Deselect All', bar_height=0,
                                    selectable=False, inactive_bg=footer_bg)
        SelectButton.pack(side='left', padx=2)
        DeselectButton.pack(side='left', padx=2)

        # Main Frame
        main_frame = Frame(self, bg=bg)
        main_frame.pack(fill='both', expand=True)
        for col in range(columns):
            main_frame.grid_columnconfigure(col, weight=1)
        for row in range((len(all_characters) - 1) // columns + 1):
            main_frame.grid_rowconfigure(row, weight=1)

        self.__buttons: list[ToggleLabelButton] = []
        for i, char in enumerate(all_characters):
            B = ToggleLabelButton(main_frame, lambda b: None, label=char,
                                  font_name=font_name_bold, font_size=20,
                                  selected=char in selected_characters,
                                  inactive_bg=bg, active_bg=footer_bg)
            B.grid(row=i // columns, column=i % columns, sticky='nsew',
                   padx=button_pad, pady=button_pad)
            self.__buttons.append(B)

    def select_all(self):
        '''
        Purpose:
            selects all label buttons
        Pre-conditions:
            (none)
        Post-conditions:
            all label buttons are changed to selected status
        Returns:
            (none)
        '''
        for B in self.__buttons:
            B.select()

    def deselect_all(self):
        '''
        Purpose:
            deselects all label buttons
        Pre-conditions:
            (none)
        Post-conditions:
            all label buttons are changed to unselected status
        Returns:
            (none)
        '''
        for B in self.__buttons:
            B.deselect()

    def get_selected_characters(self) -> list:
        '''
        Purpose:
            concatenates selected characters into a single string
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return: list of str - selected characters
        '''
        return ''.join([B.get_text() for B in self.__buttons if B.selected])
        
