import socket
import json

def get_pt_devices(host='127.0.0.1', port=39000):
    # Kapcsolódás a Packet Tracer IPC szerveréhez
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            
            # Ez egy példa kérés (az API specifikációja alapján változhat)
            # A Packet Tracer JSON-RPC szerű struktúrát használ
            request = {
                "id": "1",
                "method": "listDevices",
                "params": []
            }
            
            # Üzenet küldése
            s.sendall(json.dumps(request).encode('utf-8'))
            
            # Válasz fogadása
            data = s.recv(4096)
            response = json.loads(data.decode('utf-8'))
            
            return response
            
        except ConnectionRefusedError:
            return "Hiba: A Packet Tracer IPC szervere nem elérhető!"

# Futtatás és kiértékelés
result = get_pt_devices()
print(result)