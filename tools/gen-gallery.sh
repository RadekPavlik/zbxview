#!/usr/bin/env bash
# Generate small gallery thumbnails + a manifest (assets/screens.json) from the
# full screenshots (assets/shot<N>_<group>.<ext>). Run by the thumbnails
# workflow on every push that touches the screenshots. Requires ImageMagick.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p assets/thumbs

declare -A BYGRP   # group -> lines "N|full|thumb"

for f in assets/shot*_*.*; do
  [ -e "$f" ] || continue
  base="$(basename "$f")"
  if [[ "$base" =~ ^shot([0-9]+)_([A-Za-z]+)\.(jpg|jpeg|png|webp|JPG|JPEG|PNG|WEBP)$ ]]; then
    n="${BASH_REMATCH[1]}"
    grp="$(printf '%s' "${BASH_REMATCH[2]}" | tr '[:upper:]' '[:lower:]')"
    thumb="assets/thumbs/${base%.*}.jpg"
    # (re)build the thumbnail if missing or the source is newer
    if [ ! -f "$thumb" ] || [ "$f" -nt "$thumb" ]; then
      convert "$f" -auto-orient -strip -resize 480x480\> -quality 72 "$thumb"
      echo "thumb: $thumb"
    fi
    BYGRP[$grp]+="$n|$f|$thumb"$'\n'
  fi
done

# prune orphan thumbnails whose source no longer exists
for t in assets/thumbs/*.jpg; do
  [ -e "$t" ] || continue
  tb="$(basename "$t" .jpg)"
  if ! ls assets/"$tb".* >/dev/null 2>&1; then rm -f "$t"; echo "pruned: $t"; fi
done

# build JSON manifest
json="{"
first=1
for grp in "${!BYGRP[@]}"; do
  entries="$(printf '%s' "${BYGRP[$grp]}" | sort -t'|' -k1,1n)"
  arr=""; ef=1
  while IFS='|' read -r n full thumb; do
    [ -z "${n:-}" ] && continue
    if [ $ef -eq 1 ]; then ef=0; else arr+=","; fi
    arr+="{\"full\":\"$full\",\"thumb\":\"$thumb\"}"
  done <<< "$entries"
  if [ $first -eq 1 ]; then first=0; else json+=","; fi
  json+="\"$grp\":[$arr]"
done
json+="}"

printf '%s\n' "$json" > assets/screens.json
echo "--- assets/screens.json ---"
cat assets/screens.json
