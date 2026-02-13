from pywinauto import Application
import time
import os
import csv
import re

PT_PATH = r"C:\Program Files\Cisco Packet Tracer 9.0.0\bin\PacketTracer.exe"
BEADASOK = r"C:\Users\pillerf\Downloads"

def get_score(pka_path):

    app = Application(backend="uia").start(f'"{PT_PATH}" "{pka_path}"')
    time.sleep(10)

    # Activity ablak keresése
    activity = app.window(title_re="PT Activity.*")
    activity.wait("visible", timeout=20)

    score_value = None

    # Szövegek bejárása
    for elem in activity.descendants(control_type="Text"):
        text = elem.window_text()
        match = re.search(r"\d+\s*%", text)
        if match:
            score_value = match.group()
            break

    app.kill()

    return score_value


eredmenyek = []

for f in os.listdir(BEADASOK):
    if f.endswith(".pka"):
        path = os.path.join(BEADASOK, f)
        print(f"Feldolgozás: {f}")
        score = get_score(path)
        eredmenyek.append([f, score])

with open("eredmenyek.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Fajl", "Score"])
    writer.writerows(eredmenyek)

print("Kész.")
