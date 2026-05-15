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


SCENARIOS: list[tuple[str, str, str]] = [
    (
        "Je suis un visiteur (non connecté).",
        "Je ne remplis pas le champ e-mail ou le champ password du login "
        "administrateur et je clique sur le bouton \"Se connecter\".",
        "Je reste sur la page Login et je suis invité à remplir le champ "
        "manquant.",
    ),
    (
        "Je suis un visiteur (non connecté).",
        "Je remplis le champ e-mail du login administrateur au mauvais format "
        "(sans la forme chaîne@chaîne) et je clique sur le bouton "
        "\"Se connecter\".",
        "Je reste sur la page Login et je suis invité à remplir le champ "
        "e-mail au bon format.",
    ),
    (
        "Je suis un visiteur (non connecté).",
        "Je remplis le champ e-mail du login administrateur au bon format "
        "(sous la forme chaîne@chaîne), le champ password du login "
        "administrateur et je clique sur le bouton \"Se connecter\".",
        "Je suis envoyé sur la page Dashboard.",
    ),
    (
        "Je suis connecté en tant qu'administrateur.",
        "Je clique sur un ticket de note de frais et il est en statut "
        "“en attente”.",
        "Le formulaire de la note de frais est affiché avec l'ensemble des "
        "champs remplis sauf son statut. Il est modifiable.",
    ),
    (
        "Je suis connecté en tant qu'administrateur et j'ai cliqué sur un "
        "ticket “en attente”.",
        "Je clique sur le champ \"commentaire\".",
        "Je peux insérer un commentaire.",
    ),
    (
        "Je suis connecté en tant qu'administrateur et j'ai cliqué sur un "
        "ticket “en attente”.",
        "Je clique sur le bouton “accepter”.",
        "Le statut de la note de frais apparaît comme \"accepté\" dans le "
        "feed des notes de frais. Le nombre de notes de frais du groupe "
        "“accepté” est incrémenté de 1 et le statut apparaît comme "
        "“accepté” dans le tableau de notes de frais de l'employé "
        "qui l'avait envoyée.",
    ),
    (
        "Je suis connecté en tant qu'administrateur et j'ai cliqué sur un "
        "ticket “en attente”.",
        "Je clique sur le bouton “refuser”.",
        "Le statut de la note de frais apparaît comme “refusé” "
        "dans le feed des notes de frais. Le nombre de notes de frais du "
        "groupe “refusé” est incrémenté de 1 et le statut "
        "apparaît comme “refusé” dans le tableau de notes de "
        "frais de l'employé qui l'avait envoyée.",
    ),
    (
        "Je suis connecté en tant qu'administrateur.",
        "Je clique sur un ticket de note de frais et il est en statut "
        "“accepté” ou “refusé”.",
        "Le formulaire de la note de frais ticket est affiché avec "
        "l'ensemble des champs remplis y compris son statut. Il n'est plus "
        "modifiable.",
    ),
    (
        "Je suis connecté en tant qu'administrateur et j'ai cliqué sur une "
        "note de frais en statut “en attente”, ou “accepté"
        "” ou “refusé”.",
        "Je clique sur le bouton Visualiser.",
        "Une modale apparaît avec le PDF du justificatif.",
    ),
    (
        "Je suis connecté en tant qu'administrateur et j'ai cliqué sur une "
        "note de frais en statut “en attente”, ou “accepté"
        "” ou “refusé”.",
        "Je clique sur le bouton \"Télécharger\".",
        "Le PDF du justificatif est téléchargé.",
    ),
    (
        "Je suis connecté en tant qu'administrateur et je suis sur la page "
        "Dashboard.",
        "Je clique sur le bouton \"Se déconnecter\" de la barre verticale.",
        "Je suis envoyé à la page Login.",
    ),
    (
        "Je suis connecté en tant qu'administrateur et je suis sur la page "
        "Dashboard.",
        "Je clique sur le bouton \"Retour\" en arrière de la navigation.",
        "Je reste sur la page Dashboard.",
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

    for index, (given, when, then) in enumerate(SCENARIOS, start=1):
        table = _scenario_table(index, given, when, then, styles)
        story.append(KeepTogether([table, Spacer(1, 0.4 * cm)]))

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
