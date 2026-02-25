import math
import sys
import os
import json

with open('data.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   

def vypocitat_a(data,energie,vaha,poc_teplot):
    bod_tani = data['bod_tani']
    bod_varu = data['bod_varu']
    tep_kap_pev = data['tepelna_kapacita_pevne']
    tep_kap_kapal = data['tepelna_kapacita_kapalina']
    skup_tani = data['skupenske_teplo_tani']
    skup_varu = data['skupenske_teplo_varu']

    energie,vaha,poc_teplot,bod_tani,bod_varu,tep_kap_pev,tep_kap_kapal,skup_tani,skup_varu = int(energie),int(vaha),int(poc_teplot),int(bod_tani),int(bod_varu),int(tep_kap_pev),int(tep_kap_kapal),int(skup_tani),int(skup_varu)
    potreba_na_tani = vaha * skup_tani
    potreba_na_var = vaha * skup_varu
    print(f"debug1 {type(bod_tani)} {type(bod_varu)} {type(tep_kap_pev)} {type(tep_kap_kapal)} {type(skup_tani)} {type(skup_varu)} {type(energie)} {type(vaha)} {type(poc_teplot)}")


