from tkinter import Frame, Label
from chichitk import LabelButton


from utils.info import colors, font_size_normal
from utils.entry_field import EntryField


class LoginPage(Frame):
    def __init__(self, master, command, destroy_command, max_attempts=5, entry_width=25,
                 bg=colors['background0'], entry_bg=colors['background3'], border_bg=colors['background2'],
                 footer_fg=colors['inactive_icon']):
        '''login page that asks user for a password and encryption key'''
        Frame.__init__(self, master, bg=border_bg)
        self.__destroy_command = destroy_command
        self.__attempt_count = 0
        self.__max_attempts = max_attempts

        # Header text
        header_label = 'The most basal and barely passable password manager ever built'
        sub_header_label = '"Your passwords are safe here... as long as no one tries to guess them!"'
        header_label = Label(self, text=header_label + '\n' + sub_header_label,
                             bg=border_bg, fg=footer_fg, font=('Segoe UI Black', 12))
        header_label.place(relx=0.5, rely=0.125, anchor='center')

        # Footer text
        footer_label = 'Password Manager built with Tkinter in Python - Sam Gibson - Feb, 2023'
        Label(self, text=footer_label, bg=border_bg, fg=footer_fg, font=('Lucida Handwriting', 11)).pack(side='bottom', pady=10)

        # Main page - place in center of screen
        main_frame = Frame(self, bg=bg)
        main_frame.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.5, anchor='center')

        self.__Password = EntryField(main_frame, 'Password', bg, entry_bg, active=True, entry_width=entry_width,
                                     copy_button=False, info_text=' ', info_fg='#ff0000', hide_char='*', font_size=font_size_normal + 2)
        self.__Password.pack(side='top', fill='both', expand=True)

        self.__Key = EntryField(main_frame, 'Encryption Key', bg, entry_bg, active=True, entry_width=entry_width,
                                copy_button=False, hide_char='*', font_size=font_size_normal + 2)
        self.__Key.pack(side='top', fill='both', expand=True)

        self.Button = LabelButton(main_frame, command, label='Login', inactive_bg=bg, selectable=False)
        self.Button.pack(side='bottom', pady=20)

        # Set Tab order
        self.__Password.get_entry().bind("<Tab>", lambda e: self.__Key.get_entry().focus())
        self.__Key.get_entry().bind("<Tab>", lambda e: self.__Password.get_entry().focus())
        self.__Password.get_entry().bind("<Return>", lambda e: command())
        self.__Key.get_entry().bind("<Return>", lambda e: command())

    def get_password(self):
        '''
        Purpose:
            retrives password from self.__Password entry box
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return: str - text from password entry box
        '''
        return self.__Password.get_text()
    
    def get_key(self):
        '''
        Purpose:
            retrives text from key entry box
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return: str - text from key entry box
        '''
        return self.__Key.get_text()
    
    def update_attempts_display(self):
        '''
        Purpose:
            updates attempts display based on self.__attempt_count
        Pre-conditions:
            (none)
        Post-conditions:
            changes attempts display - underneath password entry box
        Returns:
            (none)
        '''
        attempts_remaining = self.__max_attempts - self.__attempt_count
        text = f'Incorrect credentials. {attempts_remaining} attempt{"s" * (attempts_remaining > 1)} remaining.'
        self.__Password.set_info_text(text * (self.__attempt_count > 0)) # empty string if no attempts have been made

    def reset_attempts(self):
        '''
        Purpose:
            reset unsuccessful attempt count to 0
        Pre-conditions:
            (none)
        Post-conditions:
            changes display of unsuccessful attempts
        Returns:
            (none)
        '''
        self.__attempt_count = 0
        self.update_attempts_display()

    def increment_attempts(self):
        '''
        Purpose:
            increases unsuccessful attempt count by 1
        Pre-conditions:
            (none)
        Post-conditions:
            changes display of unsuccessful attempts
        Returns:
            (none)
        '''
        self.__attempt_count += 1
        if self.__attempt_count >= self.__max_attempts:
            self.__Password.set_info_text('You done messed up A-A-ron!')
            self.after(400, self.__destroy_command)
        else:
            self.update_attempts_display()

    def clear(self):
        '''
        Purpose:
            clears text in password and key entry boxes
        Pre-conditions:
            (none)
        Post-conditions:
            clears text in password and key entry boxes
            all previous text is discarded
        Returns:
            (none)
        '''
        self.__Password.set_text('')
        self.__Key.set_text('')

    def password_focus(self):
        '''
        Purpose:
            sets focus on password entry box
        Pre-conditions:
            (none)
        Post-conditions:
            takes focus from last widget and gives it to password entry box
        Returns:
            (none)
        '''
        self.__Password.get_entry().focus()

