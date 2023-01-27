from cartridges import Cartridges
from math import trunc
import requests


class Client:
    def __init__(self):
        self._cartridges = Cartridges()
        self._weapon_query = """
            {
                items(type: gun) {
                    id
                    shortName
                    category {
                        name
                    }
                    properties {
                        ... on ItemPropertiesWeapon {
                          caliber
                          defaultRecoilVertical
                          defaultRecoilHorizontal
                          defaultErgonomics
                          fireRate
                        }
                    }
                }
            }
            """
        self._ammo_query = """
            {
                items(type: ammo) {
                    id
                    shortName
                    category {
                        name
                    }
                    properties {
                        ... on ItemPropertiesAmmo {
                            caliber
                            damage
                            penetrationPower
                            accuracyModifier
                            recoilModifier
                            fragmentationChance
                        }
                    }
                }
            }
            """

    @staticmethod
    def _run_query(query):
        # Docs: https://api.tarkov.dev/___graphql
        response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

    @staticmethod
    def _prefix(num):
        return f"{num:{'+' if num else ''}}"

    def get_weapons_list(self):
        items = self._run_query(self._weapon_query)['data']['items']
        weapons_list = []
        for item in items:
            if not item['properties'] or not item['category']:
                continue
            id_ = item['id']
            caliber = self._cartridges.match(item['properties']['caliber'].replace('Caliber', ''))
            name = item['shortName']
            type_ = item['category']['name']
            rec = item['properties']['defaultRecoilVertical'] + item['properties']['defaultRecoilHorizontal']
            ergo = trunc(item['properties']['defaultErgonomics'])
            rpm = item['properties']['fireRate']
            weapons_list.append((id_, caliber, name, type_, rec, ergo, rpm))
        return weapons_list

    def get_ammo_list(self):
        items = self._run_query(self._ammo_query)['data']['items']
        ammo_list = []
        for item in items:
            if not item['category']['name'] == 'Ammo':
                continue
            id_ = item['id']
            caliber = self._cartridges.match(item['properties']['caliber'].replace('Caliber', ''))
            name = item['shortName']
            dmg = item['properties']['damage']
            pen = item['properties']['penetrationPower']
            acc = self._prefix(trunc(item['properties']['accuracyModifier'] * 100))
            rec = self._prefix(trunc(item['properties']['recoilModifier'] * 100))
            frag = f"{trunc(item['properties']['fragmentationChance'] * 100)}%"
            ammo_list.append((id_, caliber, name, dmg, pen, acc, rec, frag))
        return ammo_list


if __name__ == '__main__':
    client = Client()
    print(client.get_weapons_list())
    print(client.get_ammo_list())
