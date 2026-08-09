# Paper ↔ Evidence synchronization layer — sync1

## Svrha

Ovaj sloj razdvaja **zaključanu analitičku istinu** od njezina prikaza. Rad (`.docx`) i web companion (`.html`) više ne bi smjeli ručno održavati verziju, obuhvat i ključne nalaze kao odvojene vrijednosti.

## Kanonske datoteke

- `release.json` — release ID, dataset/web verzije, data-lock, 180→178→175 obuhvat, aktualno testno stanje i putanje do kanonskih artefakata.
- `claims.json` — stabilni `CLAIM-*` identifikatori za H1–H5/H4'/H4b, procjene, epistemološki status i veze prema radu/webu.
- `MANIFEST.json` — ostaje autoritet za pune SHA-256 otiske zaključanih artefakata.
- `output/results_snapshot.json` — ostaje autoritet za strojno čitljive analitičke rezultate.

## Prikazi

- `Rad_REKTOROVA_v7_SYNC.docx` — akademski/narativni prikaz istog releasea.
- `izvori_v8_SYNC.html` — interaktivni dokazni prikaz istog releasea; dataset ostaje `v7`, web companion je `v8-sync`.

## Pravila protiv drifta

1. Dataset se ne mijenja zbog promjene dizajna weba ili teksta rada.
2. `237/237` je aktualno testno stanje zatečeno na web companionu; `217/217` ostaje povijesni korak revizije u Tablici D1, a dodan je zaseban završni sinkronizacijski redak `237/237 PASS`.
3. `36 × 5 = 180` je teorijski opseg; dvije 2017. jedinice nisu dio panela → `178`; tri od tih redaka nemaju dokumentiran nazivnik izlaznosti → `175` potpunih izlaznosti.
4. Za H2 web može imati `34` statusna zapisa kategorije „raspoloživa mjesta”, ali samo `11` službeno verificiranih brojčanih vrijednosti ulazi u omjer kandidata po mjestu. Nema imputacije.
5. Konfirmacijski i eksplorativni nalazi ne smiju se spajati. H4' i H4b uvijek moraju biti označeni kao eksplorativni.
6. PSPP provjera naziva se **neovisna računska/softverska reprodukcija**, jer koristi istu zaključanu bazu; nije neovisno ponovno prikupljanje podataka.
7. Svaka promjena vrijednosti u `release.json` ili `claims.json` mora aktivirati validator i, ako se radi o zaključanom analitičkom artefaktu, novi lock/release prema pravilima projekta.

## Lokalna validacija

Pokrenuti:

```bash
python validate_paper_evidence_sync.py .
```

Validator provjerava da se release ID, 180→178→175, H2 34/11, claim ID-jevi, 237/237 i ključni nazivi nalaze u oba prikaza. To je dodatni **sync drift detector** i ne treba ga retroaktivno pribrajati postojećem službenom broju `237/237` dok se stvarno ne uključi u glavni testni paket repozitorija.

## Sljedeći korak u repozitoriju

Idealno je izmijeniti generatore tako da Word/HTML ne sadrže ručno upisane release vrijednosti, nego da ih pri buildu čitaju iz `release.json` i `claims.json`. Nakon toga CI treba redom pokrenuti: analitičke testove → generiranje rada/web-stranice → sync validator → link checker → hash/manifest provjeru.
