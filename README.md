# ZbxView — landing page

Public website for the **ZbxView** app (a mobile Zabbix client).
Served via GitHub Pages: <https://radekpavlik.github.io/zbxview/>

- `index.html` — landing page (hero, features, editions, about).
- `privacy.html` — privacy policy (the URL required by Google Play).
- `styles.css` — self-contained styles (no external fonts/CDNs).
- `assets/` — app icon, developer logo; drop screenshots here.

## How to add screenshots
The "Podívej se dovnitř" carousel is filled from `assets/screens.json`:
`{"mobile":[{"full":"assets/x.jpg","thumb":"assets/thumbs/x.jpg"}, ...], "tv":[...], "watch":[...]}`
(shown in that order; a tab with no entries is hidden). Watch entries may add
`"shape":"rect"` for Apple Watch shots (rounded square instead of a circle).

Current shots are renders of the Design canvas boards, named
`scr_<tab>_<nn>_<board>.jpg` (phone 1080x2337, TV 1920x1080, watch 454x454,
JPEG q85) with a thumbnail of the same name in `assets/thumbs/` (max 480 px).
The hero and feature sections use `shot1_tablet.jpg`, `shot7_mobile.jpg`,
`shot8_mobile.jpg`, `shot12_mobile.jpg`, `shot33_tv.jpg` and `shot46_watch.jpg`.

## Custom domain (optional, later)
Buy a domain (e.g. `zbxview.app`), add a `CNAME` file with the domain, and
point DNS to GitHub Pages.
