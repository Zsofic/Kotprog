import requests
import csv
import json

def konyvek_lekerese(max_oldalak=3):
    url = "https://gutendex.com/books?search=hungarian"
    konyvek = []
    oldal = 0

    while url and oldal < max_oldalak:
        print("Oldal lekérése:", oldal + 1)
        valasz = requests.get(url)
        adatok = valasz.json()

        for konyv in adatok["results"]:
            cim = konyv.get("title", "Nincs cím")

            szerzok_lista = []
            for szerzo in konyv.get("authors", []):
                szerzok_lista.append(szerzo["name"])

            szerzok = ", ".join(szerzok_lista)

            if szerzok == "":
                szerzok = "Ismeretlen szerző"

            letoltesek = konyv.get("download_count", 0)

            konyvek.append({
                "Cím": cim,
                "Szerzők": szerzok,
                "Letöltések": letoltesek
            })

        url = adatok.get("next")
        oldal += 1

    return konyvek

def konyvek_rendezese(konyvek):
    return sorted(konyvek, key=lambda x: x["Letöltések"], reverse=True)


def csv_mentes(konyvek):
    with open("konyvek.csv", "w", newline="", encoding="utf-8") as fajl:
        csviro = csv.DictWriter(fajl, fieldnames=konyvek[0].keys())
        csviro.writeheader()
        csviro.writerows(konyvek)

    print("Mentve ide: konyvek.csv")


def json_mentes(konyvek):
    with open("konyvek.json", "w", encoding="utf-8") as fajl:
        json.dump(konyvek, fajl, ensure_ascii=False, indent=4)

    print("Mentve ide: konyvek.json")


konyvek = konyvek_lekerese(5)
konyvek = konyvek_rendezese(konyvek)

print("Talált könyvek száma:", len(konyvek))
print("\nTop 10 legnépszerűbb könyv:")

for konyv in konyvek[:10]:
    print(konyv["Cím"], "—", konyv["Szerzők"], "(", konyv["Letöltések"], "letöltés)")

csv_mentes(konyvek)
json_mentes(konyvek)