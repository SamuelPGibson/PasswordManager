from tkinter import Frame, Label, messagebox
from chichitk import EditLabel, DoubleIconButton, brighten


from utils.info import colors, font_name_bold, font_size_header
from utils.accounts import Account
from utils.entry_field import EntryField, BoxField
from utils.encoding_manager import EncodingManager


class EditPage(Frame):
    def __init__(self, master, bg, EncodingManager:EncodingManager,
                 save_function, account_names_function,
                 inactive_fg=colors['inactive_icon'],
                 top_bg=colors['background1'], top_hover_bg='#aaaaaa',
                 entry_bg=colors['background4'], header_fg='#ffffff',
                 entry_width=38):
        '''page to edit properties of existing account or create new account'''
        Frame.__init__(self, master, bg=bg)
        self.__save_function = save_function # saves accounts to database and repacks AccountsPage
        self.__EncodingManager = EncodingManager
        self.__Account: Account = None # Account object if an account is loaded
        self.__active = False # True when an account is loaded
        self.__editing = False # True when the current account is being edited

        self.inactive_page = Label(self, text='No Account Selected', bg=bg,
                                   fg=inactive_fg, font=(font_name_bold, font_size_header))
        self.inactive_page.pack(fill='both', expand=True)

        # Main Page
        self.main_page = Frame(self, bg=bg)

        cf = lambda s: self.__Account == None or s == self.__Account.get_name() or s not in account_names_function()
        self.__Name = EditLabel(self.main_page, 'Account Name', bg=top_bg,
                                hover_bg=top_hover_bg, fg=header_fg,
                                editable=self.__editing, font_name=font_name_bold,
                                font_size=font_size_header, justify='center',
                                check_function=cf)
        self.__Name.pack(side='top', fill='x')

        self.__Username = EntryField(self.main_page, 'Username', bg, entry_bg,
                                     active=self.__editing, entry_width=entry_width)
        self.__Username.pack(side='top', fill='both', expand=True)

        self.__Password = EntryField(self.main_page, 'Password', bg, entry_bg,
                                     active=self.__editing, entry_width=entry_width)
        self.__Password.pack(side='top', fill='both', expand=True)

        self.__Category = EntryField(self.main_page, 'Category', bg, entry_bg,
                                     active=self.__editing, entry_width=entry_width)
        self.__Category.pack(side='top', fill='both', expand=True)

        self.__Notes = BoxField(self.main_page, 'Notes', bg, entry_bg,
                                active=self.__editing, line_numbers_labels=False,
                                entry_width=entry_width + 4, entry_height=4, wrap='word')
        self.__Notes.pack(side='top', fill='both', expand=True)

        self.Button = DoubleIconButton(self.main_page, 'icons\\edit.png',
                                       'icons\\save.png', self.to_edit, self.save,
                                       label1='Edit', label2='Save',
                                       popup_label1='Edit Fields',
                                       popup_label2='Save Account',
                                       inactive_bg=bg)
        self.Button.pack(side='bottom', pady=8)

        # Set Tab order - doesnt work - there is an automatic tab order
        # self.__Username.get_entry().bind("<Tab>", lambda e: self.__Password.get_entry().focus())
        # self.__Password.get_entry().bind("<Tab>", lambda e: self.__Category.get_entry().focus())
        # self.__Category.get_entry().bind("<Tab>", lambda e: self.__Notes.get_entry().focus())
        # self.__Notes.get_entry().bind("<Return>", lambda e: self.Button.Button2.click_button)

    def to_static(self):
        '''
        Purpose:
            makes page un-editable
        Pre-conditions:
            (none)
        Post-conditions:
            changes status of fields to un-editable
        Returns:
            (none)
        '''
        self.__editing = False
        for Field in [self.__Name, self.__Username, self.__Password, self.__Category, self.__Notes]:
            Field.set_inactive()

    def to_edit(self):
        '''
        Purpose:
            makes page editable
        Pre-conditions:
            (none)
        Post-conditions:
            changes status of fields to editable
        Returns:
            (none)
        '''
        self.__editing = True
        for Field in [self.__Name, self.__Username, self.__Password, self.__Category, self.__Notes]:
            Field.set_active()

    def to_inactive_page(self):
        '''
        Purpose:
            switches to inactive page which says, "No Account Selected"
        Pre-conditions:
            (none)
        Post-conditions:
            switches to inactive page which says, "No Account Selected"
        Returns:
            (none)
        '''
        self.__active = False
        self.to_static()
        self.main_page.pack_forget()
        self.inactive_page.pack(fill='both', expand=True)

    def save(self):
        '''
        Purpose:
            called when save button is clicked
            saves changes to self.__Account, so long as all fields are complete
            gives error to user if there are any empty fields
        Pre-conditions:
            (none)
        Post-conditions:
            changes fields to static after saving
            could show error to user if there are any empty fields
        Returns:
            (none)
        '''
        message = '{} field is empty! You must complete all fields before saving.'
        fields = [self.__Name.get(), self.__Username.get_text(), self.__Password.get_text(),
                  self.__Category.get_text(), self.__Notes.get_text()]
        labels = ['Account Name', 'Username', 'Password', 'Category', 'Notes']
        for field, label in zip(fields, labels):
            if field == '':
                self.Button.switch2() # stay on 'save' button
                messagebox.showerror(title='Incomplete Field', message=message.format(label))
                return # cannot save with empty fields
        self.to_static()
        if self.unsaved_changes():
            self.__Account.set_name(self.__Name.get())
            self.__Account.set_username(self.__Username.get_text())
            self.__Account.set_password(self.__EncodingManager.encode(self.__Password.get_text()))
            self.__Account.set_category(self.__Category.get_text())
            self.__Account.set_notes(self.__Notes.get_text())
            self.__save_function()

    def show_account(self, Account:Account):
        '''
        Purpose:
            display account information in EditPage
            account information is displayed static - uneditable mode
        Pre-conditions:
            :param Account : Account object - contains information do display
        Post-conditions:
            changes information displayed in EditPage
            discards previous Account if there is one
        Returns:
            (none)
        '''
        if not self.__active:
            self.inactive_page.pack_forget()
            self.main_page.pack(fill='both', expand=True)
        self.Button.switch1() # switch button to 'edit'
        self.to_static() # switch static mode
        self.__Account = Account
        # update fields
        bg = self.__Account.get_color()
        info = self.__Account.get_info_dict()
        self.__Name.set_bg(bg, hover_bg=brighten(bg, 0.1))
        self.__Name.set_text(info['name'])
        self.__Username.set_text(info['username'])
        self.__Password.set_text(self.__EncodingManager.decode(info['password']))
        self.__Category.set_text(info['category'])
        self.__Notes.set_text(info['notes'])
        
    def unsaved_changes(self):
        '''
        Purpose:
            checks if there is an account loaded with unsaved changes
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return: bool - True if there are unsaved changes, otherwise False
        '''
        if self.__Account == None:
            return False
        # check each entry box which each attribute of __Account
        info = self.__Account.get_info_dict()
        if self.__Name.get() != info['name']:
            return True
        if self.__Username.get_text() != info['username']:
            return True
        if self.__Password.get_text() != self.__EncodingManager.decode(info['password']):
            return True
        if self.__Category.get_text() != info['category']:
            return True
        if self.__Notes.get_text() != info['notes']:
            return True
        return False

    def get_active_account(self):
        '''
        Purpose:
            retrives the account that is currently loaded
            there may be no account loaded, in which case function returns None
        Pre-conditions:
            (none)
        Post-conditions:
            (none)
        Returns:
            :return: Account object or None
        '''
        return self.__Account
