import tkinter as tk
from tkinter import ttk
from functools import partial
import sqlite3


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        conn = sqlite3.connect('resources/eft.db')
        self.c = conn.cursor()

        self.title('EFT Munitions')
        self.iconbitmap('resources/ammo.ico')

        self.resizable(0, 0)
        window_width = 830
        window_height = 520
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coord = int((screen_width / 2) - (window_width / 2))
        y_coord = int((screen_height / 2) - (window_height / 2) - 40)
        self.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

        self.r_var = None
        self.input_field = None
        self.results = None
        self.ammo_tree = None
        self.weapon_tree = None

        self.widgets()

    def widgets(self):
        pad = {'padx': 10, 'pady': 10}
        self.search_frame(pad)
        self.button_frame(pad)
        self.db_frame(pad)

    def search_frame(self, pad):
        search_frame = ttk.Frame(self)
        search_frame.grid(column=0, row=0, **pad)

        search_by = ttk.Label(search_frame, text='Search by name: ')
        search_by.grid(column=0, row=0)

        self.r_var = tk.IntVar()
        self.r_var.set(0)
        ammo_radio = ttk.Radiobutton(search_frame, text='Ammo', variable=self.r_var, value=0)
        ammo_radio.grid(column=1, row=0)
        weapon_radio = ttk.Radiobutton(search_frame, text='Weapon', variable=self.r_var, value=1)
        weapon_radio.grid(column=2, row=0)

        self.input_field = ttk.Entry(search_frame)
        self.input_field.grid(column=0, row=1, columnspan=2, ipadx=15, pady=10)
        self.input_field.bind('<Return>', self.submit_keypress)

        submit = ttk.Button(search_frame, text='Submit', command=self.submit_click)
        submit.grid(column=2, row=1)

        self.results = ttk.Label(search_frame, text='')
        self.results.grid(column=0, row=2, columnspan=3)

    def button_frame(self, pad):
        btn_frame = ttk.Frame(self)
        btn_frame.grid(column=0, row=1, padx=10)

        cartridges = ttk.Label(btn_frame, text='Search by cartridge:')
        cartridges.grid(column=0, row=0, columnspan=2)

        r_f = ttk.Frame(btn_frame)
        r_f.grid(column=0, row=1, rowspan=11, sticky='nw', **pad)
        r_cartridges = ttk.Label(r_f, text='Rifle')
        r_cartridges.grid(sticky='w')
        btn_9x39mm = ttk.Button(r_f, text='9x39mm', command=partial(self.ammo_click, '9x39mm'))
        btn_9x39mm.grid(sticky='w')
        btn_366_tkm = ttk.Button(r_f, text='.366 TKM', command=partial(self.ammo_click, '.366 TKM'))
        btn_366_tkm.grid(sticky='w')
        btn_545x39mm = ttk.Button(r_f, text='5.45x39mm', command=partial(self.ammo_click, '5.45x39mm'))
        btn_545x39mm.grid(sticky='w')
        btn_556x45mm_nato = ttk.Button(r_f, text='5.56x45mm NATO', command=partial(self.ammo_click, '5.56x45mm NATO'))
        btn_556x45mm_nato.grid(sticky='w')
        btn_300_blackout = ttk.Button(r_f, text='.300 Blackout', command=partial(self.ammo_click, '.300 Blackout'))
        btn_300_blackout.grid(sticky='w')
        btn_762x39mm = ttk.Button(r_f, text='7.62x39mm', command=partial(self.ammo_click, '7.62x39mm'))
        btn_762x39mm.grid(sticky='w')
        btn_762x51mm_nato = ttk.Button(r_f, text='7.62x51mm NATO', command=partial(self.ammo_click, '7.62x51mm NATO'))
        btn_762x51mm_nato.grid(sticky='w')
        btn_762x54mmr = ttk.Button(r_f, text='7.62x54mmR', command=partial(self.ammo_click, '7.62x54mmR'))
        btn_762x54mmr.grid(sticky='w')
        btn_338 = ttk.Button(r_f, text='.338 Lapua Magnum', command=partial(self.ammo_click, '.338 Lapua Magnum'))
        btn_338.grid(sticky='w')
        btn_127x55mm = ttk.Button(r_f, text='12.7x55mm STs-130', command=partial(self.ammo_click, '12.7x55mm STs-130'))
        btn_127x55mm.grid(sticky='w')

        gl_f = ttk.Frame(btn_frame)
        gl_f.grid(column=0, row=3, sticky='sw', **pad)
        gl_cartridges = ttk.Label(gl_f, text='GL')
        gl_cartridges.grid(sticky='w')
        btn_40x46mm = ttk.Button(gl_f, text='40x46 mm', command=partial(self.ammo_click, '40x46 mm'))
        btn_40x46mm.grid(sticky='w')

        s_f = ttk.Frame(btn_frame)
        s_f.grid(column=1, row=1, sticky='w', **pad)
        s_cartridges = ttk.Label(s_f, text='Shotgun')
        s_cartridges.grid(sticky='w')
        btn_12_70 = ttk.Button(s_f, text='12/70', command=partial(self.ammo_click, '12/70'))
        btn_12_70.grid(sticky='w')
        btn_20_70 = ttk.Button(s_f, text='20/70', command=partial(self.ammo_click, '20/70'))
        btn_20_70.grid(sticky='w')
        btn_23x75mm = ttk.Button(s_f, text='23x75mm', command=partial(self.ammo_click, '23x75mm'))
        btn_23x75mm.grid(sticky='w')

        p_f = ttk.Frame(btn_frame)
        p_f.grid(column=1, row=2, sticky='w', **pad)
        p_cartridges = ttk.Label(p_f, text='Pistol')
        p_cartridges.grid(sticky='w')
        btn_7_62x25mm = ttk.Button(p_f, text='7.62x25mm Tokarev', command=partial(self.ammo_click, '7.62x25mm Tokarev'))
        btn_7_62x25mm.grid(sticky='w')
        btn_9x18mm = ttk.Button(p_f, text='9x18mm Makarov', command=partial(self.ammo_click, '9x18mm Makarov'))
        btn_9x18mm.grid(sticky='w')
        btn_9x19mm = ttk.Button(p_f, text='9x19mm Parabellum', command=partial(self.ammo_click, '9x19mm Parabellum'))
        btn_9x19mm.grid(sticky='w')
        btn_9x21mm = ttk.Button(p_f, text='9x21mm Gyurza', command=partial(self.ammo_click, '9x21mm Gyurza'))
        btn_9x21mm.grid(sticky='w')
        btn_45_acp = ttk.Button(p_f, text='.45 ACP', command=partial(self.ammo_click, '.45 ACP'))
        btn_45_acp.grid(sticky='w')

        pdw_f = ttk.Frame(btn_frame)
        pdw_f.grid(column=1, row=3, sticky='w', **pad)
        pdw_cartridges = ttk.Label(pdw_f, text='PDW')
        pdw_cartridges.grid(sticky='w')
        button_46x30mm_hk = ttk.Button(pdw_f, text='4.6x30mm HK', command=partial(self.ammo_click, '4.6x30mm HK'))
        button_46x30mm_hk.grid(sticky='w')
        button_57x28mm_fn = ttk.Button(pdw_f, text='5.7x28mm FN', command=partial(self.ammo_click, '5.7x28mm FN'))
        button_57x28mm_fn.grid(sticky='w')

    def db_frame(self, pad):
        db_frame = ttk.Frame(self)
        db_frame.grid(column=1, row=0, rowspan=99, sticky='n', **pad)

        scroll_height = {'ipady': 88}
        cartridge_width = {'width': 120, 'minwidth': 120, 'stretch': 0}
        int_cols_width = {'width': 50, 'minwidth': 50, 'stretch': 0}
        a_name_width = {'width': 210, 'minwidth': 210, 'stretch': 0}
        w_name_width = {'width': 120, 'minwidth': 120, 'stretch': 0}
        w_type_width = {'width': a_name_width['width'] - w_name_width['width'],
                        'minwidth': a_name_width['minwidth'] - w_name_width['minwidth'],
                        'stretch': 0}

        ammo_tree_f = ttk.LabelFrame(db_frame, text="Ammunition")
        ammo_tree_f.grid(column=0, row=0)
        ammo_tree_scroll = ttk.Scrollbar(ammo_tree_f)
        ammo_tree_scroll.grid(column=1, row=0, **scroll_height)
        self.ammo_tree = TvSort(ammo_tree_f,
                                columns=("Cartridge", "Name", "Dmg", "Pen", "Frag"),
                                yscrollcommand=ammo_tree_scroll.set)
        self.ammo_tree.column("#0", width=0, stretch=0)
        self.ammo_tree.column("Cartridge", **cartridge_width)
        self.ammo_tree.column("Name", **a_name_width)
        self.ammo_tree.column("Dmg", **int_cols_width)
        self.ammo_tree.column("Pen", **int_cols_width)
        self.ammo_tree.column("Frag", **int_cols_width)
        self.ammo_tree.heading("Cartridge", text="Cartridge", sort_by="name")
        self.ammo_tree.heading("Name", text="Name", sort_by="name")
        self.ammo_tree.heading("Dmg", text="Dmg", sort_by="x")
        self.ammo_tree.heading("Pen", text="Pen", sort_by="number")
        self.ammo_tree.heading("Frag", text="Frag", sort_by="percent")
        self.ammo_tree.grid(column=0, row=0)
        ammo_tree_scroll.config(command=self.ammo_tree.yview)

        weapon_tree_f = ttk.LabelFrame(db_frame, text="Weaponry")
        weapon_tree_f.grid(column=0, row=1)
        weapon_tree_scroll = ttk.Scrollbar(weapon_tree_f)
        weapon_tree_scroll.grid(column=1, row=0, **scroll_height)
        self.weapon_tree = TvSort(weapon_tree_f,
                                  columns=("Cartridge", "Name", "Type", "Recoil", "Ergo", "RPM"),
                                  yscrollcommand=weapon_tree_scroll.set)
        self.weapon_tree.column("#0", width=0, stretch=0)
        self.weapon_tree.column("Cartridge", **cartridge_width)
        self.weapon_tree.column("Name", **w_name_width)
        self.weapon_tree.column("Type", **w_type_width)
        self.weapon_tree.column("Recoil", **int_cols_width)
        self.weapon_tree.column("Ergo", **int_cols_width)
        self.weapon_tree.column("RPM", **int_cols_width)
        self.weapon_tree.heading("Cartridge", text="Cartridge", sort_by="name")
        self.weapon_tree.heading("Name", text="Name", sort_by="name")
        self.weapon_tree.heading("Type", text="Type", sort_by="name")
        self.weapon_tree.heading("Recoil", text="Recoil", sort_by="number")
        self.weapon_tree.heading("Ergo", text="Ergo", sort_by="number")
        self.weapon_tree.heading("RPM", text="RPM", sort_by="number")
        self.weapon_tree.grid(column=0, row=0)
        weapon_tree_scroll.config(command=self.weapon_tree.yview)

        self.ammo_tree.bind('<Button-1>', self.separator_resize_blocker)
        self.ammo_tree.bind('<Motion>', self.separator_resize_blocker)
        self.weapon_tree.bind('<Button-1>', self.separator_resize_blocker)
        self.weapon_tree.bind('<Motion>', self.separator_resize_blocker)

    def result(self):
        rows = len(self.ammo_tree.get_children()) + len(self.weapon_tree.get_children())
        self.results.config(text=f"Found {rows} results")

    def submit_sql_query(self, query):
        self.ammo_tree.delete(*self.ammo_tree.get_children())
        self.weapon_tree.delete(*self.weapon_tree.get_children())

        if self.input_field.get() == "" or self.input_field.get() == " ":
            self.result()

        elif self.r_var.get() == 0:
            self.c.execute(f"SELECT * FROM Ammo WHERE name LIKE '%{query}%'")
            a_data = self.c.fetchall()
            for col in a_data:
                self.ammo_tree.insert(parent='', index='end', text='',
                                      values=(col[1], col[2], col[3], col[4], col[5]))
            self.c.execute("SELECT DISTINCT w.caliber, w.name, w.type, w.recoil, w.ergo, w.rpm "
                           "FROM Weapons AS w "
                           "JOIN Ammo AS a "
                           "ON a.caliber = w.caliber "
                           f"WHERE a.name LIKE '%{query}%'")
            w_data = self.c.fetchall()
            for col in w_data:
                self.weapon_tree.insert(parent='', index='end', text='',
                                        values=(col[0], col[1], col[2], col[3], col[4], col[5]))

        else:
            self.c.execute("SELECT DISTINCT a.caliber, a.name, a.dmg, a.pen, a.frag "
                           "FROM Ammo AS a "
                           "JOIN Weapons AS w "
                           "ON w.caliber = a.caliber "
                           f"WHERE w.name LIKE '%{query}%'")
            a_data = self.c.fetchall()
            for col in a_data:
                self.ammo_tree.insert(parent='', index='end', text='',
                                      values=(col[0], col[1], col[2], col[3], col[4]))
            self.c.execute(f"SELECT * FROM Weapons WHERE name LIKE '%{query}%'")
            w_data = self.c.fetchall()
            for col in w_data:
                self.weapon_tree.insert(parent='', index='end', text='',
                                        values=(col[3], col[1], col[2], col[4], col[5], col[6]))

        self.result()

    def button_sql_query(self, query):
        self.ammo_tree.delete(*self.ammo_tree.get_children())
        self.weapon_tree.delete(*self.weapon_tree.get_children())

        self.c.execute(f"SELECT * FROM Ammo WHERE caliber = '{query}'")
        a_data = self.c.fetchall()
        for col in a_data:
            self.ammo_tree.insert(parent='', index='end', text='',
                                  values=(col[1], col[2], col[3], col[4], col[5]))
        self.c.execute(f"SELECT * FROM Weapons WHERE caliber = '{query}'")
        w_data = self.c.fetchall()

        for col in w_data:
            self.weapon_tree.insert(parent='', index='end', text='',
                                    values=(col[3], col[1], col[2], col[4], col[5], col[6]))

        self.result()

    def submit_click(self):
        self.submit_sql_query(self.input_field.get())
        self.input_field.delete(0, 'end')

    # noinspection PyUnusedLocal
    def submit_keypress(self, event):
        self.submit_sql_query(self.input_field.get())
        self.input_field.delete(0, 'end')

    def separator_resize_blocker(self, event):
        if self.ammo_tree.identify_region(event.x, event.y) == "separator" or \
                self.weapon_tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def ammo_click(self, cartridge):
        self.button_sql_query(cartridge)


class TvSort(ttk.Treeview):
    def heading(self, column, sort_by=None, anchor='w', **kwargs):
        if sort_by and not hasattr(kwargs, "command"):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs["command"] = partial(func, column, False)
        return super().heading(column, **kwargs)

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


def main():
    GUI().mainloop()


if __name__ == '__main__':
    main()
