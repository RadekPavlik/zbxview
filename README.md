# ZbxView — landing page

Public website for the **ZbxView** app (a mobile Zabbix client).
Served via GitHub Pages: <https://radekpavlik.github.io/zbxview/>

- `index.html` — landing page (hero, features, editions, about).
- `privacy.html` — privacy policy (the URL required by Google Play).
- `styles.css` — self-contained styles (no external fonts/CDNs).
- `assets/` — app icon, developer logo; drop screenshots here.

## How to add screenshots
Drop JPGs in `assets/` named `shot<N>_<group>.jpg`, where `<group>` is one of
`tv`, `phone`, `tablet` — e.g. `shot1_tablet.jpg`, `shot2_tablet.jpg`,
`shot1_phone.jpg`. Number them from 1 upward (small gaps are tolerated).

The gallery auto-discovers them: it shows an environment tab (TV / Telefon /
Tablet) **only** for groups that have at least one file, renders each shot in
the matching device frame, and hides empty groups. No HTML editing needed —
just add the files, commit and push.

## Custom domain (optional, later)
Buy a domain (e.g. `zbxview.app`), add a `CNAME` file with the domain, and
point DNS to GitHub Pages.
