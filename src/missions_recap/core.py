"""Logique de calcul : événements .ics -> jours par mission et par mois."""
import re
from collections import defaultdict
from datetime import date, datetime, timedelta

import icalendar
import recurring_ical_events

A_TRIER = "À trier"
DEMI = re.compile(r"\((matin|aprem|apr[eè]s-?midi|am|pm)\)", re.IGNORECASE)


def charger_calendrier(chemin):
    with open(chemin, "rb") as f:
        return icalendar.Calendar.from_ical(f.read())


def _to_date(v):
    return v.date() if isinstance(v, datetime) else v


def est_journee_entiere(comp):
    """Vrai si l'événement est de type « journée entière » (DTSTART sans heure)."""
    if "DTSTART" not in comp:
        return False
    return not isinstance(comp["DTSTART"].dt, datetime)


def jours_evenement(comp):
    """Liste des dates couvertes par un événement « journée entière »."""
    d0 = comp["DTSTART"].dt
    d1 = comp["DTEND"].dt if "DTEND" in comp else d0 + timedelta(days=1)
    if isinstance(d1, datetime):  # cas atypique : fin avec heure
        d1 = d1.date()
    # DTEND est exclusif pour les journées entières
    jours = []
    d = d0
    while d < d1:
        jours.append(d)
        d += timedelta(days=1)
    return jours or [d0]


def est_ignore(titre):
    """Vrai si le titre est entouré de « -- » (ex : « --Travail chez un tel-- »)."""
    return titre.startswith("--")


def analyser_titre(titre):
    """Retourne (nom de mission, poids du jour)."""
    poids = 0.5 if DEMI.search(titre) else 1.0
    nom = DEMI.sub("", titre).strip()
    return nom, poids


def calculer_recap(cal, annee, mois_filtre=None):
    """Retourne {mois (1-12): {catégorie: nombre de jours}}.

    Seuls les événements « journée entière » sont pris en compte.
    `mois_filtre` : itérable de mois (1-12) à conserver ; None = tous.
    """
    mois_retenus = set(mois_filtre) if mois_filtre else set(range(1, 13))
    debut, fin = date(annee, 1, 1), date(annee + 1, 1, 1)
    evenements = recurring_ical_events.of(cal).between(debut, fin)

    par_jour = defaultdict(lambda: defaultdict(float))
    for ev in evenements:
        if not est_journee_entiere(ev):
            continue
        titre = str(ev.get("SUMMARY", "")).strip()
        if est_ignore(titre):
            continue
        nom, poids = analyser_titre(titre)
        if not nom:
            continue
        for j in jours_evenement(ev):
            if j.year == annee and j.month in mois_retenus:
                par_jour[j][nom] += poids

    resultat = defaultdict(lambda: defaultdict(float))
    d = debut
    while d < fin:
        if d.month in mois_retenus:
            contenu = par_jour.get(d, {})
            for nom, poids in contenu.items():
                resultat[d.month][nom] += poids
            if d.weekday() < 5:  # lundi-vendredi
                reste = 1.0 - sum(contenu.values())
                if reste > 0:
                    resultat[d.month][A_TRIER] += reste
        d += timedelta(days=1)
    return resultat
