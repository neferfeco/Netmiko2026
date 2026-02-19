from netmiko import ConnectHandler


kapcsolo = {
    "device_type": "cisco_ios",
    "host": "192.168.40....",
    "username": "....",
    "password": "...."
}


try:
    with ConnectHandler(**kapcsolo) as kapcsolat:

    
        valasz = kapcsolat.send_command("show run")
        if "enable password" in valasz:
            jelszo = kapcsolat.send_command("show run | include enable password").split(' ')[-1]
            print(jelszo)
            if len(jelszo) < 8:
                print("Az enable jelszó nem megfelelő hosszúságú.")
                ujjelszo = input("Adj meg egy legalább 8 karakterből álló jelszót: ")
                while len(ujjelszo) < 8:
                    ujjelszo = input("Adj meg egy legalább 8 karakterből álló jelszót: ")
                kapcsolat.send_config_set(f"enable password {ujjelszo}")
                print("A jelszó beéllítása megtörtént.")
            else:
                print("MEgfelelő az enable jelszó")
                
        konzol = kapcsolat.send_command("sh run | section line con")
        konzol = konzol.split("\n")
        print(konzol)
        for i in konzol:
            if i.strip().startswith('password'):
                if len(i.split(' ')[-1]) < 8:
                    print("Az konzol jelszó nem megfelelő hosszúságú.")
                    
                    ujjelszo2 = input("Adj meg egy legalább 8 karakterből álló jelszót: ")
                
                    while len(ujjelszo2) < 8:
                        ujjelszo2 = input("Adj meg egy legalább 8 karakterből álló jelszót: ")
                
                    kapcsolat.send_config_set(["line con 0" , f"password {ujjelszo2}"])
                    print("A jelszó beéllítása megtörtént.")
                else:
                    print("MEgfelelő az konzol jelszó")   
        #--------------------
        vty = kapcsolat.send_command("sh run | section line vty")
        vty = vty.split("\n")
        print(vty)
        for i in konzol:
            if i.strip().startswith('password'):
                if len(i.split(' ')[-1]) < 8:
                    print("Az konzol jelszó nem megfelelő hosszúságú.")
                    
                    ujjelszo2 = input("Adj meg egy legalább 8 karakterből álló jelszót: ")
                
                    while len(ujjelszo2) < 8:
                        ujjelszo2 = input("Adj meg egy legalább 8 karakterből álló jelszót: ")
                
                    kapcsolat.send_config_set(["line con 0" , f"password {ujjelszo2}"])
                    print("A jelszó beéllítása megtörtént.")
                else:
                    print("MEgfelelő az konzol jelszó")      
        
            
except Exception as ex:
    print(f"Hiba: {ex}")


