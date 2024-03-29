import customtkinter
import tkinter as tk
from tkinter import ttk
from functools import partial
from cartridges import Cartridges
import sqlite3


customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('dark-blue')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        conn = sqlite3.connect('resources/eft.db')
        self.c = conn.cursor()

        self.title('EFT Munitions')
        self.iconbitmap('resources/ammo.ico')
        self.resizable(False, False)
        win_w, win_h = 782, 592

        self.search_frame = customtkinter.CTkFrame(self)
        self.search_frame.grid(column=0, row=0, padx=5, pady=5, sticky='n')
        self.search_label = customtkinter.CTkLabel(self.search_frame, text='Search by name: ')
        self.search_label.grid(column=0, columnspan=3, row=0)
        self.search_subframe = customtkinter.CTkFrame(self.search_frame)
        self.search_subframe.grid(column=0, row=1, padx=4)
        self.radio_var = tk.IntVar()
        self.radio_var.set(0)
        self.radio_size = {'radiobutton_width': 20, 'radiobutton_height': 20, 'border_width_unchecked': 3, 'border_width_checked': 6}
        self.radio_button_0 = customtkinter.CTkRadioButton(self.search_subframe, text='Ammo', variable=self.radio_var, value=0, **self.radio_size)
        self.radio_button_0.grid(column=0, row=0, pady=8)
        self.radio_button_1 = customtkinter.CTkRadioButton(self.search_subframe, text='Weapon', variable=self.radio_var, value=1, **self.radio_size)
        self.radio_button_1.grid(column=1, row=0, pady=8)
        self.entry = customtkinter.CTkEntry(self.search_subframe)
        self.entry.grid(column=0, row=1, padx=6, ipadx=5, pady=(0, 8))
        self.entry.bind('<Return>', self.submit_entry)
        self.submit_button = customtkinter.CTkButton(self.search_subframe, text='Submit', command=self.submit_entry, width=90)
        self.submit_button.grid(column=1, row=1, padx=(0, 8), pady=(0, 8))
        self.results_label = customtkinter.CTkLabel(self.search_frame, text='.  .  .')
        self.results_label.grid(column=0, row=3, columnspan=3)

        self.cartridge_frame = customtkinter.CTkFrame(self)
        self.cartridge_frame.grid(column=0, row=1, padx=5, sticky='n')
        self.cartridge_label = customtkinter.CTkLabel(self.cartridge_frame, text='Search by cartridge:')
        self.cartridge_label.grid(column=0, columnspan=2, row=0)
        self.rifle_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.rifle_frame.grid(column=0, row=1, rowspan=3, sticky='n', padx=5, pady=(0, 5))
        self.rifle_label = customtkinter.CTkLabel(self.rifle_frame, text='Rifle')
        self.rifle_label.grid()
        self.gl_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.gl_frame.grid(column=0, row=3, sticky='s', padx=5, pady=(0, 5))
        self.gl_label = customtkinter.CTkLabel(self.gl_frame, text='GL')
        self.gl_label.grid()
        self.shotgun_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.shotgun_frame.grid(column=1, row=1, padx=(0, 5), pady=(0, 5))
        self.shotgun_label = customtkinter.CTkLabel(self.shotgun_frame, text='Shotgun')
        self.shotgun_label.grid()
        self.pistol_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.pistol_frame.grid(column=1, row=2, padx=(0, 5), pady=(0, 5))
        self.pistol_label = customtkinter.CTkLabel(self.pistol_frame, text='Pistol')
        self.pistol_label.grid()
        self.pdw_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.pdw_frame.grid(column=1, row=3, padx=(0, 5), pady=(0, 5))
        self.pdw_label = customtkinter.CTkLabel(self.pdw_frame, text='PDW')
        self.pdw_label.grid()

        self.cartridges = Cartridges()
        self.cartridge_frame_map = {
            self.rifle_frame:   self.cartridges.map['rifle'].values(),
            self.gl_frame:      self.cartridges.map['gl'].values(),
            self.shotgun_frame: self.cartridges.map['shotgun'].values(),
            self.pistol_frame:  self.cartridges.map['pistol'].values(),
            self.pdw_frame:     self.cartridges.map['pdw'].values()}
        seen = set()
        for frame, cartridges in self.cartridge_frame_map.items():
            for cartridge in cartridges:
                if cartridge not in seen:
                    seen.add(cartridge)
                    customtkinter.CTkButton(frame, text=cartridge, command=partial(self.submit_cartridge, cartridge),
                                            width=120, height=25).grid(padx=4, pady=(0, 4))

        self.ammo_tree_frame = customtkinter.CTkFrame(self)
        self.ammo_tree_frame.grid(column=1, row=0, rowspan=2, sticky='n', pady=5)
        self.ammo_tree_label = customtkinter.CTkLabel(self.ammo_tree_frame, text='Ammunition')
        self.ammo_tree_label.grid(column=0, row=0)
        self.ammo_tree_columns = {
            'Cartridge': (90, 'name'),
            'Name': (140, 'name'),
            'Dmg': (50, 'number'),
            'Pen': (50, 'number'),
            'Acc': (50, 'number'),
            'Rec': (50, 'number'),
            'Frag': (50, 'number')}
        self.ammo_tree = CustomTreeview(self.ammo_tree_frame, height=11, columns=tuple(self.ammo_tree_columns))
        self.ammo_tree.grid(column=0, row=1)
        self.ammo_tree.column('#0', width=0, stretch=0)
        for column, (width, sort_by) in self.ammo_tree_columns.items():
            self.ammo_tree.column(column, **self.get_width_kwargs(width))
            self.ammo_tree.heading(column, text=column, sort_by=sort_by)
        self.ammo_tree_scroll = customtkinter.CTkScrollbar(self.ammo_tree_frame, command=self.ammo_tree.yview)
        self.ammo_tree_scroll.grid(column=1, row=1, ipady=24)
        self.ammo_tree.configure(yscrollcommand=self.ammo_tree_scroll.set)
        self.ammo_tree.bind('<Button-1>', self.separator_lock)
        self.ammo_tree.bind('<Motion>', self.separator_lock)

        self.weapon_tree_frame = customtkinter.CTkFrame(self)
        self.weapon_tree_frame.grid(column=1, row=1, sticky='s')
        self.weapon_tree_label = customtkinter.CTkLabel(self.weapon_tree_frame, text='Weaponry')
        self.weapon_tree_label.grid(column=0, row=0)
        self.weapon_tree_columns = {
            'Cartridge': (90, 'name'),
            'Name': (140, 'name'),
            'Type': (100, 'name'),
            'Rec': (50, 'number'),
            'Ergo': (50, 'number'),
            'RPM': (50, 'number')}
        self.weapon_tree = CustomTreeview(self.weapon_tree_frame, height=11, columns=tuple(self.weapon_tree_columns))
        self.weapon_tree.grid(column=0, row=1)
        self.weapon_tree.column('#0', width=0, stretch=0)
        for column, (width, sort_by) in self.weapon_tree_columns.items():
            self.weapon_tree.column(column, **self.get_width_kwargs(width))
            self.weapon_tree.heading(column, text=column, sort_by=sort_by)
        self.weapon_tree_scroll = customtkinter.CTkScrollbar(self.weapon_tree_frame, command=self.weapon_tree.yview)
        self.weapon_tree_scroll.grid(column=1, row=1, ipady=24)
        self.weapon_tree.configure(yscrollcommand=self.weapon_tree_scroll.set)
        self.weapon_tree.bind('<Button-1>', self.separator_lock)
        self.weapon_tree.bind('<Motion>', self.separator_lock)

        win_x = int((self.winfo_screenwidth() / 2) - (win_w / 2))
        win_y = int((self.winfo_screenheight() / 2) - (win_h / 2) - 40)
        self.attributes('-topmost', True)
        self.geometry(f"{win_w}x{win_h}+{win_x}+{win_y}")
        self.update()
        self.attributes('-topmost', False)

    def count_results(self):
        rows = len(self.ammo_tree.get_children()) + len(self.weapon_tree.get_children())
        self.results_label.configure(text=f"Found {rows} results")

    def execute_and_populate(self, query, tree, col_indices):
        self.c.execute(query)
        for col in self.c.fetchall():
            values = [col[i] for i in col_indices]
            tree.insert(parent='', index='end', text='', values=values)

    def query_entry(self, entry):
        self.ammo_tree.delete(*self.ammo_tree.get_children())
        self.weapon_tree.delete(*self.weapon_tree.get_children())

        if self.entry.get() == '' or self.entry.get() == ' ':
            self.count_results()

        elif self.radio_var.get() == 0:
            self.execute_and_populate(
                f"SELECT * FROM Ammo WHERE name LIKE '%{entry}%'",
                self.ammo_tree, [2, 3, 4, 5, 6, 7, 8])
            self.execute_and_populate(
                "SELECT DISTINCT w.caliber, w.name, w.type, w.rec, w.ergo, w.rpm "
                "FROM Weapons AS w "
                "JOIN Ammo AS a "
                "ON a.caliber = w.caliber "
                f"WHERE a.name LIKE '%{entry}%'",
                self.weapon_tree, [0, 1, 2, 3, 4, 5])

        elif self.radio_var.get() == 1:
            self.execute_and_populate(
                "SELECT DISTINCT a.caliber, a.name, a.dmg, a.pen, a.acc, a.rec, a.frag "
                "FROM Ammo AS a "
                "JOIN Weapons AS w "
                "ON w.caliber = a.caliber "
                f"WHERE w.name LIKE '%{entry}%'",
                self.ammo_tree, [0, 1, 2, 3, 4, 5, 6])
            self.execute_and_populate(
                f"SELECT * FROM Weapons WHERE name LIKE '%{entry}%'",
                self.weapon_tree, [2, 3, 4, 5, 6, 7])

        self.count_results()

    def query_cartridge(self, cartridge):
        self.ammo_tree.delete(*self.ammo_tree.get_children())
        self.weapon_tree.delete(*self.weapon_tree.get_children())

        self.execute_and_populate(
            f"SELECT * FROM Ammo WHERE caliber = '{cartridge}'",
            self.ammo_tree, [2, 3, 4, 5, 6, 7, 8])
        self.execute_and_populate(
            f"SELECT * FROM Weapons WHERE caliber = '{cartridge}'",
            self.weapon_tree, [2, 3, 4, 5, 6, 7])

        self.count_results()

    def submit_entry(self, *_):
        self.query_entry(self.entry.get())
        self.entry.delete(0, 'end')

    def submit_cartridge(self, cartridge):
        self.query_cartridge(cartridge)

    def separator_lock(self, event):
        if self.ammo_tree.identify_region(event.x, event.y) == 'separator' or \
                self.weapon_tree.identify_region(event.x, event.y) == 'separator':
            return 'break'

    @staticmethod
    def get_width_kwargs(width):
        return {'width': width,
                'minwidth': width,
                'stretch': 0}


class CustomTreeview(ttk.Treeview):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure(
            'Treeview',
            fieldbackground=customtkinter.ThemeManager.theme['CTkFrame']['fg_color'][1],
            background=customtkinter.ThemeManager.theme['CTkFrame']['fg_color'][1],
            foreground=customtkinter.ThemeManager.theme['CTkLabel']['text_color'][1],
            borderwidth=0
        )
        treestyle.map(
            'Treeview',
            background=[('selected', customtkinter.ThemeManager.theme['CTkButton']['fg_color'][1])],
            foreground=[('selected', customtkinter.ThemeManager.theme['CTkButton']['text_color'][1])]
        )
        treestyle.configure(
            'Treeview.Heading',
            background=customtkinter.ThemeManager.theme['CTkButton']['fg_color'][1],
            foreground=customtkinter.ThemeManager.theme['CTkButton']['text_color'][1],
            relief='flat',
            borderwidth=6
        )
        treestyle.map(
            'Treeview.Heading',
            background=[('active', customtkinter.ThemeManager.theme["CTkButton"]["hover_color"][1])]
        )

    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            kwargs['command'] = partial(self._sort, column, sort_by)
        return super().heading(column, anchor='w', **kwargs)

    def _sort(self, column, sort_by, reverse=False):
        data = {
            'name': str,
            'number': lambda x: int(x.replace('%', '')) if str else int,
        }.get(sort_by, None)

        items = [(self.set(k, column), k) for k in self.get_children('')]
        items.sort(key=lambda t: data(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(items):
            self.move(k, '', index)
        self.heading(column, command=partial(self._sort, column, sort_by, not reverse))


if __name__ == '__main__':
    app = App()
    app.mainloop()
