"""Génère le PDF du plan de tests E2E — parcours administrateur RH.

Le rendu se fait via WeasyPrint à partir du fichier HTML/CSS source
``docs/e2e_admin_plan.html``. Le PDF est écrit à la racine du projet
sous le nom de livrable attendu.

Usage :
    python3 docs/generate_e2e_admin_plan.py [chemin_sortie.pdf]
"""

from __future__ import annotations

import sys
from pathlib import Path

from weasyprint import HTML


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_HTML = REPO_ROOT / "docs" / "e2e_admin_plan.html"
DEFAULT_OUTPUT = REPO_ROOT / "Henneron_Mathys_4_plan_test_admin_052026.pdf"


def build(output_path: Path) -> Path:
    HTML(filename=str(SOURCE_HTML)).write_pdf(str(output_path))
    return output_path


def main(argv: list[str]) -> int:
    output = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    built = build(output)
    print(f"PDF généré : {built}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
