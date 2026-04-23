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
            szerzok = ", ".join(s["name"] for s in konyv.get("authors", [])) or "Ismeretlen"
            letoltesek = konyv.get("download_count", 0)

            konyvek.append({
                "Cím": cim,
                "Szerzők": szerzok,
                "Letöltések": letoltesek
            })

        url = adatok.get("next")
        oldal += 1

    return konyvek


def csv_mentes(konyvek):
    if not konyvek:
        print("Nincs menthető adat.")
        return

    with open("konyvek.csv", "w", newline="", encoding="utf-8") as fajl:
        iro = csv.DictWriter(fajl, fieldnames=konyvek[0].keys())
        iro.writeheader()
        iro.writerows(konyvek)

    print("Mentve: konyvek.csv")


# --- Főprogram ---

konyvek = konyvek_lekerese(5)

print(f"\nTalált könyvek száma: {len(konyvek)}")

for k in konyvek[:10]:
    print(k)

csv_mentes(konyvek)