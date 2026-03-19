from netmiko import ConnectHandler


kapcsolo = {
    "device_type": "cisco_ios",
    "host": "192.168.40.110",
    "username": "rolivagyok",
    "password": "kiskacsa"
}


try:
    with ConnectHandler(**kapcsolo) as kapcsolat:
        
        # 1. feladat
        output = kapcsolat.send_command("show version | include uptime")
        
        reszek = output.split(" ")
        
        print(f"Az eszköz {reszek[-2]} {reszek[-1]} ideje működik.\n")
        
        
        # 2. feladat
        output = kapcsolat.send_command("show ip interface brief") 
        
        interfesz_adatok = output.split("\n")
        
        print(f"Inaktív interfészek:")
        for interfesz in interfesz_adatok:
            if "down" in interfesz:
                print(f"\t{interfesz.split(" ")[0]}")
        
        
        # 3. feladat
        if_letrehozas = [
            "interface Loopback101",
            "description This is an infinite loop.",
            "ip address 10.10.10.100 255.255.255.0",
            "no shutdown"
        ]
        
        kapcsolat.send_config_set(if_letrehozas)
        
        if len(kapcsolat.send_command("show ip interface brief | include Loopback101")) != 0:
            print(f"\nInterfész létrehozása sikerült!\n")


        # 4. feladat
        
        output = kapcsolat.send_command("show interface G0/0/0")
        
        print(f"A G0/0/0 interfész EIGRP mérték számításban szereplő paramétereinek értékei:")
        
        for sor in output.split("\n"):
            if "BW" in sor:
                adatok = sor.strip().split(",")
                
                for adat in adatok:
                    if "BW" in adat:
                        print(f"\tSávszélesség: {adat.split(" ")[-2:]}")
                    elif "DLY" in adat:
                        print(f"\tKésleltetés: {adat.split(" ")[-2:]}")

            elif "reliability" in sor:
                adatok = sor.strip().split(",")
                
                for adat in adatok:    
                    if "reliability" in adat:
                        print(f"\tMegbízhatóság: {adat.split(" ")[-1]}")
                        print(f"\tTerhelés:", end=" ")
                    elif "load" in adat:
                        print(f"{adat.split(" ")[-1]}", end=" ")
                
        print("\n")
            
            
except Exception as ex:
    print(f"Hiba: {ex}")


