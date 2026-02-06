from netmiko import ConnectHandler

login_adatok = {
    "device_type": "cisco_ios",
    "host": "192.168.40.64",
    "username": "tanulo",
    "password": "Jelszo123"
}



def konzol_konfig_fajlba_mentes(ssh):
    with open("konzol.txt", "w", encoding="utf-8") as fajl:
        fajl.write(f"{ssh.send_command("show running-config | section line con 0")}")


def konzol_konfig_beolvasasa():
    try:
        with open("konzol.txt", encoding="utf-8") as fajl:
            output = fajl.read()
    except IOError as ex:
        print(f"Fájl olvasási hiba!: {ex}")
    
    return output

def konzol_jelszo_ellenorzes_A(ssh, online):
    if online:
        output = ssh.send_command("show running-config | section line con 0")
    else:        
        output = konzol_konfig_beolvasasa()

    print(f"Konzol beállítások:\n{'-' * 20}\n{output}\n{'-' * 20}\n")



    if "password" in output:
        if "login\n" in output:
            print(f"Konzol jelszó és hitelesítés beállítása OK!")
        else:
            print(f"Hiányzik a 'login' parancs!")
    elif "login\n" in output:
        print(f"Hiányzó jelszó!")
    else:
        print(f"A jelszó beállítás teljesen hiányzik!")
  

def konzol_jelszo_ellenorzes_B(ssh, online):    
    if online:
        output = ssh.send_command("show running-config | section line con 0")
    else:        
        output = konzol_konfig_beolvasasa()

    print(f"Konzol beállítások:\n{'-' * 20}\n{output}\n{'-' * 20}\n")

    clean_output = []    
    for sor in output.split("\n"):
        sor = sor.strip()
        
        if ("password" in sor) or ("login" == sor):
            clean_output.append(sor)
     
    if len(clean_output) == 0:
        print(f"A jelszó beállítás teljesen hiányzik!")
    elif len(clean_output) == 2:
        print(f"Konzol jelszó és hitelesítés beállítása OK!")
    elif "login" in clean_output:
        print(f"Hiányzó jelszó!")
    else:
        print(f"Hiányzó 'login' parancs!")







def interface_fajlba_mentes(ssh):
    with open("interfaces.txt", "w", encoding="utf-8") as fajl:
        fajl.write(f"{ssh.send_command("show running-config | include interface")}")


def interface_tipus_db_A(ssh, online):
    if online:
        output = ssh.send_command("show running-config | include interface")
    else:        
        output = konzol_konfig_beolvasasa()

    print(f"Interfészek listája:\n{'-' * 20}\n{output}\n{'-' * 20}\n")
    
    ifek = output.split("\n")
    
    if_tipusok = []
    for sor in ifek:
        tipus = (sor.split(" ")[1]).split("/")[0][:-1]
        if "Ethernet" in tipus and tipus not in if_tipusok:
            if_tipusok.append(tipus)
    
    db = 0
    for tipus in if_tipusok:
        for sor in ifek:
            if tipus in sor:
                db += 1
        print(f"{tipus}: {}")
            
    




def interface_tipus_db_B(ssh, online):
    if online:
        output = ssh.send_command("show running-config | include interface")
    else:        
        output = konzol_konfig_beolvasasa()

    print(f"Interfészek listája:\n{'-' * 20}\n{output}\n{'-' * 20}\n")







# ---------------------------
# PROGRAM
# ---------------------------

try:
    with ConnectHandler(**login_adatok) as kapcsolat:
        
        
        
        # 2. feladat
        #konzol_konfig_fajlba_mentes(kapcsolat)        
        
        """
        online = input(f"Ellenőrzés SSH-k kereszül (online)? [I/n])")
        if online.upper() == "I":
            konzol_jelszo_ellenorzes_A(kapcsolat, True)
            #konzol_jelszo_ellenorzes_B(kapcsolat, True)
        else:
            konzol_jelszo_ellenorzes_A(kapcsolat, False)
            #konzol_jelszo_ellenorzes_B(kapcsolat, False)
        """






        #4. feladat
        #interface_fajlba_mentes(kapcsolat)
        
        online = input(f"Ellenőrzés SSH-k kereszül (online)? [I/n])")
        if online.upper() == "I":
            interface_tipus_db_A(kapcsolat, True)
            #konzol_jelszo_ellenorzes_B(kapcsolat, True)
        else:
            interface_tipus_db_A(kapcsolat, False)
            #konzol_jelszo_ellenorzes_B(kapcsolat, False)

except Exception as ex:
    print(f"Csatlakozási hiba: {ex}")





