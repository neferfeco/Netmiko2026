from netmiko import ConnectHandler


kapcsolo = {
    "device_type": "cisco_ios",
    "host": "192.168.40.64",
    "username": "tanulo",
    "password": "Jelszo123"
}


try:
    with ConnectHandler(**kapcsolo) as kapcsolat:
        
        tftp_ip = input(f"Add meg a szerver IP-címét!: ")
        fajlnev = input(f"Mentendő konfig fájl neve:")
        
        output = kapcsolat.send_multiline_timing(["copy running-config tftp", tftp_ip, fajlnev])
        
        print(output)
        
            
except Exception as ex:
    print(f"Hiba: {ex}")


