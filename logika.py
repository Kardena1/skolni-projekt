import math
import sys
import os
import json

with open('data.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   

def vypocitat_a(data, energie, vaha, poc_teplot):
    # Převod na čísla (nechej vše float, je to jistota)
    energie, vaha, poc_teplot = float(energie), float(vaha), float(poc_teplot)
    
    bod_tani = float(data['bod_tani'])
    bod_varu = float(data['bod_varu'])
    tep_kap_pev = float(data['tepelna_kapacita_pevne'])
    tep_kap_kapal = float(data['tepelna_kapacita_kapalina'])
    skup_tani = float(data['skupenske_teplo_tani'])
    skup_varu = float(data['skupenske_teplo_varu'])
    
    zbytek_energie = energie
    t_aktualni = poc_teplot

    # 1. FÁZE: Ohřev pevné látky k bodu tání
    if t_aktualni < bod_tani:
        potreba_ohrev_tani = vaha * tep_kap_pev * (bod_tani - t_aktualni)
        if zbytek_energie <= potreba_ohrev_tani:
            t_vysledna = t_aktualni + (zbytek_energie / (vaha * tep_kap_pev))
            return round(t_vysledna, 2), "Pevne skupenstvi"
        
        zbytek_energie -= potreba_ohrev_tani
        t_aktualni = bod_tani

    # 2. FÁZE: Tání (Tady jsi měl tu chybu - chybělo to tu)
    potreba_skup_tani = vaha * skup_tani
    if zbytek_energie <= potreba_skup_tani:
        return bod_tani, "Smes pevne/kapalne (tani)"
    
    zbytek_energie -= potreba_skup_tani
    # Teď je z toho 100% kapalina na bodu tání

    # 3. FÁZE: Ohřev kapaliny k bodu varu
    potreba_ohrev_var = vaha * tep_kap_kapal * (bod_varu - t_aktualni)
    if zbytek_energie <= potreba_ohrev_var:
        t_vysledna = t_aktualni + (zbytek_energie / (vaha * tep_kap_kapal))
        return round(t_vysledna, 2), "Kapalne skupenstvi"   
    
    zbytek_energie -= potreba_ohrev_var

    # 4. FÁZE: Var (přeměna na plyn)
    potreba_na_vypar = vaha * skup_varu
    if zbytek_energie <= potreba_na_vypar:
        return bod_varu, "Smes kapalne/plyn (var)"
    
    return bod_varu, "Plynne skupenstvi"
        


    
   