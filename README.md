# ZbxView — landing page

Public website for the **ZbxView** app (a mobile Zabbix client).
Served via GitHub Pages: <https://radekpavlik.github.io/zbxview/>

- `index.html` — landing page (hero, features, editions, about).
- `privacy.html` — privacy policy (the URL required by Google Play).
- `styles.css` — self-contained styles (no external fonts/CDNs).
- `assets/` — app icon, developer logo; drop screenshots here.

## How to add screenshots
Drop images in `assets/` named `shot<N>_<group>.<ext>`, where:
- `<group>` = `tv` | `mobile` | `tablet` (the device tab it appears under),
- `<ext>` = `jpg`, `png`, `jpeg` or `webp`,
- `<N>` = any number up to 60; numbering may start anywhere and have gaps
  (shots are shown in numeric order).

Examples: `shot1_tablet.jpg`, `shot17_mobile.png`, `shot1_tv.jpg`.

The gallery auto-discovers them: it shows an environment tab (TV / Telefon /
Tablet) **only** for groups that have at least one file, renders each shot in
the matching device frame, supports grab-and-drag scrolling, and click-to-zoom
(lightbox). No HTML editing needed — just add the files, commit and push.

## Custom domain (optional, later)
Buy a domain (e.g. `zbxview.app`), add a `CNAME` file with the domain, and
point DNS to GitHub Pages.
