#!/usr/bin/env bash
set -euo pipefail
# Extract TYNDP_Products_complete_upload_bundle.zip first.
# Run from the extracted directory with git authentication enabled.
DEST="${1:-TYNDP_Products}"
if [ -e "$DEST/.git" ]; then
  echo "Existing Git checkout: refusing to overwrite" >&2
  exit 1
fi
git clone https://github.com/AlOussama/TYNDP_Products.git "$DEST"
cp -R docs archive code revision_snapshot provenance "$DEST"/
cd "$DEST"
git add docs archive code revision_snapshot provenance
if git diff --cached --quiet; then echo "Nothing to commit"; exit 0; fi
git commit -m "Import all IoSN reports, code, tests, analyses and archival artifacts"
git push origin HEAD:main
