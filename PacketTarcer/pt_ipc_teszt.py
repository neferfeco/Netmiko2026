import os           # Operációs rendszer műveletek (fájlok keresése)
import subprocess   # Külső programok (Packet Tracer) indítása
import time         # Időzítés (várakozás)
import socket       # Hálózati kommunikáció (ez a "kábel" a Python és a PT között)
import sys          # Rendszer szintű parancsok (pl. kiírás a konzolra)



# ==========================================
# KONFIGURÁCIÓ (Ezeket írd át a sajátodra!)
# ==========================================

# 1. A Packet Tracer program (.exe) pontos helye
# A 'r' betű (raw string) azért kell, hogy a \ jeleket ne vegye vezérlőkarakternek
PT_PATH = r"C:\Program Files\Cisco Packet Tracer 9.0.0\bin\PacketTracer.exe"

# 2. A megnyitandó .pka fájl pontos helye (teljes útvonal!)
PKA_PATH = r"C:\Users\Feco\Desktop\TMP2\12B\Tulip.pka"

# 3. IPC beállítások (Ezek általában fixek a PT-ben)
IPC_HOST = '127.0.0.1'  # localhost (saját gép)
IPC_PORT = 39000        # A port, ahol a PT "fülel"


# ==========================================
# OSZTÁLY A KOMMUNIKÁCIÓHOZ
# ==========================================

class VerbosePacketTracerIPC:
    """Ez az osztály felel a 'telefonhívásért' a Packet Tracer felé."""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None # Itt tároljuk majd a nyitott kapcsolatot

    def connect(self):
        """Megpróbál kapcsolódni a futó Packet Tracerhez."""
        print(f"   [IPC] Kapcsolódási kísérlet ide: {self.host}:{self.port} ...")
        try:
            # Létrehozunk egy internetes (AF_INET), TCP (SOCK_STREAM) socketet
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Beállítunk 5 mp türelmi időt. Ha a PT nem válaszol ennyi idő alatt, feladjuk.
            self.sock.settimeout(10) 
            
            # Itt történik a tényleges "betárcsázás"
            self.sock.connect((self.host, self.port))
            print("   [IPC] SIKER: Kapcsolat létrejött a Packet Tracerrel!")
            return True
            
        except ConnectionRefusedError:
            # Ez akkor jön, ha a PT nem fut, vagy nincs bepipálva az IPC Listen
            print("   [HIBA] A kapcsolat elutasítva. Fut a Packet Tracer? Engedélyezve van az IPC?")
            return False
        except Exception as e:
            # Minden egyéb hiba (pl. tűzfal)
            print(f"   [HIBA] Váratlan hiba: {e}")
            return False

    def send_command(self, command_str):
        """Elküld egy szöveges parancsot és várja a választ."""
        if not self.sock:
            return None
        
        # Debugolás: kiírjuk mit küldünk, hogy lássuk, ha elakad
        print(f"   [DEBUG] Küldés -> '{command_str}'")
        
        try:
            # 1. Kódolás: A Python stringet bájtokká kell alakítani (utf-8), 
            # és teszünk a végére egy újsor karaktert (\n), hogy a PT tudja, vége a parancsnak.
            msg_bytes = command_str.encode('utf-8') + b'\n'
            self.sock.sendall(msg_bytes)
            
            # 2. Fogadás: Várunk a válaszra. 4096 bájt a puffer mérete (ennyi fér el egy csomagban).
            response_bytes = self.sock.recv(4096)
            
            # 3. Dekódolás: A kapott bájtokat visszaalakítjuk szöveggé.
            response_str = response_bytes.decode('utf-8').strip() # strip() leszedi a felesleges szóközöket/entereket
            
            print(f"   [DEBUG] Válasz <- '{response_str}'")
            return response_str
            
        except Exception as e:
            print(f"   [HIBA] Kommunikációs hiba: {e}")
            return None

    def close(self):
        """Lezárja a kapcsolatot (letesszük a telefont)."""
        if self.sock:
            self.sock.close()

# ==========================================
# SEGÉDFÜGGVÉNYEK
# ==========================================

def check_paths():
    """Ellenőrzi, hogy léteznek-e a megadott fájlok."""
    print("[ELLENŐRZÉS] Útvonalak vizsgálata...")
    
    # Létezik a PacketTracer.exe?
    if not os.path.exists(PT_PATH):
        print(f"   [KRITIKUS HIBA] A Packet Tracer exe nem található itt:\n   {PT_PATH}")
        return False
        
    # Létezik a .pka fájl?
    if not os.path.exists(PKA_PATH):
        print(f"   [KRITIKUS HIBA] A .pka fájl nem található itt:\n   {PKA_PATH}")
        return False
        
    print("   [OK] Minden fájl megvan.")
    return True

def open_pka_file():
    """Elindítja a Packet Tracert a megadott pka fájllal."""
    print(f"\n[LÉPÉS 1/4] Packet Tracer indítása...")
    try:
        # A subprocess.Popen elindítja a programot, de nem állítja meg a Python futását (párhuzamosan futnak tovább)
        subprocess.Popen([PT_PATH, PKA_PATH])
        print("   [INFO] Indítási parancs elküldve.")
        
        # FONTOS: A PT-nek idő kell, amíg betölti a GUI-t és elindítja az IPC szervert.
        # Ha azonnal próbálnánk kapcsolódni, hibát kapnánk.
        print("   [INFO] Várakozás a betöltésre (30 mp)...")
        for i in range(30, 0, -1):
            sys.stdout.write(f"\r   Hátravan: {i} mp... ") # Visszaszámláló egy sorban
            sys.stdout.flush()
            time.sleep(1)
        print("\n   [INFO] Várakozási idő letelt.")
        return True
    except Exception as e:
        print(f"   [HIBA] Nem sikerült elindítani a Packet Tracert: {e}")
        return False

def fetch_data(client):
    print(f"\n[LÉPÉS 3/4] Adatok lekérdezése...")
    # Küldjünk egy üres entert először, hátha csak "alvó" állapotban van az interfész
    client.send_command("") 
    time.sleep(1)
    
    devices_data = []

    # 1. Megkérdezzük: Hány eszköz van összesen?
    # (A parancs neve 'ExApp.GetDeviceCount' - ez PT verziófüggő lehet, de ez a leggyakoribb)
    count_resp = client.send_command('ExApp.GetDeviceCount')
    
    if not count_resp or not count_resp.isdigit():
        print("   [HIBA] Nem kaptunk érvényes számot az eszközökről.")
        return []

    count = int(count_resp)
    print(f"   [INFO] Észlelt eszközök száma: {count}")

    # 2. Ciklus: Ha van 3 eszköz, akkor lekérjük a 0., 1., és 2. nevét.
    for i in range(count):
        # Összerakjuk a parancsot, pl: ExApp.GetDeviceName(0)
        cmd = f'ExApp.GetDeviceName({i})'
        name = client.send_command(cmd)
        
        if name:
            # Eltároljuk egy szótárban (dictionary)
            devices_data.append({"id": i, "name": name})
            
    return devices_data

# ==========================================
# FŐ PROGRAM (MAIN)
# ==========================================

def main():
    print("=== PYTHON <-> PACKET TRACER KAPCSOLAT ===")

    # 0. Előellenőrzés: Megvannak a fájlok?
    if not check_paths():
        print("\nA program leáll, mert a fájlok nem találhatók.")
        return

    # 1. Megnyitás: Elindítjuk a PT-t a pka fájllal
    if open_pka_file():
        
        # 2. Kapcsolódás: Próbálunk csatlakozni a sockethez
        print(f"\n[LÉPÉS 2/4] Kapcsolódás az IPC interfészhez...")
        client = VerbosePacketTracerIPC(IPC_HOST, IPC_PORT)
        
        if client.connect():
            # 3. Adatgyűjtés: Ha sikerült a kapcsolat, indul a lekérdezés
            devices = fetch_data(client)
            
            # 4. Kiírás: Eredmények megjelenítése
            print(f"\n[LÉPÉS 4/4] Eredmények feldolgozása...")
            print("-" * 40)
            print(f" {'ID':<5} | {'ESZKÖZ NEVE'}")
            print("-" * 40)
            
            if devices:
                for dev in devices:
                    print(f" {dev['id']:<5} | {dev['name']}")
            else:
                print(" Nem találtam eszközöket.")
            print("-" * 40 + "\n")
            
            # Kapcsolat bontása
            client.close()
        else:
            print("\n[VÉGZETES HIBA] Nem sikerült a socket kapcsolat.")
    
    print("=== PROGRAM VÉGE ===")

# Ez biztosítja, hogy a kód csak akkor fusson, ha közvetlenül indítjuk
if __name__ == "__main__":
    main()