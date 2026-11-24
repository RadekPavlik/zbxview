#!/usr/bin/env bash
# Generate small gallery thumbnails (assets/thumbs/) for the screenshots
# (assets/shot*.* and assets/scr_*.*). Run by the thumbnails workflow.
# The gallery itself - which screenshots, in which order - is assets/screens.json,
# curated by hand (it follows the user's path through the app). This script
# never writes it. Requires ImageMagick.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p assets/thumbs

for f in assets/shot*.* assets/scr_*.*; do
  [ -e "$f" ] || continue
  base="$(basename "$f")"
  [[ "$base" =~ \.(jpg|jpeg|png|webp|JPG|JPEG|PNG|WEBP)$ ]] || continue
  thumb="assets/thumbs/${base%.*}.jpg"
  # (re)build the thumbnail if missing or the source is newer
  if [ ! -f "$thumb" ] || [ "$f" -nt "$thumb" ]; then
    convert "$f" -auto-orient -strip -resize 480x480\> -quality 72 "$thumb"
    echo "thumb: $thumb"
  fi
done

# prune orphan thumbnails whose source no longer exists
for t in assets/thumbs/*.jpg; do
  [ -e "$t" ] || continue
  tb="$(basename "$t" .jpg)"
  if ! ls assets/"$tb".* >/dev/null 2>&1; then rm -f "$t"; echo "pruned: $t"; fi
done

# every entry of the hand-made manifest must point at existing files
if [ -f assets/screens.json ]; then
  missing=$(grep -o '"assets/[^"]*"' assets/screens.json | tr -d '"' | while read -r p; do [ -e "$p" ] || echo "$p"; done)
  if [ -n "$missing" ]; then echo "screens.json points at missing files:"; echo "$missing"; exit 1; fi
fi
