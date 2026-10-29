import argparse
import csv
from datetime import date

from . import __version__
from .core import A_TRIER, calculer_recap, charger_calendrier

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="missions-recap",
        description="Jours par mission et par mois depuis un export .ics.",
    )
    p.add_argument("ics", help="fichier calendrier exporté (.ics)")
    p.add_argument("annee", type=int, nargs="?", default=date.today().year,
                   help="année à analyser (défaut : année en cours)")
    p.add_argument("-m", "--mois", type=int, nargs="+", metavar="N",
                   choices=range(1, 13),
                   help="ne garder que ces mois (1-12), ex : -m 10  ou  -m 9 10 11")
    p.add_argument("--csv", metavar="FICHIER", help="exporter aussi en CSV")
    p.add_argument("--version", action="version", version=__version__)
    args = p.parse_args(argv)

    mois = calculer_recap(charger_calendrier(args.ics), args.annee, args.mois)

    if not mois:
        print("Aucune donnée pour cette période.")
        return

    lignes = []
    for m in sorted(mois):
        print(f"\n=== {MOIS[m - 1].capitalize()} {args.annee} ===")
        for nom, total in sorted(mois[m].items(), key=lambda x: (x[0] == A_TRIER, x[0])):
            print(f"  {nom:<25} {total:g} j".replace(".", ","))
            lignes.append([args.annee, MOIS[m - 1], nom, total])

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Année", "Mois", "Catégorie", "Jours"])
            w.writerows(lignes)
        print(f"\nCSV écrit : {args.csv}")
