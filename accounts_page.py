from tkinter import Frame, Label
from chichitk import ScrollableFrame, IconButton


from utils.info import colors, font_name, font_name_bold, font_size_normal, font_size_header
from utils.accounts import AccountDisplay


class ListSeparator(Frame):
    def __init__(self, master, text:str, bg:str, fg:str=colors['inactive_icon'],
                 line_color:str=colors['background4'], line_width=2, padx=1, pady=1):
        '''frame to separate categories in accounts listing
        such as "Category ---------------------------------"
        '''
        Frame.__init__(self, master, bg=bg, padx=padx, pady=pady)
        self.__text = text

        Label(self, text=self.__text + ' ', bg=bg, fg=fg,
              font=(font_name, font_size_normal)).pack(side='left')
        Frame(self, bg=line_color, height=line_width).pack(side='left', fill='x', expand=True) # divider line

    def get_text(self) -> str:
        '''
        Purpose:
            returns separator text
        '''
        return self.__text

class AccountsPage(Frame):
    ''' Page to display list of accounts
    '''
    def __init__(self, master, bg, top_bg=colors['background1'],
                 header_fg='#ffffff', inactive_fg=colors['inactive_icon']):
        self.bg = bg
        Frame.__init__(self, master, bg=self.bg)
        self.__Accounts: list[AccountDisplay] = [] # all accounts
        self.Accounts: list[AccountDisplay] = [] # only accounts currently displayed - controlled by search bar
        self.Separators: list[ListSeparator] = []
        
        header_label = Label(self, text='Accounts', bg=top_bg, fg=header_fg,
                             font=(font_name_bold, font_size_header))
        header_label.pack(side='top', fill='x')

        self.inactive_page = Label(self, text='No Search Results', bg=bg,
                                   fg=inactive_fg, font=(font_name_bold, font_size_header))

        self.main_page = Frame(self, bg=bg)
        self.main_page.pack(fill='both', expand=True)

        buttons_frame = Frame(self.main_page, bg=bg)
        buttons_frame.pack(side='top', fill='x')
        NameButton = IconButton(buttons_frame, 'icons\\arrow_down.png',
                                self.reorder_name, label='Name', bar_height=3,
                                inactive_bg=bg, popup_label='Order by Account Name')
        TypeButton = IconButton(buttons_frame, 'icons\\arrow_down.png',
                                self.reorder_type, label='Type', bar_height=3,
                                inactive_bg=bg, popup_label='Order by Category')
        DateButton = IconButton(buttons_frame, 'icons\\arrow_down.png',
                                self.reorder_date, label='Date', bar_height=3,
                                inactive_bg=bg, popup_label='Order by Date')
        NameButton.pack(side='left', fill='x', expand=True)
        TypeButton.pack(side='left', fill='x', expand=True)
        DateButton.pack(side='left', fill='x', expand=True)
        self.__order_buttons = [NameButton, TypeButton, DateButton]

        self.scroll_frame = ScrollableFrame(self.main_page, bg,
                                            include_scrollbar=True,
                                            scrollbar_side='right',
                                            yscrollincrement=1)
        self.scroll_frame.pack(side='top', fill='both', expand=True)
        self.main_frame = self.scroll_frame.scrollable_frame # all account listings go in main_frame
        self.bind_all('<MouseWheel>', self.scroll_frame.on_mousewheel)

        NameButton.click_button()

    def add_accounts(self, accounts:list):
        '''
        Purpose:
            add accounts to display list
            removes and re-packs all existing accounts
            accounts must already be initialized with self.main_frame as master
        Pre-conditions:
            accounts : list of AccountDisplay objects or a single AccountDisplay object - accounts to be added
        Post-conditions:
            adds accounts to display list
        Returns:
            (none)
        '''
        if isinstance(accounts, list):
            self.__Accounts.extend(accounts)
        else:
            self.__Accounts.append(accounts)
        self.Accounts = self.__Accounts # display all accounts - regardless of search bar status
        self.repack_accounts()

    def remove_account(self, account_name:str):
        '''
        Purpose:
            removes account with the specified name from accounts list
        Pre-conditions:
            :param account_name : str - name of account to remove
        Post-conditions:
            removes an account from the list
        Returns:
            (none)
        '''
        for Account in self.__Accounts:
            if Account.get_name() == account_name:
                Account.pack_forget()
                self.__Accounts.remove(Account)
                if Account in self.Accounts: # removed account is one of the accounts currently displayed
                    i = self.Accounts.index(Account)
                    # if Account is the last in its category, remove separator
                    if self.categories.count(self.categories[i]) == 1:
                        for S in self.Separators:
                            if S.get_text() == self.categories[i]:
                                S.pack_forget()
                                self.Separators.remove(S)
                                break
                    del self.Accounts[i]
                    del self.categories[i]
                break

    def show_accounts(self, account_names:list):
        '''
        Purpose:
            displays only the accounts corresponding to names in account_names
            removes accounts who's names are not in account_names
            all accounts are still stored, but only those in account_names are displayed
            if account_names is an empty list, displays text "No Search Results"
        Pre-conditions:
            :param account_names: list or str - names of accounts to display
        Post-conditions:
            changes account displayed in accounts listing
        Returns:
            (none)
        '''
        self.Accounts = [A for A in self.__Accounts if A.get_name() in account_names]
        self.repack_accounts()
        self.scroll_frame.canvas.yview_moveto(0)

    def show_all_accounts(self):
        '''
        Purpose:
            called when X is clicked to clear scrollbar
            shows all accounts in accounts listing
        Pre-conditions:
            (none)
        Post-conditions:
            shows all accounts in accounts listing
        Returns:
            (none)
        '''
        self.Accounts = self.__Accounts
        self.repack_accounts()

    def remove_all_widgets(self):
        '''
        Purpose:
            removes all AccountDisplay objects and Separators from page
        Pre-conditions:
            (none)
        Post-conditions:
            removes everything from page
        Returns:
            (none)
        '''
        for A in self.__Accounts:
            A.pack_forget()
        for S in self.Separators:
            S.pack_forget()
        self.Separators = []

    def pack_accounts(self):
        '''
        Purpose:
            display list of account frames - AccountDisplay objects
            called when an account is added, deleted, or ordering is changed
        Pre-conditions:
            (none)
        Post-conditions:
            order of accounts is changed
        Returns:
            (none)
        '''
        self.remove_all_widgets()
        # check if there are no accounts - if so, display inactive Frame
        if len(self.Accounts) == 0:
            self.main_page.pack_forget()
            self.inactive_page.pack(fill='both', expand=True)
            if len(self.__Accounts) == 0: # no accounts exist
                self.inactive_page.config(text='No Accounts')
            else:
                self.inactive_page.config(text='No Search Results')
        else:
            self.inactive_page.pack_forget()
            self.main_page.pack(fill='both', expand=True)

        last_category = None
        for Account, category in zip(self.Accounts, self.categories):
            if category != last_category: # add separator for new category
                S = ListSeparator(self.main_frame, category, self.bg)
                S.pack(side='top', fill='x')
                self.Separators.append(S)
            Account.pack(side='top', fill='x', padx=10, pady=2)
            last_category = category
        # check scroll position at start, scroll back when done
        # scrolll to position of selected account

    def repack_accounts(self):
        '''
        Purpose:
            removes and repacks accounts
            intended to be called when account info is changed - since this could change the order
        Pre-conditions:
            (none)
        Post-conditions:
            may change order of accounts display
        Returns:
            (none)
        '''
        for button in self.__order_buttons:
            if button.selected:
                button.click_button() # sort accounts, set categories, and pack accounts
                break
    
    def deselect_accounts(self):
        '''
        Purpose:
            deselect all accounts in list
        '''
        for A in self.__Accounts:
            A.deselect()

    def deselect_buttons(self):
        '''
        Purpose:
            deselects all order buttons
            called when any button is clicked to deselect other buttons
        '''
        for B in self.__order_buttons:
            B.deselect()

    def reorder_name(self):
        '''
        Purpose:
            called when 'Name' order button is clicked
            reorders accounts in alphabetical order by account name
        Pre-conditions:
            (none)
        Post-conditions:
            changes order of accounts
        Returns:
            (none)
        '''
        self.deselect_buttons()
        self.Accounts.sort(key=lambda A: A.get_name())
        self.categories = [A.get_name()[0].upper() for A in self.Accounts] # start letter of each account
        self.pack_accounts()

    def reorder_type(self):
        '''
        Purpose:
            called when 'Name' order button is clicked
            reorders accounts in alphabetical order by account type
        Pre-conditions:
            (none)
        Post-conditions:
            changes order of accounts
        Returns:
            (none)
        '''
        self.deselect_buttons()
        # sort by name first so that accounts will be in alphabetical order within each category
        self.Accounts.sort(key=lambda A: A.get_name())
        self.Accounts.sort(key=lambda A: A.get_order_category())
        self.categories = [A.get_category() for A in self.Accounts]
        self.pack_accounts()

    def reorder_date(self):
        '''
        Purpose:
            called when 'Name' order button is clicked
            reorders accounts based on date added
        Pre-conditions:
            (none)
        Post-conditions:
            changes order of accounts
        Returns:
            (none)
        '''
        self.deselect_buttons()
        # sort by name first so that accounts will be in alphabetical order within each date category
        self.Accounts.sort(key=lambda A: A.get_name())
        self.Accounts.sort(key=lambda A: A.get_date_year(), reverse=True) # reverse - most recent dates first
        self.categories = [A.get_date_year() for A in self.Accounts] # should get only month or only year
        self.pack_accounts()

