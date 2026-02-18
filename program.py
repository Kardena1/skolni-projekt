import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

with open('data.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   

def pridani_materialu():
    nazev = input("Zadej nazev materialu: ")
    bod_tani = int(input("Zadej bod tani: "))
    bod_varu = int(input("Zadej bod varu: "))
    novy_material = {
        "nazev": nazev,
        "bod_tani": bod_tani,
        "bod_varu": bod_varu
    }
    data["material"].append(novy_material)
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # ulozeni zpet do souboru 



def vypsat_materialy():
    for i, material in enumerate(data["material"], start=1):
        print(f"{i}. Material:", material["nazev"], "Bod tani:", material["bod_tani"],"°C", "Bod varu:", material["bod_varu"],"°C","\n") # vypsat materialy s jejich atributy

vypsat_materialy()

    
































# Funkce
