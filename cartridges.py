class Cartridges:
    def __init__(self):
        self.map = {
            'pistol': {
                '762x25TT': '7.62x25mm',
                '9x18PM': '9x18mm',
                '9x18PMM': '9x18mm',
                '9x19PARA': '9x19mm',
                '9x21': '9x21mm',
                '9x33R': '.357 Magnum',
                '1143x23ACP': '.45 ACP'
            },
            'pdw': {
                '46x30': '4.6x30mm',
                '57x28': '5.7x28mm'
            },
            'rifle': {
                '545x39': '5.45x39mm',
                '556x45NATO': '5.56x45mm',
                '762x35': '.300 Blackout',
                '762x39': '7.62x39mm',
                '762x51': '7.62x51mm',
                '762x54R': '7.62x54mmR',
                '86x70': '.338 Lapua',
                '9x39': '9x39mm',
                '366TKM': '.366 TKM',
                '127x55': '12.7x55mm'
            },
            'shotgun': {
                '12g': '12x70mm',
                '20g': '20x70mm',
                '23x75': '23x75mm',
            },
            'gl': {
                '40x46': '40x46mm',
                '40mmRU': '40x53mm'
            },
            'flare': {
                '26x75': '26x75mm'
            }
        }
        self._flat_map = {}
        for key in self.map:
            self._flat_map.update(self.map[key])

    def match(self, string):
        if string not in self._flat_map:
            print(f"No match: {string}")
        return self._flat_map.get(string, string)
