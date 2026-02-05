from netmiko import ConnectHandler

login_adatok = {
    "device_type": "cisco_ios",
    "host": "192.168.40.64",
    "username": "tanulo",
    "password": "Jelszo123"
}








# ---------------------------
# PROGRAM
# ---------------------------

try:
    with ConnectHandler(**login_adatok) as kapcsolat:
        pass
        
        
        
        

        

except Exception as ex:
    print(f"Csatlakozási hiba: {ex}")





