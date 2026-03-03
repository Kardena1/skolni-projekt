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

    # 2. FÁZE: Tání (přeměna pevné látky na kapalinu)
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
    
        


    
   