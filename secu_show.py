from netmiko import ConnectHandler

def netmiko_show_version(kapcsolo):
    try:
        with ConnectHandler(**kapcsolo) as kapcsolat:
            output = kapcsolat.send_command("show version")
                
    except Exception as ex:
        print(f"Hiba: {ex}")

def fajlbeolvasas():
    try:
        with open("show_version.txt", encoding="utf-8") as fajl:
            szoveg = fajl.read()
        
    except IOError as ex:
        print(f"IO hiba: {ex}")

    return szoveg


# Milyen IOS verzió fut a kapcsolón?
def ios_verzio(verzio_info):
    elso_sor = verzio_info.split("\n")[0]
    
    r = elso_sor.split(",")
    
    verzio = r[1].strip().split(" ")[2].lstrip("(").rstrip(")")
    verzio += " " + r[2].strip().lstrip("Version ")

    return verzio


# Hány Ethernet interace van a kapcsolón?
def ethernet_interfacek_szama():
    pass


#################################################
#    PROGRAM
#################################################

output = ""

kapcsolo = {
    "device_type": "cisco_ios",
    "host": "192.168.40.133",
    "username": "feco",
    "password": "netmiko2026"
}

#netmiko_show_version(kapcsolo)
#print(output)

verzio_info = fajlbeolvasas()
# print(verzio_info)

print(f"IOS verzió: {ios_verzio(verzio_info)}")

print(f"{ethernet_interfacek_szama()} Ethernet interface van a kapcsolón.")


