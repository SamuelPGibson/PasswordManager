from tkinter import Tk, Frame, Label, messagebox
from chichitk import IconButton, ToggleIconButton
from datetime import datetime
import pandas as pd
import os

from utils.info import colors, font_name, font_size_normal, database_path
from utils.search_bar import SearchBar
from utils.timeout_bar import TimeoutBar
from utils.generator import GeneratorFrame
from utils.encoding_manager import EncodingManager
from utils.accounts import Account, AccountDisplay
from accounts_page import AccountsPage
from edit_page import EditPage
from login_page import LoginPage

# BUG
#   If an account is added while logged in with the wrong encryption key,
#   it will be encoded incorrectly - it can never be retrived

class App(Tk):
    def __init__(self, w_fact=0.55, h_fact=0.75, header_footer_bg=colors['background0']):
        self.__unsaved_message = 'There are unsaved changes to the current account. Loading a new account will discard unsaved changes. Do you want to load new account anyway?'

        Tk.__init__(self)
        self.__logged_in = False
        self.protocol('WM_DELETE_WINDOW', self.window_destroy)
        self.iconbitmap('lock_icon.ico')
        self.configure(bg=colors['background2'])
        self.title('Password Manager')

        # set window size
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = int(sw * w_fact), int(sh * h_fact)
        self.geometry(f'{w}x{h}+{sw // 2 - w // 2}+{sh // 2 - h // 2 - 15}')

        self.__EncodingManager = EncodingManager()

        # Login Window
        self.LoginPage = LoginPage(self, self.login, self.destroy, max_attempts=5)
        self.LoginPage.pack(fill='both', expand=True)

        # Main Window - (visible when logged in)
        self.home_frame = Frame(self)

        # Header
        header_frame = Frame(self.home_frame, bg=header_footer_bg)
        header_frame.pack(side='top', fill='x')
        self.SearchBar = SearchBar(header_frame, [],
                                   lambda l: self.AccountsPage.show_accounts(l),
                                   lambda: self.AccountsPage.show_all_accounts(),
                                   bg=header_footer_bg)
        self.SearchBar.pack(side='left')
        self.NewButton = IconButton(header_frame, 'icons\\plus.png',
                                    self.new_account, label='New', bar_height=0,
                                    popup_label='Create New Account',
                                    selectable=False,
                                    inactive_bg=header_footer_bg, padx=2)
        self.NewButton.pack(side='right')

        # Footer
        footer_frame = Frame(self.home_frame, bg=header_footer_bg)
        footer_frame.pack(side='bottom', fill='x')
        self.GeneratorButton = ToggleIconButton(footer_frame, 'icons\\edit.png',
                                                self.toggle_generator_frame,
                                                label='Password Generator',
                                                popup_label='Open/Close Password Generator',
                                                active_bg=header_footer_bg,
                                                inactive_bg=header_footer_bg)
        self.GeneratorButton.pack(side='left')
        self.timeout_label = Label(footer_frame, text='', bg=header_footer_bg,
                                   fg=colors['inactive_icon'],
                                   font=(font_name, font_size_normal))
        self.timeout_label.pack(side='right', padx=3)
        LockButton = IconButton(footer_frame, 'icons\\lock.png', self.lockout,
                                popup_label='Lock', bar_height=0,
                                selectable=False, inactive_bg=header_footer_bg)
        LockButton.pack(side='right')

        self.Timer = TimeoutBar(self.home_frame, header_footer_bg, 120, self.lockout,
                                lambda s: self.timeout_label.config(text=f'Time Until Lockout: {s}'), height=2)
        self.Timer.pack(side='bottom', fill='x')

        # Main Frame
        main_frame = Frame(self.home_frame)
        main_frame.pack(fill='both', expand=True)
        
        left_frame = Frame(main_frame, bg=colors['background2'])
        right_frame = Frame(main_frame, bg=colors['background3'])
        left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1, anchor='nw')
        right_frame.place(relx=1, rely=0, relwidth=0.5, relheight=1, anchor='ne')

        self.AccountsPage = AccountsPage(left_frame, colors['background2'])
        self.AccountsPage.pack(side='top', fill='both', expand=True)
        self.EditPage = EditPage(right_frame, colors['background3'],
                                 self.__EncodingManager, self.save_accounts,
                                 self.get_account_names, top_bg='#1e281d',
                                 top_hover_bg='#2d3c2b')
        self.EditPage.pack(side='top', fill='both', expand=True)

        self.GeneratorFrame = GeneratorFrame(left_frame, colors['background3'])

        # Any click in the app will restart lockout timer
        # add='+' causes this to not override other bindings
        self.bind_all('<Button-1>', lambda e: self.Timer.restart(), add='+')

        self.load_accounts()
        self.LoginPage.password_focus()
        self.mainloop()

    def load_accounts(self):
        '''load accounts from database
        only ever called once at the start of program - in App.__init__
        '''
        if not os.path.exists(database_path): # no database available
            return
        self.__Accounts: list[Account] = []
        df = pd.read_csv(database_path, index_col=0)
        for _, row in df.iterrows():
            D = AccountDisplay(self.AccountsPage.main_frame, row.name,
                               row.notes, row.category, row.date,
                               self.select_account, self.delete_account)
            A = Account(D, row.name, row.username, row.password,
                        category=row.category, notes=row.notes, date=row.date)
            self.__Accounts.append(A)
        self.AccountsPage.add_accounts([A.get_display() for A in self.__Accounts])
        self.SearchBar.set_results([A.get_name() for A in self.__Accounts])

    def save_accounts(self, repack=True):
        '''saves accounts to database and repacks in AccountsPage'''
        if repack:
            # repack accounts because changes may affect the order of accounts in display
            self.AccountsPage.repack_accounts()
        # update account names known to search bar
        self.SearchBar.set_results([A.get_name() for A in self.__Accounts])
        # generate pandas DatFrame from a list of dictionaries
        df = pd.DataFrame([A.get_info_dict() for A in self.__Accounts])
        # sort DataFrame however you want
        #df.to_csv(database_path, index=False)

    def new_account(self):
        '''creates new account to be edited in right frame'''
        if self.EditPage.unsaved_changes() and not messagebox.askyesno(title='Unsaved Changes', message=self.__unsaved_message):
            return # don't create new account if there are unsasved changes the user wants to keep
        date = datetime.now().strftime('%m/%d/%Y')
        D = AccountDisplay(self.AccountsPage.main_frame, 'New Account', '', 'Other', date,
                           self.select_account, self.delete_account)
        A = Account(D, 'New Account', '', '', category='Other', notes='', date=date)
        self.AccountsPage.add_accounts(D)
        self.__Accounts.append(A)
        self.SearchBar.set_results([A.get_name() for A in self.__Accounts])
        # show new account for editing
        self.EditPage.show_account(A)
        self.AccountsPage.deselect_accounts()
        A.get_display().select()
        self.EditPage.to_edit()
        self.EditPage.Button.switch2()

    def delete_account(self, account_name:str):
        '''
        Purpose:
            called by clicking delete button in AccountDisplay
            removes the Account from everywhere
            sets EditPage to inactive if the account being viewed is deleted
        Pre-conditions:
            :param account_name: str - name of account to delete
        Post-conditions:
            deletes account once and for all
        Returns:
            (none)
        '''
        self.AccountsPage.remove_account(account_name)
        for A in self.__Accounts:
            if A.get_name() == account_name:
                if A is self.EditPage.get_active_account():
                    self.EditPage.to_inactive_page()
                self.__Accounts.remove(A)
                break
        self.save_accounts(repack=False)

    def get_account_names(self):
        '''
        Purpose:
            gets list of all account names
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return: list of str - account names
        '''
        return [A.get_name() for A in self.__Accounts]

    def select_account(self, account_name:str):
        '''called when an account is selected via search bar or display list'''
        for A in self.__Accounts:
            if A.get_name() == account_name:
                if self.EditPage.unsaved_changes() and not messagebox.askyesno(title='Unsaved Changes', messsage=self.__unsaved_message):
                    return # don't show new account if there are unsasved changes the user wants to keep
                self.EditPage.show_account(A)
                self.AccountsPage.deselect_accounts()
                A.get_display().select()
                break

    def toggle_generator_frame(self, turn_on:bool):
        '''show/hide password generator frame based on turn_on'''
        if turn_on:
            self.GeneratorFrame.pack(side='bottom', fill='x')
        else:
            self.GeneratorFrame.pack_forget()
    
    def login(self):
        '''
        Purpose:
            login and show home page - so long as login credentials are correct
        Pre-conditions:
            (none)
        Post-conditions:
            goes to home page if login credentials are correct
        Returns:
            (none)
        '''
        if self.LoginPage.get_password() != self.__EncodingManager.raw_decode('wYe[+t') or self.LoginPage.get_key() == '':
            self.LoginPage.increment_attempts()
            return # incorrect password, cant login
        self.__logged_in = True
        self.LoginPage.pack_forget()
        self.home_frame.pack(fill='both', expand=True)
        self.__EncodingManager.initiate_chars(self.LoginPage.get_key())
        self.Timer.restart()
        self.SearchBar.Entry.activate(focus=True)

    def lockout(self):
        '''called when session time expires due to inactivity - goes to login page'''
        if self.__logged_in: # dont do lockout process if already locked out
            self.__logged_in = False
            self.home_frame.pack_forget()
            self.LoginPage.pack(fill='both', expand=True)
            self.LoginPage.reset_attempts()
            self.LoginPage.clear()
            self.LoginPage.password_focus()

    def window_destroy(self):
        '''called when projects window is closed'''
        if self.EditPage.unsaved_changes():
            m = 'There are unsaved changes Exiting will discard all unsaved changes. Would you like to exit anyway?'
            if not messagebox.askyesno(title='Unsaved Changes', message=m, default='no'):
                return # do not exit app
        self.destroy()

root = App()
