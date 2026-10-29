import icalendar

from missions_recap import A_TRIER, calculer_recap

ICS = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//test//
BEGIN:VEVENT
UID:1
DTSTART;VALUE=DATE:20261005
DTEND;VALUE=DATE:20261007
SUMMARY:Mission A
END:VEVENT
BEGIN:VEVENT
UID:2
DTSTART;VALUE=DATE:20261007
DTEND;VALUE=DATE:20261008
SUMMARY:Mission A (matin)
END:VEVENT
BEGIN:VEVENT
UID:3
DTSTART;VALUE=DATE:20261007
DTEND;VALUE=DATE:20261008
SUMMARY:Mission B (aprem)
END:VEVENT
BEGIN:VEVENT
UID:4
DTSTART;VALUE=DATE:20261008
DTEND;VALUE=DATE:20261009
SUMMARY:OFF
END:VEVENT
BEGIN:VEVENT
UID:5
DTSTART:20261009T090000Z
DTEND:20261009T170000Z
SUMMARY:Mission C
END:VEVENT
BEGIN:VEVENT
UID:6
DTSTART;VALUE=DATE:20261112
DTEND;VALUE=DATE:20261113
SUMMARY:Mission B
END:VEVENT
BEGIN:VEVENT
UID:7
DTSTART;VALUE=DATE:20261013
DTEND;VALUE=DATE:20261014
SUMMARY:--Travail chez un tel--
END:VEVENT
END:VCALENDAR
"""


def cal():
    return icalendar.Calendar.from_ical(ICS)


def test_recap_octobre():
    oct_ = calculer_recap(cal(), 2026)[10]
    assert oct_["Mission A"] == 2.5
    assert oct_["Mission B"] == 0.5
    assert oct_["OFF"] == 1
    # l'événement horaire "Mission C" est ignoré
    assert "Mission C" not in oct_
    # 22 jours ouvrés - 4 définis (5,6,7(demi+demi),8) = 18 à trier (le 9 compte)
    assert oct_[A_TRIER] == 18
    # "--Travail chez un tel--" est ignoré (le 13 reste à trier)
    assert "--Travail chez un tel--" not in oct_


def test_filtre_mois():
    res = calculer_recap(cal(), 2026, [11])
    assert list(res.keys()) == [11]
    assert res[11]["Mission B"] == 1


def test_mois_vide():
    assert not calculer_recap(cal(), 2026, [2]).get(1)
