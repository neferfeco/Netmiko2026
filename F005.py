from netmiko import ConnectHandler


kapcsolo = {
    "device_type": "cisco_ios",
    "host": "192.168.40.57",
    "username": "oli",
    "password": "wsw"
}


try:
    with ConnectHandler(**kapcsolo) as kapcsolat:

        # Helyes router azonosító bekérése
        azon = input("Adj meg egy egyedi router azonosítót: ").strip()
        darabok = azon.split('.')
        joe = True        
        if not(len(darabok) == 4):
            joe = False
        for darab in darabok:
            if not(darab.isnumeric() and int(darab) <= 255):
                joe = False
        while not joe:
            azon = input("Adj meg egy helyes router azonosítót: ").strip()
            darabok = azon.split('.')
            joe = True
            if not(len(darabok) == 4):
                joe = False
            for darab in darabok:
                if not(darab.isnumeric() and int(darab) <= 255):
                    joe = False
        
        kapcsolat.send_config_set(("router ospf 13","router-id "+azon))
        
        print("sikerult")
except Exception as ex:
    print(f"Hiba: {ex}")















