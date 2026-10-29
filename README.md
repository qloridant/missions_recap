# missions-recap

Récapitulatif mensuel du nombre de jours par mission, à partir d'un calendrier
exporté de Thunderbird (ou tout fichier `.ics`).

## Convention d'écriture des événements

| Titre de l'événement   | Effet                         |
|------------------------|-------------------------------|
| `Mission A`            | 1 jour pour *Mission A*       |
| `Mission A (matin)`    | 0,5 jour pour *Mission A*     |
| `Mission B (aprem)`    | 0,5 jour pour *Mission B*     |
| `OFF`                  | 1 jour pour *OFF*             |

Un jour de semaine (lun-ven) sans événement, ou à moitié rempli, ajoute le
reste dans la catégorie **À trier**. Les week-ends ne comptent que s'ils
contiennent un événement.

> **Seuls les événements « journée entière » (*All day event*) sont pris en
> compte.** Les événements avec des horaires sont ignorés.

## Ignorer un événement

Un événement dont le titre **commence par `--`** est totalement ignoré, par
exemple `--Travail chez un tel--` ou `--RDV perso`. Il n'est pas compté, et le
jour reste « À trier » s'il n'a pas d'autre événement.

## Export depuis Thunderbird

Clic droit sur le calendrier → *Exporter le calendrier…* → **iCalendar (.ics)**.

## Utilisation

Sans rien installer (avec [uv](https://docs.astral.sh/uv/)) :

```bash
uvx missions-recap calendrier.ics 2026
```

Ou installé comme outil :

```bash
uv tool install missions-recap
missions-recap calendrier.ics 2026 --csv recap.csv
```

Filtrer par mois (un ou plusieurs) :

```bash
missions-recap calendrier.ics 2026 -m 10
missions-recap calendrier.ics 2026 --mois 9 10 11
```

## Développement

```bash
uv sync
uv run pytest
uv run missions-recap mon.ics 2026
```

## Publication sur PyPI

```bash
uv build
uv publish          # nécessite un token PyPI : UV_PUBLISH_TOKEN=pypi-...
```
