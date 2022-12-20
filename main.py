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

        self.radio = None
        self.results = None
        self.ammo_tree = None
        self.weapon_tree = None

        self.widgets()

        self.attributes('-topmost', True)
        self.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")
        self.update()
        self.attributes('-topmost', False)

    def widgets(self):
        pad = {'padx': 10, 'pady': 10}
        self.search_frame(pad)
        self.button_frame(pad)
        self.db_frame(pad)

    def search_frame(self, pad):
        search_frame = ttk.Frame(self)
        search_frame.grid(column=0, row=0, **pad)
        ttk.Label(search_frame, text='Search by name: ').grid(column=0, row=0)

        self.radio = tk.IntVar()
        self.radio.set(0)
        ttk.Radiobutton(search_frame, text='Ammo', variable=self.radio, value=0).grid(column=1, row=0)
        ttk.Radiobutton(search_frame, text='Weapon', variable=self.radio, value=1).grid(column=2, row=0)
        ttk.Button(search_frame, text='Submit', command=self.submit_click).grid(column=2, row=1)

        self.results = ttk.Label(search_frame, text='')
        self.results.grid(column=0, row=2, columnspan=3)

    def button_frame(self, pad):
        btn_frame = ttk.Frame(self)
        btn_frame.grid(column=0, row=1, padx=10)
        ttk.Label(btn_frame, text='Search by cartridge:').grid(column=0, row=0, columnspan=2)

        rifle_frame = ttk.Frame(btn_frame)
        rifle_frame.grid(column=0, row=1, rowspan=2, sticky='nw', **pad)
        ttk.Label(rifle_frame, text='Rifle').grid(sticky='w')
        rifle_cartridges = ['9x39mm', '.366 TKM', '5.45x39mm', '5.56x45mm NATO', '.300 Blackout', '7.62x39mm',
                            '7.62x51mm NATO', '7.62x54mmR', '.338 Lapua Magnum', '12.7x55mm STs-130']
        for cartridge in rifle_cartridges:
            ttk.Button(rifle_frame, text=cartridge, command=partial(self.ammo_click, cartridge)).grid(sticky='w')

        gl_frame = ttk.Frame(btn_frame)
        gl_frame.grid(column=0, row=3, sticky='sw', **pad)
        ttk.Label(gl_frame, text='GL').grid(sticky='w')
        gl_cartridges = ['40x46 mm']
        for cartridge in gl_cartridges:
            ttk.Button(gl_frame, text=cartridge, command=partial(self.ammo_click, cartridge)).grid(sticky='w')

        shotgun_frame = ttk.Frame(btn_frame)
        shotgun_frame.grid(column=1, row=1, sticky='w', **pad)
        ttk.Label(shotgun_frame, text='Shotgun').grid(sticky='w')
        shotgun_cartridges = ['12/70', '20/70', '23x75mm']
        for cartridge in shotgun_cartridges:
            ttk.Button(shotgun_frame, text=cartridge, command=partial(self.ammo_click, cartridge)).grid(sticky='w')

        pistol_frame = ttk.Frame(btn_frame)
        pistol_frame.grid(column=1, row=2, sticky='w', **pad)
        ttk.Label(pistol_frame, text='Pistol').grid(sticky='w')
        pistol_cartridges = ['7.62x25mm Tokarev', '9x18mm Makarov', '9x19mm Parabellum', '9x21mm Gyurza', '.45 ACP']
        for cartridge in pistol_cartridges:
            ttk.Button(pistol_frame, text=cartridge, command=partial(self.ammo_click, cartridge)).grid(sticky='w')

        pdw_frame = ttk.Frame(btn_frame)
        pdw_frame.grid(column=1, row=3, sticky='w', **pad)
        ttk.Label(pdw_frame, text='PDW').grid(sticky='w')
        pdw_cartridges = ['4.6x30mm HK', '5.7x28mm FN']
        for cartridge in pdw_cartridges:
            ttk.Button(pdw_frame, text=cartridge, command=partial(self.ammo_click, cartridge)).grid(sticky='w')

    def db_frame(self, pad):
        db_frame = ttk.Frame(self)
        db_frame.grid(column=1, row=0, rowspan=2, sticky='n', **pad)

        scroll_height = {'ipady': 88}

        ammo_tree_f = ttk.LabelFrame(db_frame, text="Ammunition")
        ammo_tree_f.grid(column=0, row=0)
        ammo_tree_scroll = ttk.Scrollbar(ammo_tree_f)
        ammo_tree_scroll.grid(column=1, row=0, **scroll_height)
        self.ammo_tree = TvSort(ammo_tree_f,
                                columns=("Cartridge", "Name", "Dmg", "Pen", "Frag"),
                                yscrollcommand=ammo_tree_scroll.set)

        self.entry = ttk.Entry(search_frame)
        self.entry.grid(column=0, row=1, columnspan=2, ipadx=15, pady=10)
        self.entry.bind('<Return>', self.submit_entry)
        self.ammo_tree.column("#0", width=0, stretch=0)
        self.ammo_tree.column("Cartridge", **self.get_width_kwargs(120))
        self.ammo_tree.column("Name", **self.get_width_kwargs(210))
        self.ammo_tree.column("Dmg", **self.get_width_kwargs(50))
        self.ammo_tree.column("Pen", **self.get_width_kwargs(50))
        self.ammo_tree.column("Frag", **self.get_width_kwargs(50))
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
        self.weapon_tree.column("Cartridge", **self.get_width_kwargs(120))
        self.weapon_tree.column("Name", **self.get_width_kwargs(120))
        self.weapon_tree.column("Type", **self.get_width_kwargs_difference(210, 120))
        self.weapon_tree.column("Recoil", **self.get_width_kwargs(50))
        self.weapon_tree.column("Ergo", **self.get_width_kwargs(50))
        self.weapon_tree.column("RPM", **self.get_width_kwargs(50))
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

    def count_results(self):
        rows = len(self.ammo_tree.get_children()) + len(self.weapon_tree.get_children())
        self.results.config(text=f"Found {rows} results")
    def execute_and_populate(self, query, tree, col_indices):
        self.c.execute(query)
        for col in self.c.fetchall():
            values = [col[i] for i in col_indices]
            tree.insert(parent='', index='end', text='', values=values)

    def query_entry(self, entry):
        self.ammo_tree.delete(*self.ammo_tree.get_children())
        self.weapon_tree.delete(*self.weapon_tree.get_children())

        if self.entry.get() == "" or self.entry.get() == " ":
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





    def separator_resize_blocker(self, event):
        if self.ammo_tree.identify_region(event.x, event.y) == "separator" or \
                self.weapon_tree.identify_region(event.x, event.y) == "separator":
            return "break"



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
