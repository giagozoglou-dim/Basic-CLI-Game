all_items = ("Bandage", "Painkiller", "Serum", "Meat", "100 Dollar Bill")
all_descs = (
    "Heals 20 HP",
    "Heals 35 HP",
    "Heals 50 HP",
    "Grants +2 damage for the current room",
    "Ooooh shiny!"
)

def zip_items():
    """zips the item and item description lists together"""
    for item, desc in zip(all_items, all_descs):
        yield item, desc

def find_desc(key):
    """finds item description of key"""
    for item, desc in zip_items():
        if item == key:
            return desc
    return None
