import math
import sys
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


with open('data.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   

def vypocitat_a(data, energie, vaha, poc_teplot):
    energie = float(energie)
    vaha = float(vaha)
    t_aktualni = float(poc_teplot)
    
    # Načtení konstant z JSON
    bod_tani = float(data['bod_tani'])
    bod_varu = float(data['bod_varu'])
    tep_kap_pev = float(data['tepelna_kapacita_pevne'])
    tep_kap_kapal = float(data['tepelna_kapacita_kapalina'])
    tep_kap_plyn = float(data.get('tepelna_kapacita_plyn', 0)) # Nové
    skup_tani = float(data['skupenske_teplo_tani'])
    skup_varu = float(data['skupenske_teplo_varu'])

    zbytek_energie = energie

    # 1. Ohřev pevné látky
    if t_aktualni < bod_tani:
        potreba = vaha * tep_kap_pev * (bod_tani - t_aktualni)
        if zbytek_energie <= potreba:
            return t_aktualni + (zbytek_energie / (vaha * tep_kap_pev)), "Pevné"
        zbytek_energie -= potreba
        t_aktualni = bod_tani

    # 2. Tání (fázová přeměna)
    if t_aktualni == bod_tani:
        potreba = vaha * skup_tani
        if zbytek_energie <= potreba:
            return t_aktualni, f"Tání (roztaveno {(zbytek_energie/potreba)*100:.1f} %)"
        zbytek_energie -= potreba

    # 3. Ohřev kapaliny
    if t_aktualni < bod_varu:
        potreba = vaha * tep_kap_kapal * (bod_varu - t_aktualni)
        if zbytek_energie <= potreba:
            return t_aktualni + (zbytek_energie / (vaha * tep_kap_kapal)), "Kapalné"
        zbytek_energie -= potreba
        t_aktualni = bod_varu

    # 4. Var (fázová přeměna na plyn)
    if t_aktualni == bod_varu:
        potreba = vaha * skup_varu
        if zbytek_energie <= potreba:
            return t_aktualni, f"Var (vypařeno {(zbytek_energie/potreba)*100:.1f} %)"
        zbytek_energie -= potreba

    # 5. Ohřev plynu (pokud zbyla energie)
    if tep_kap_plyn > 0:
        t_final = t_aktualni + (zbytek_energie / (vaha * tep_kap_plyn))
        return t_final, "Plynné"
    
    return t_aktualni, "Plynné (kapacita plynu neznámá)"

def vypocitat_b(data, cilova_teplota, vaha, poc_teplot):
    # Převod na čísla
    cil_t, vaha, poc_t = float(cilova_teplota), float(vaha), float(poc_teplot)
    
    bod_tani = float(data['bod_tani'])
    bod_varu = float(data['bod_varu'])
    tep_kap_pev = float(data['tepelna_kapacita_pevne'])
    tep_kap_kapal = float(data['tepelna_kapacita_kapalina'])
    skup_tani = float(data['skupenske_teplo_tani'])
    skup_varu = float(data['skupenske_teplo_varu'])
    
    celkova_energie = 0
    t_aktualni = poc_t

    # 1. Ohřev pevné látky k bodu tání (pokud jsme pod ním)
    if t_aktualni < bod_tani:
        t_cil_faze = min(cil_t, bod_tani)
        celkova_energie += vaha * tep_kap_pev * (t_cil_faze - t_aktualni)
        t_aktualni = t_cil_faze

    # 2. Roztavení (pokud je cílová teplota aspoň bod tání a začínali jsme pod ním nebo na něm)
    if cil_t >= bod_tani and t_aktualni == bod_tani:
        # Tady se můžeš uživatele v UI zeptat, jestli chce jen začít tavit nebo úplně roztavit.
        # Standardně počítáme úplné roztavení.
        celkova_energie += vaha * skup_tani
        # t_aktualni zůstává bod_tani, ale už je to kapalina

    # 3. Ohřev kapaliny k bodu varu
    if cil_t > bod_tani:
        t_zacatek = bod_tani
        t_cil_faze = min(cil_t, bod_varu)
        celkova_energie += vaha * tep_kap_kapal * (t_cil_faze - t_zacatek)
        t_aktualni = t_cil_faze

    # 4. Vypaření (pokud chceme dosáhnout bodu varu a změnit na plyn)
    if cil_t >= bod_varu and t_aktualni == bod_varu:
        celkova_energie += vaha * skup_varu

    return round(celkova_energie, 2)
    
        


    
   