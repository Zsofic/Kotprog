import requests
import csv

def konyvek_lekerese(max_oldalak=3):
    url = "https://gutendex.com/books?search=hungarian"
    konyvek = []
    oldal = 0

    while url and oldal < max_oldalak:
        print(f"Oldal lekérése: {oldal + 1}")
        valasz = requests.get(url)
        adatok = valasz.json()

        for konyv in adatok["results"]:
            cim = konyv.get("title", "Nincs cím")
            szerzok = ", ".join(szerzo["name"] for szerzo in konyv.get("authors", [])) or "Ismeretlen"
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
    if not konyvek:
        print("Nincs menthető adat.")
        return

    with open("konyvek.csv", "w", newline="", encoding="utf-8") as fajl:
        iro = csv.DictWriter(fajl, fieldnames=konyvek[0].keys())
        iro.writeheader()
        iro.writerows(konyvek)

    print("Mentve: konyvek.csv")


konyvek = konyvek_lekerese(5)

konyvek = konyvek_rendezese(konyvek)

print(f"\nTalált könyvek száma: {len(konyvek)}")
print("\nTop 10 legnépszerűbb könyv:")
for k in konyvek[:10]:
    print(f"{k['Cím']} — {k['Szerzők']} ({k['Letöltések']} letöltés)")

csv_mentes(konyvek)