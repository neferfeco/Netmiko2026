import random
betuk = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
szamok = []
rendszamok = []

for i in range(10):
    rendszam = ''
    szam = random.randint(100, 999)
    for j in range(3):
        betu = random.randint(0, 8)    
        rendszam += betuk[betu]
    rendszam = rendszam + "-" + str(szam)
    rendszamok.append(rendszam)
print(rendszamok)

i = 0

while i < len(rendszamok) and rendszamok[i] != "ABC-123":
    i+=1
if i < len(rendszamok):
    print("Van ilyen.")
else:
    print("Nincs ilyen.")    
    
    
