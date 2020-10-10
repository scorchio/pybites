from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup

out_dir = "/tmp"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
# source:
# https://www.digminecraft.com/lists/enchantment_list_pc.php
URL = ("https://bites-data.s3.us-east-2.amazonaws.com/"
       "minecraft-enchantment.html")

ITEMS = [
    "armor",
    "axe",
    "boots",
    "bow",
    "chestplate",
    "crossbow",
    "fishing_rod",
    "helmet",
    "pickaxe",
    "shovel",
    "sword",
    "trident",
]

ROMAN_TO_INT = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
}

@dataclass
class Enchantment:
    """Minecraft enchantment class
    
    Implements the following: 
        id_name, name, max_level, description, items
    """
    id_name: str
    name: str
    max_level: int
    description: str
    items: List[str] = field(default_factory=list)

    def short_str(self):
        return f'[{self.max_level}] {self.id_name}'

    def __str__(self):
        return f'{self.name} ({self.max_level}): {self.description}'


@dataclass
class Item:
    """Minecraft enchantable item class
    
    Implements the following: 
        name, enchantments
    """
    name: str = ''
    enchantments: List[Enchantment] = field(default_factory=list)

    def __str__(self):
        lines = []
        lines.append(f'{self.name.replace("_", " ").title()}: ')
        for enchantment in self.enchantments:
            lines.append(f'  {enchantment.short_str()}')
        result = '\n'.join(lines)
        return result


def generate_enchantments(soup):
    """Generates a dictionary of Enchantment objects
    
    With the key being the id_name of the enchantment.
    """
    results = {}
    item_rows = soup.find(id='minecraft_items').find_all('tr')
    for item_row in item_rows[1:]:
        tds = item_row.find_all('td')
        name = tds[0].find('a').get_text()
        id_name = tds[0].find('em').get_text()
        max_level = ROMAN_TO_INT[tds[1].get_text()]
        description = tds[2].get_text()
        raw_items = tds[4].find('img').get('data-src').split('/')[-1]
        found_items = []
        for item in ITEMS:
            if item in raw_items:
                found_items.append(item)
        results[id_name] = Enchantment(id_name, name, max_level, description, found_items)
    return results


def generate_items(data):
    """Generates a dictionary of Item objects
    
    With the key being the item name.
    """
    items = defaultdict(Item)
    for enchant in data.values():
        for item_name in enchant.items:
            items[item_name].name = item_name
            if enchant not in items[item_name].enchantments:
                items[item_name].enchantments.append(enchant)
    return items


def get_soup(file=HTML_FILE):
    """Retrieves/takes source HTML and returns a BeautifulSoup object"""
    if isinstance(file, Path):
        if not HTML_FILE.is_file():
            urlretrieve(URL, HTML_FILE)

        with file.open() as html_source:
            soup = Soup(html_source, "html.parser")
    else:
        soup = Soup(file, "html.parser")

    return soup


def main():
    """This function is here to help you test your final code.
    
    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    for item in minecraft_items:
        print(minecraft_items[item], "\n")


if __name__ == "__main__":
    main()

"""
Armor: 
  [1] binding_curse
  [4] blast_protection
  [4] fire_protection
  [4] projectile_protection
  [4] protection
  [3] thorns 

Axe: 
  [5] bane_of_arthropods
  [5] efficiency
  [3] fortune
  [5] sharpness
  [1] silk_touch
  [5] smite 

Boots: 
  [3] depth_strider
  [4] feather_falling
  [2] frost_walker 

Bow: 
  [1] flame
  [1] infinity
  [5] power
  [2] punch 

Chestplate: 
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Crossbow: 
  [1] multishot
  [4] piercing
  [3] quick_charge 

Fishing Rod: 
  [3] luck_of_the_sea
  [3] lure
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Helmet: 
  [1] aqua_affinity
  [3] respiration 

Pickaxe: 
  [5] efficiency
  [3] fortune
  [1] mending
  [1] silk_touch
  [3] unbreaking
  [1] vanishing_curse 

Shovel: 
  [5] efficiency
  [3] fortune
  [1] silk_touch 

Sword: 
  [5] bane_of_arthropods
  [2] fire_aspect
  [2] knockback
  [3] looting
  [1] mending
  [5] sharpness
  [5] smite
  [3] sweeping
  [3] unbreaking
  [1] vanishing_curse 

Trident: 
  [1] channeling
  [5] impaling
  [3] loyalty
  [3] riptide
"""