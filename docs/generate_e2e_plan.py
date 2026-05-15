"""Générateur du plan de test End-to-End du parcours administrateur RH.

Produit un PDF formaté avec en-tête « Billed », un titre principal puis une
suite de scénarios au format Given / When / Then. La source des scénarios est
définie ci-dessous dans la constante ``SCENARIOS`` ; pour modifier le plan il
suffit d'éditer cette liste ou de mettre à jour le fichier
``docs/e2e_test_plan.md`` puis de reproduire les changements ici.

Usage :
    python3 docs/generate_e2e_plan.py [chemin_sortie.pdf]
"""

from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BILLED_BLUE = colors.HexColor("#0D5AE5")
LIGHT_GREY = colors.HexColor("#F5F5F5")
DARK_TEXT = colors.HexColor("#1F1F1F")

DEFAULT_OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "Henneron_Mathys_3_plan_de_test_end_to_end.pdf"
)


SECTIONS: list[tuple[str, list[tuple[str, str, str]]]] = [
    (
        "I. Authentification (page Login)",
        [
            (
                "Je suis un visiteur (non connecté).",
                "Je ne remplis pas le champ e-mail ou le champ password du login "
                "administrateur et je clique sur le bouton « Se connecter ».",
                "Je reste sur la page Login et je suis invité à remplir le champ "
                "manquant.",
            ),
            (
                "Je suis un visiteur (non connecté).",
                "Je remplis le champ e-mail du login administrateur au mauvais "
                "format (sans la forme chaîne@chaîne) et je clique sur le bouton "
                "« Se connecter ».",
                "Je reste sur la page Login et je suis invité à remplir le champ "
                "e-mail au bon format.",
            ),
            (
                "Je suis un visiteur (non connecté).",
                "Je remplis le champ e-mail et le champ password du login "
                "administrateur dans le bon format et je clique sur le bouton "
                "« Se connecter ».",
                "Je suis authentifié en tant qu'administrateur RH et je suis "
                "redirigé vers la page Dashboard (« Validations »).",
            ),
            (
                "Je suis un administrateur authentifié sur la page Dashboard.",
                "Je rafraîchis la page ou je reviens sur l'application.",
                "Ma session est conservée (via le localStorage) et je reste sur "
                "la page Dashboard sans devoir me reconnecter.",
            ),
        ],
    ),
    (
        "II. Page Dashboard – vue globale des notes de frais",
        [
            (
                "Je suis un administrateur RH authentifié.",
                "J'arrive sur la page Dashboard.",
                "Je vois trois sections (« En attente », « Validé », « Refusé ») "
                "avec le nombre de notes de frais pour chaque statut, ainsi que "
                "la zone « Validations » à droite avec la grande icône Billed.",
            ),
            (
                "Je suis sur la page Dashboard et au moins une note de frais "
                "existe pour le statut « En attente ».",
                "Je clique sur la flèche de la section « En attente ».",
                "La section se déplie et affiche la liste des cartes des notes "
                "de frais correspondantes (nom de l'employé, libellé, montant, "
                "date, type).",
            ),
            (
                "Je suis sur la page Dashboard et la section « En attente » est "
                "dépliée.",
                "Je clique à nouveau sur la flèche de la même section.",
                "La section se replie et les cartes des notes de frais "
                "associées ne sont plus affichées.",
            ),
            (
                "Je suis sur la page Dashboard et plusieurs sections sont "
                "dépliées simultanément.",
                "Je clique sur la flèche d'une autre section (par exemple "
                "« Validé »).",
                "La section ciblée se déplie indépendamment des autres ; chaque "
                "section conserve son propre état (ouvert/fermé).",
            ),
        ],
    ),
    (
        "III. Page Dashboard – consultation d'une note de frais",
        [
            (
                "Je suis sur la page Dashboard et la section « En attente » est "
                "dépliée.",
                "Je clique sur la carte d'une note de frais.",
                "Le formulaire de détail de la note de frais s'affiche à droite "
                "(type, nom, date, commentaire, montant, TVA, justificatif) et "
                "les boutons « Refuser » et « Accepter » apparaissent car la "
                "note est au statut « En attente ».",
            ),
            (
                "Je suis sur la page Dashboard et le formulaire de détail d'une "
                "note de frais est ouvert.",
                "Je clique une deuxième fois sur la carte de la même note de "
                "frais.",
                "Le formulaire de détail se ferme et la grande icône Billed "
                "(big-billed-icon) réapparaît à droite.",
            ),
            (
                "Je suis sur la page Dashboard et le formulaire de détail d'une "
                "note de frais est ouvert.",
                "Je clique sur l'icône en forme d'œil située dans le "
                "formulaire.",
                "Une modale s'ouvre et affiche le justificatif (image du reçu) "
                "associé à la note de frais.",
            ),
        ],
    ),
    (
        "IV. Page Dashboard – validation / refus d'une note de frais",
        [
            (
                "Je suis sur la page Dashboard et le formulaire d'une note de "
                "frais au statut « En attente » est ouvert.",
                "Je saisis éventuellement un commentaire puis je clique sur le "
                "bouton « Accepter ».",
                "Le statut de la note de frais passe à « accepted », mon "
                "commentaire est enregistré et je suis redirigé vers la vue "
                "principale du Dashboard.",
            ),
            (
                "Je suis sur la page Dashboard et le formulaire d'une note de "
                "frais au statut « En attente » est ouvert.",
                "Je saisis éventuellement un commentaire puis je clique sur le "
                "bouton « Refuser ».",
                "Le statut de la note de frais passe à « refused », mon "
                "commentaire est enregistré et je suis redirigé vers la vue "
                "principale du Dashboard.",
            ),
        ],
    ),
    (
        "V. Déconnexion",
        [
            (
                "Je suis un administrateur RH authentifié sur n'importe quelle "
                "page de l'application.",
                "Je clique sur l'icône de déconnexion dans la barre verticale "
                "gauche.",
                "Ma session est supprimée du localStorage et je suis redirigé "
                "vers la page Login.",
            ),
        ],
    ),
]


def _register_unicode_font() -> str:
    """Enregistre une police TTF supportant les caractères français.

    Retourne le nom de la police à utiliser. Si aucune police TTF n'est
    disponible sur le système, retourne ``Helvetica`` (qui couvre Latin-1 et
    suffit pour le français).
    """

    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont("AppFont", path))
            bold = path.replace("Sans.ttf", "Sans-Bold.ttf").replace(
                "Regular", "Bold"
            )
            if Path(bold).exists():
                pdfmetrics.registerFont(TTFont("AppFont-Bold", bold))
            else:
                pdfmetrics.registerFont(TTFont("AppFont-Bold", path))
            return "AppFont"
    return "Helvetica"


def _styles(font_name: str) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    bold = (
        "AppFont-Bold" if font_name == "AppFont" else "Helvetica-Bold"
    )
    return {
        "logo": ParagraphStyle(
            "logo",
            parent=base["Normal"],
            fontName=bold,
            fontSize=34,
            textColor=BILLED_BLUE,
            alignment=1,  # center
            leading=42,
            spaceAfter=24,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Heading1"],
            fontName=bold,
            fontSize=15,
            textColor=BILLED_BLUE,
            alignment=1,
            leading=20,
            spaceBefore=0,
            spaceAfter=22,
        ),
        "section": ParagraphStyle(
            "section",
            parent=base["Heading2"],
            fontName=bold,
            fontSize=13,
            textColor=BILLED_BLUE,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "label": ParagraphStyle(
            "label",
            parent=base["Normal"],
            fontName=bold,
            fontSize=10,
            textColor=colors.white,
            alignment=1,
            leading=12,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName=font_name,
            fontSize=10,
            textColor=DARK_TEXT,
            leading=13,
        ),
        "scenario_header": ParagraphStyle(
            "scenario_header",
            parent=base["Normal"],
            fontName=bold,
            fontSize=11,
            textColor=colors.white,
            alignment=1,
            leading=14,
        ),
    }


def _scenario_table(index: int, given: str, when: str, then: str, styles):
    header_row = [Paragraph(f"Scénario {index}", styles["scenario_header"])]
    rows = [
        header_row,
        [
            Paragraph("Given", styles["label"]),
            Paragraph(given, styles["cell"]),
        ],
        [
            Paragraph("When", styles["label"]),
            Paragraph(when, styles["cell"]),
        ],
        [
            Paragraph("Then", styles["label"]),
            Paragraph(then, styles["cell"]),
        ],
    ]

    table = Table(
        rows,
        colWidths=[2.6 * cm, 13.6 * cm],
        hAlign="LEFT",
    )
    style = TableStyle(
        [
            ("SPAN", (0, 0), (1, 0)),
            ("BACKGROUND", (0, 0), (-1, 0), BILLED_BLUE),
            ("BACKGROUND", (0, 1), (0, -1), BILLED_BLUE),
            ("BACKGROUND", (1, 1), (1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 0.75, BILLED_BLUE),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BILLED_BLUE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
    table.setStyle(style)
    return table


def build(output_path: Path) -> Path:
    font_name = _register_unicode_font()
    styles = _styles(font_name)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Plan de test End-to-End du parcours administrateur RH",
        author="Mathys Henneron",
    )

    story = []
    story.append(Paragraph("Billed", styles["logo"]))
    story.append(
        Paragraph(
            "Plan de test End-to-End du parcours administrateur RH",
            styles["title"],
        )
    )

    scenario_index = 1
    for section_title, scenarios in SECTIONS:
        story.append(Paragraph(section_title, styles["section"]))
        for given, when, then in scenarios:
            table = _scenario_table(scenario_index, given, when, then, styles)
            story.append(KeepTogether([table, Spacer(1, 0.4 * cm)]))
            scenario_index += 1

    doc.build(story)
    return output_path


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    built = build(output)
    print(f"PDF généré : {built}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
