from netmiko import ConnectHandler

login_adatok = {
    "device_type": "cisco_ios",
    "host": "192.168.40.64",
    "username": "tanulo",
    "password": "Jelszo123"
}

# -----------------------------------------------

def vlan_letrehozas(ssh):
    parancsok = [
                "vlan 10", "name Tanulo",
                "vlan 20", "name Oktato",
                "vlan 30", "name Pedagogus",
                "vlan 100", "name Ugyvitel"
    ]
    
    ssh.send_config_set(parancsok)
    
    print(f"{ssh.send_command("show vlan brief")}\n")


def konzol_konfig_fajlba_mentes(ssh):
    with open("konzol.txt", "w", encoding="utf-8") as fajl:
        fajl.write(f"{ssh.send_command("show running-config | section line con 0")}")


def konzol_konfig_beolvasasa():
    try:
        with open("saved_configs/konzol.txt", encoding="utf-8") as fajl:
            output = fajl.read()
    except IOError as ex:
        print(f"Fájl olvasási hiba!: {ex}")
    
    return output


def konzol_jelszo_ellenorzes_A(ssh, online):
    if online:
        output = ssh.send_command("show running-config | section line con 0")
    else:        
        output = konzol_konfig_beolvasasa()

    print(f"A) Konzol beállítások:\n{'-' * 20}\n{output}\n{'-' * 20}\n")

    if "password" in output:
        if "login" in output or "login\n" in output \
            and "login " not in output:
            print(f"Konzol jelszó és hitelesítés beállítása OK!\n")
        else:
            print(f"Hiányzik a 'login' parancs!\n")
            
    elif "login" in output or "login\n" in output \
          and "login " not in output:
        print(f"Hiányzó jelszó!\n")
    else:
        print(f"A jelszó beállítás teljesen hiányzik!\n")
  

def konzol_jelszo_ellenorzes_B(ssh, online):    

    if online:
        output = ssh.send_command("show running-config | section line con 0")
    else:        
        output = konzol_konfig_beolvasasa()

    print(f"B) Konzol beállítások:\n{'-' * 20}\n{output}\n{'-' * 20}\n")

    clean_output = []    
    for sor in output.split("\n"):
        sor = sor.strip()
        
        if ("password" in sor) or ("login" == sor):
            clean_output.append(sor)
     
    if len(clean_output) == 0:
        print(f"A jelszó beállítás teljesen hiányzik!\n")
    elif len(clean_output) == 2:
        print(f"Konzol jelszó és hitelesítés beállítása OK!\n")
    elif "login" in clean_output:
        print(f"Hiányzó jelszó!\n")
    else:
        print(f"Hiányzó 'login' parancs!\n")


def konzol_jelszo_csere(ssh):
    parancsok = [
                "line console 0",
                "password konJelszo"
    ]
    
    ssh.send_config_set(parancsok)
    
    print(f"{ssh.send_command("show run | section line con")}\n")


def interface_fajlba_mentes(ssh):
    with open("interfaces.txt", "w", encoding="utf-8") as fajl:
        fajl.write(f"{ssh.send_command("show running-config | include interface")}")


def interface_lista_beolvasasa():
    try:
        with open("saved_configs/interfaces.txt", encoding="utf-8") as fajl:
            output = fajl.read()
    except IOError as ex:
        print(f"Fájl olvasási hiba!: {ex}")
    
    return output


def interface_tipus_db_A(ssh, online):
    if online:
        output = ssh.send_command("show running-config | include interface")
    else:        
        output = interface_lista_beolvasasa()

    #print(f"Interfészek listája:\n{'-' * 20}\n{output}\n{'-' * 20}\n")
    
    ifek = output.split("\n")
    
    if_tipusok = []
    for sor in ifek:
        tipus = (sor.split(" ")[1]).split("/")[0][:-1]
        if "Ethernet" in tipus and tipus not in if_tipusok:
            if_tipusok.append(tipus) 
    #print(f"{if_tipusok}")
    
    print(f"(A) A kapcsoló interfészeinek típusa és száma:")
    for tipus in if_tipusok:
        db = 0
        for sor in ifek:
            if tipus in sor:
                db += 1
        print(f"\t{tipus:20}: {db} db")
            

def interface_tipus_db_B(ssh, online):
    if online:
        output = ssh.send_command("show running-config | include interface")
    else:        
        output = interface_lista_beolvasasa()

    #print(f"Interfészek listája:\n{'-' * 20}\n{output}\n{'-' * 20}\n")

    ifek = output.split("\n")
    
    i = 0
    while "Ethernet" not in ifek[i]:
        i += 1
    
    print(f"(B) A kapcsoló interfészeinek típusa és száma:")
    akt = (ifek[i].split(" ")[1]).split("/")[0][:-1]
    print(f"\t{akt:20}: ", end="")
    db = 1
    
    for j in range(i + 1, len(ifek)):
        if akt in ifek[j]:
            db += 1
        elif "Ethernet" in ifek[j]:
            print(f"{db} db")
            akt = (ifek[j].split(" ")[1]).split("/")[0][:-1]
            print(f"\t{akt:20}: ", end="")
            db = 1
    print(f"{db} db")        


# -----------------------------------------------
# PROGRAM
# -----------------------------------------------

try:
    with ConnectHandler(**login_adatok) as kapcsolat:    
        # 1. feladat
        print(f"1. feladat")
        #vlan_letrehozas(kapcsolat)        


        # 2. feladat
        print(f"2. feladat")
        #konzol_konfig_fajlba_mentes(kapcsolat)        
        
        konzol_jelszo_ellenorzes_A(kapcsolat, True)
        konzol_jelszo_ellenorzes_B(kapcsolat, True)


        # 3. feladat
        print(f"3. feladat")
        #konzol_jelszo_csere(kapcsolat)


        #4. feladat
        print(f"4. feladat")
        #interface_fajlba_mentes(kapcsolat)
        
        #interface_tipus_db_A(kapcsolat, True)
        #interface_tipus_db_B(kapcsolat, True)

except Exception as ex:
    print(f"Csatlakozási hiba: {ex}")


# -----------------------------------------------

# OFFLINE ellenőrzés

# 2. feladat
konzol_jelszo_ellenorzes_A(None, False)
#konzol_jelszo_ellenorzes_B(None, False)

# 4. feladat
#interface_tipus_db_A(None, False)
#interface_tipus_db_B(None, False)




