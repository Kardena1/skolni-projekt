import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

with open('objednavky.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   






























# Funkce
