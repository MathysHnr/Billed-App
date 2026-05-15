#!/usr/bin/env bash
# Convertit le plan de test E2E (Word) en PDF, conservant la mise en page
# d'origine. Le PDF est généré à la racine du projet sous le nom de livrable
# attendu par OpenClassrooms.
#
# Prérequis : libreoffice-writer (sur Debian/Ubuntu : `apt install libreoffice-writer`).
#
# Usage : ./docs/convert_e2e_plan_to_pdf.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

SOURCE_DOCX="${SCRIPT_DIR}/BilledE2E_parcours_administrateur.docx"
OUTPUT_PDF="${REPO_ROOT}/Henneron_Mathys_3_plan_de_test_end_to_end.pdf"
TMP_PROFILE="$(mktemp -d)"

trap 'rm -rf "${TMP_PROFILE}"' EXIT

soffice --headless \
    "-env:UserInstallation=file://${TMP_PROFILE}" \
    --convert-to pdf "${SOURCE_DOCX}" \
    --outdir "${REPO_ROOT}" >/dev/null

mv "${REPO_ROOT}/BilledE2E_parcours_administrateur.pdf" "${OUTPUT_PDF}"
echo "PDF généré : ${OUTPUT_PDF}"
