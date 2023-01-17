import customtkinter
import tkinter as tk
from tkinter import ttk
from functools import partial
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
        win_w, win_h = 800, 567

        self.search_frame = customtkinter.CTkFrame(self)
        self.search_frame.grid(column=0, row=0, padx=5, pady=5, sticky='n')
        self.search_label = customtkinter.CTkLabel(self.search_frame, text='Search by name: ')
        self.search_label.grid(column=0, columnspan=3, row=0)
        self.search_subframe = customtkinter.CTkFrame(self.search_frame)
        self.search_subframe.grid(column=0, row=1, padx=4)
        self.radio_var = tk.IntVar()
        self.radio_var.set(0)
        radio_size = {'radiobutton_width': 20, 'radiobutton_height': 20, 'border_width_unchecked': 3, 'border_width_checked': 6}
        self.radio_button_0 = customtkinter.CTkRadioButton(self.search_subframe, text='Ammo', variable=self.radio_var, value=0, **radio_size)
        self.radio_button_0.grid(column=0, row=0, pady=8)
        self.radio_button_1 = customtkinter.CTkRadioButton(self.search_subframe, text='Weapon', variable=self.radio_var, value=1, **radio_size)
        self.radio_button_1.grid(column=1, row=0, pady=8)
        self.entry = customtkinter.CTkEntry(self.search_subframe)
        self.entry.grid(column=0, row=1, padx=8, ipadx=9, pady=(0, 8))
        self.entry.bind('<Return>', self.submit_entry)
        self.submit_button = customtkinter.CTkButton(self.search_subframe, text='Submit', command=self.submit_entry, width=100)
        self.submit_button.grid(column=1, row=1, padx=(0, 8), pady=(0, 8))
        self.results_label = customtkinter.CTkLabel(self.search_frame, text='')
        self.results_label.grid(column=0, row=3, columnspan=3)

        self.cartridge_frame = customtkinter.CTkFrame(self)
        self.cartridge_frame.grid(column=0, row=1, padx=5, sticky='n')
        self.cartridge_label = customtkinter.CTkLabel(self.cartridge_frame, text='Search by cartridge:')
        self.cartridge_label.grid(column=0, columnspan=2, row=0)
        self.rifle_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.rifle_frame.grid(column=0, row=1, rowspan=3, sticky='n', padx=4, pady=(0, 4))
        self.rifle_label = customtkinter.CTkLabel(self.rifle_frame, text='Rifle')
        self.rifle_label.grid()
        self.gl_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.gl_frame.grid(column=0, row=3, sticky='s', padx=4, pady=4)
        self.gl_label = customtkinter.CTkLabel(self.gl_frame, text='GL')
        self.gl_label.grid()
        self.shotgun_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.shotgun_frame.grid(column=1, row=1, padx=(0, 5), pady=(0, 4))
        self.shotgun_label = customtkinter.CTkLabel(self.shotgun_frame, text='Shotgun')
        self.shotgun_label.grid()
        self.pistol_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.pistol_frame.grid(column=1, row=2, padx=(0, 5), pady=4)
        self.pistol_label = customtkinter.CTkLabel(self.pistol_frame, text='Pistol')
        self.pistol_label.grid()
        self.pdw_frame = customtkinter.CTkFrame(self.cartridge_frame)
        self.pdw_frame.grid(column=1, row=3, padx=(0, 5), pady=4)
        self.pdw_label = customtkinter.CTkLabel(self.pdw_frame, text='PDW')
        self.pdw_label.grid()
        self.cartridge_frame_map = {
            self.rifle_frame: ['9x39mm', '.366 TKM', '5.45x39mm', '5.56x45mm NATO', '.300 Blackout', '7.62x39mm',
                               '7.62x51mm NATO', '7.62x54mmR', '.338 Lapua Magnum', '12.7x55mm STs-130'],
            self.gl_frame: ['40x46 mm'],
            self.shotgun_frame: ['12/70', '20/70', '23x75mm'],
            self.pistol_frame: ['7.62x25mm Tokarev', '9x18mm Makarov', '9x19mm Parabellum', '9x21mm Gyurza', '.45 ACP'],
            self.pdw_frame: ['4.6x30mm HK', '5.7x28mm FN']
        }
        for frame, cartridges in self.cartridge_frame_map.items():
            for cartridge in cartridges:
                customtkinter.CTkButton(frame, text=cartridge, command=partial(self.submit_cartridge, cartridge),
                                        width=130, height=25).grid(padx=4, pady=(0, 4))

        self.ammo_tree_frame = customtkinter.CTkFrame(self)
        self.ammo_tree_frame.grid(column=1, row=0, rowspan=2, sticky='n', pady=5)
        self.ammo_tree_label = customtkinter.CTkLabel(self.ammo_tree_frame, text='Ammunition')
        self.ammo_tree_label.grid(column=0, row=0)
        self.ammo_tree = CustomTreeview(self.ammo_tree_frame, height=11, columns=('Cartridge', 'Name', 'Dmg', 'Pen', 'Frag'))
        self.ammo_tree.grid(column=0, row=1)
        self.ammo_tree.column('#0', width=0, stretch=0)
        self.ammo_tree.column('Cartridge', **self.get_width_kwargs(120))
        self.ammo_tree.column('Name', **self.get_width_kwargs(210))
        self.ammo_tree.column('Dmg', **self.get_width_kwargs(50))
        self.ammo_tree.column('Pen', **self.get_width_kwargs(50))
        self.ammo_tree.column('Frag', **self.get_width_kwargs(50))
        self.ammo_tree.heading('Cartridge', text='Cartridge', sort_by='name')
        self.ammo_tree.heading('Name', text='Name', sort_by='name')
        self.ammo_tree.heading('Dmg', text='Dmg', sort_by='x')
        self.ammo_tree.heading('Pen', text='Pen', sort_by='number')
        self.ammo_tree.heading('Frag', text='Frag', sort_by='percent')
        self.ammo_tree_scroll = customtkinter.CTkScrollbar(self.ammo_tree_frame, command=self.ammo_tree.yview)
        self.ammo_tree_scroll.grid(column=1, row=1, ipady=24)
        self.ammo_tree.configure(yscrollcommand=self.ammo_tree_scroll.set)
        self.ammo_tree.bind('<Button-1>', self.separator_lock)
        self.ammo_tree.bind('<Motion>', self.separator_lock)

        self.weapon_tree_frame = customtkinter.CTkFrame(self)
        self.weapon_tree_frame.grid(column=1, row=1, sticky='s')
        self.weapon_tree_label = customtkinter.CTkLabel(self.weapon_tree_frame, text='Weaponry')
        self.weapon_tree_label.grid(column=0, row=0)
        self.weapon_tree = CustomTreeview(self.weapon_tree_frame, height=11, columns=('Cartridge', 'Name', 'Type', 'Recoil', 'Ergo', 'RPM'))
        self.weapon_tree.grid(column=0, row=1)
        self.weapon_tree.column('#0', width=0, stretch=0)
        self.weapon_tree.column('Cartridge', **self.get_width_kwargs(120))
        self.weapon_tree.column('Name', **self.get_width_kwargs(120))
        self.weapon_tree.column('Type', **self.get_width_kwargs_difference(210, 120))
        self.weapon_tree.column('Recoil', **self.get_width_kwargs(50))
        self.weapon_tree.column('Ergo', **self.get_width_kwargs(50))
        self.weapon_tree.column('RPM', **self.get_width_kwargs(50))
        self.weapon_tree.heading('Cartridge', text='Cartridge', sort_by='name')
        self.weapon_tree.heading('Name', text='Name', sort_by='name')
        self.weapon_tree.heading('Type', text='Type', sort_by='name')
        self.weapon_tree.heading('Recoil', text='Recoil', sort_by='number')
        self.weapon_tree.heading('Ergo', text='Ergo', sort_by='number')
        self.weapon_tree.heading('RPM', text='RPM', sort_by='number')
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
                self.ammo_tree, [1, 2, 3, 4, 5])
            self.execute_and_populate(
                "SELECT DISTINCT w.caliber, w.name, w.type, w.recoil, w.ergo, w.rpm "
                "FROM Weapons AS w "
                "JOIN Ammo AS a "
                "ON a.caliber = w.caliber "
                f"WHERE a.name LIKE '%{entry}%'",
                self.weapon_tree, [0, 1, 2, 3, 4, 5])

        elif self.radio_var.get() == 1:
            self.execute_and_populate(
                "SELECT DISTINCT a.caliber, a.name, a.dmg, a.pen, a.frag "
                "FROM Ammo AS a "
                "JOIN Weapons AS w "
                "ON w.caliber = a.caliber "
                f"WHERE w.name LIKE '%{entry}%'",
                self.ammo_tree, [0, 1, 2, 3, 4])
            self.execute_and_populate(
                f"SELECT * FROM Weapons WHERE name LIKE '%{entry}%'",
                self.weapon_tree, [3, 1, 2, 4, 5, 6])

        self.count_results()

    def query_cartridge(self, cartridge):
        self.ammo_tree.delete(*self.ammo_tree.get_children())
        self.weapon_tree.delete(*self.weapon_tree.get_children())

        self.execute_and_populate(
            f"SELECT * FROM Ammo WHERE caliber = '{cartridge}'",
            self.ammo_tree, [1, 2, 3, 4, 5])
        self.execute_and_populate(
            f"SELECT * FROM Weapons WHERE caliber = '{cartridge}'",
            self.weapon_tree, [3, 1, 2, 4, 5, 6])

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

    @staticmethod
    def get_width_kwargs_difference(width1, width2):
        return {'width': width1 - width2,
                'minwidth': width1 - width2,
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
        if sort_by and not hasattr(kwargs, "command"):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs["command"] = partial(func, column, False)
        return super().heading(column, anchor='w', **kwargs)

    def _sort(self, column, reverse, data_type, callback):
        items = [(self.set(k, column), k) for k in self.get_children("")]
        items.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(items):
            self.move(k, "", index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str, self._sort_by_name)

    def _sort_by_number(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_number)

    def _sort_by_x(self, column, reverse):
        def _x_to_number(string):
            split = string.split("x")
            if len(split) > 1:
                return int(split[0]) * int(split[1])
            else:
                return int(split[0])
        self._sort(column, reverse, _x_to_number, self._sort_by_x)

    def _sort_by_percent(self, column, reverse):
        def _percent_to_number(string):
            return int(string.replace("%", ""))
        self._sort(column, reverse, _percent_to_number, self._sort_by_percent)


if __name__ == '__main__':
    app = App()
    app.mainloop()
