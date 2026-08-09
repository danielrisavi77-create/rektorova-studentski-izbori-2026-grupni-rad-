# rektorova-studentski-izbori-2026 (grupni rad)

## Dizajn reproducibilnog istraživačkog sustava

**Status:** odobren dizajn, spreman za implementacijski plan  
**Datum:** 2026-08-09  
**Repo:** `danielrisavi77-create/rektorova-studentski-izbori-2026-grupni-rad-`  
**Projektni naslov:** `rektorova-studentski-izbori-2026 (grupni rad)`  
**Trenutačna vidljivost repozitorija:** public

---

## 1. Cilj sustava

Repozitorij nije samo spremište rada i priloga. On mora biti kanonski, reproducibilni istraživački paket iz kojega se može:

1. provjeriti svaka ključna brojka u radu;
2. pratiti svaka ključna tvrdnja do analitičkog rezultata i izvornog podatka;
3. reproducirati ključne statističke rezultate;
4. dokazati integritet zaključanih artefakata SHA-256 vrijednostima;
5. automatski otkriti neslaganje između rada, web-stranice i strojnog izvora istine;
6. izgraditi web-sloj bez ručnog prepisivanja zaključanih brojki;
7. napraviti verzionirani release prikladan za Zenodo/OSF i DOI;
8. jasno razlikovati konfirmacijske, parcijalne i eksplorativne rezultate.

Temeljno načelo je **jedna analitička istina, više prikaza**. Word/PDF rad i web-stranica nisu dva neovisna izvora, nego dvije projekcije istih zaključanih podataka i rezultata.

---

## 2. Kanonski izvori istine

Sustav koristi strogo definiranu hijerarhiju artefakata.

### 2.1. Zaključani podatci

`data/final/` sadržava samo finalne analitičke ulaze. Podatci se nakon zaključavanja ne uređuju ručno. Svaka promjena zahtijeva novi lock cycle i novu verziju releasea.

Planirani ključni artefakti:

- `panel_wide.csv`
- `panel_long.csv`
- `sources.csv`

### 2.2. Kanonski rezultati

`analysis/results_snapshot.json` sadržava brojčane rezultate koji se citiraju u radu i prikazuju na webu. To je jedini strojni izvor za zaključane procjene H1, H2, H3, H4, H4', H4b i H5.

Nijedna zaključana procjena ne smije biti ručno duplicirana kao autoritativna vrijednost u više datoteka.

### 2.3. Registar tvrdnji

`claims.json` povezuje znanstvenu tvrdnju s:

- stabilnim `CLAIM-*` identifikatorom;
- tipom analize: konfirmacijska / parcijalna / eksplorativna;
- procjenom i intervalom;
- uzorkom i brojem klastera gdje je relevantno;
- ključem u `results_snapshot.json`;
- tablicom, slikom i poglavljem u radu;
- web-anchorom;
- skriptom koja generira rezultat;
- relevantnim podatkovnim artefaktom;
- statusom dokaza i ograničenjima.

### 2.4. Release metadata

`release.json` sadržava verziju cijelog istraživačkog releasea, uključujući:

- research release;
- paper version;
- dataset version;
- lock cycle;
- release date;
- broj službenih testova;
- broj sinkronizacijskih testova;
- broj teorijskih jedinica-ciklusa;
- broj redaka panela;
- broj redaka s potpunom izlaznošću;
- hash ključnih artefakata;
- status releasea.

`release.json` je jedini autoritativni izvor za release-level metapodatke. Git commit SHA ne upisuje se kao samoreferencijalno kanonsko polje u istu datoteku koja se commita i hashira. Točan commit svakog javnog releasea određuju Git tag i GitHub release metadata. Ako je potreban strojno čitljiv commit u distributivnom paketu, CI ga pri izradi artefakta zapisuje u zasebni generirani `release-build.json`, koji nije kanonski ulaz niti dio hash petlje.

---

## 3. Obvezni prikaz uzorka: 180 → 178 → 175

Sustav mora identično prikazivati isti sampling funnel u radu i na webu:

- 36 sastavnica × 5 ciklusa = 180 teorijskih jedinica-ciklusa;
- 2 nisu dio analitičkog panela;
- 178 analitičkih redaka;
- 3 nemaju izračunljivu izlaznost zbog nedostupnog nazivnika;
- 175 redaka s potpunom izlaznošću.

Te vrijednosti ne smiju se ručno unositi u Word i HTML kao neovisne konstante. Generator ili validator ih mora povlačiti iz kanonskih release/podatkovnih metapodataka.

---

## 4. H2 i status dokumentacije

Sustav mora eksplicitno razlikovati:

- 34 statusna zapisa koji opisuju dokumentacijsku pokrivenost raspoloživih mjesta;
- 11/34 jedinica s numerički i službeno verificiranim brojem mjesta koje ulaze u parcijalnu provjeru omjera kandidata po mjestu.

Web i rad ne smiju formulacijom stvarati dojam da svih 34 jedinice imaju numerički poznat nazivnik.

---

## 5. Arhitektura repozitorija

```text
/
├── README.md
├── CITATION.cff
├── LICENSE
├── MANIFEST.json
├── release.json
├── claims.json
│
├── paper/
│   ├── Rad_REKTOROVA_v7_SYNC.docx
│   ├── PAPER_EVIDENCE_SYNC.md
│   └── generated/
│
├── data/
│   ├── final/
│   │   ├── panel_wide.csv
│   │   ├── panel_long.csv
│   │   └── sources.csv
│   └── README.md
│
├── evidence/
│   ├── provenance.json
│   ├── DECISIONS.md
│   └── source_registry/
│
├── analysis/
│   ├── results_snapshot.json
│   ├── scripts/
│   └── replication/
│       ├── provjera.sps
│       └── usporedba.csv
│
├── web/
│   ├── index.html
│   ├── izvori.html
│   └── assets/
│
├── scripts/
│   ├── build_release.py
│   ├── build_manifest.py
│   ├── build_web.py
│   ├── sync_paper.py
│   └── validate_sync.py
│
├── tests/
│   ├── test_release.py
│   ├── test_claims.py
│   ├── test_dataset.py
│   ├── test_paper_sync.py
│   ├── test_web_sync.py
│   └── test_manifest.py
│
├── docs/
│   ├── methodology/
│   └── superpowers/specs/
│
└── .github/
    └── workflows/
        └── reproducibility.yml
```

Granice modula moraju ostati jasne: podatci nisu generatori, generatori nisu validatori, validatori ne mijenjaju podatke, a web i paper layer nikada ne postaju izvori istine.

---

## 6. Tok podataka

```text
SLUŽBENI IZVORI
      ↓
provenance.json / sources.csv
      ↓
zaključani panel
      ↓
analitičke skripte
      ↓
results_snapshot.json
      ↓
claims.json + release.json
      ↓
MANIFEST.json
      ↓
┌─────────────────────────┐
│                         │
↓                         ↓
RAD                       WEB
↓                         ↓
└──────── validate_sync ──┘
             ↓
       GitHub Actions
             ↓
        release artefakt
```

Svaki sloj smije čitati samo definirane upstream artefakte. Nijedan downstream prikaz ne smije ručno redefinirati zaključani rezultat.

---

## 7. Paper ↔ Evidence sinkronizacija

### 7.1. Rad

Word ostaje glavni urednički format rada kako bi se sačuvao postojeći izgled, stil, numeracija, tablice i grafička struktura. Ne uvodi se potpuna migracija na Quarto u ovoj fazi.

`sync_paper.py` mora prvenstveno provjeravati, a samo gdje je tehnički sigurno ažurirati, strogo označena sinkronizacijska polja. Ne smije nekontrolirano preformatirati dokument.

Obvezne sinkronizirane cjeline:

- release metadata;
- 180 → 178 → 175 funnel;
- H1, H2, H3, H4, H4', H4b i H5 ključne zaključane procjene i statusi;
- konfirmacijsko/parcijalno/eksplorativno označavanje;
- broj službenih i sinkronizacijskih testova;
- hash i release ID u reproducibilnom prilogu;
- Claim-to-Evidence indeks.

### 7.2. Web

Web je interaktivni dokazni sloj. Mora sadržavati:

- sažetak ključnih nalaza;
- evidence cards;
- matricu dokumentacije;
- jasne statusne oznake;
- ograničenja interpretacije;
- pretraživanje sastavnica i tvrdnji;
- sampling funnel;
- reproducibility/download sekciju;
- veze prema `claims.json`, `release.json`, `MANIFEST.json` i podatcima;
- dvosmjerne reference prema poglavljima, tablicama i slikama rada.

Web ne smije sadržavati zaključane brojeve kao ručno održavane neovisne konstante ako su već dostupni iz kanonskih JSON artefakata.

---

## 8. Claim-to-Evidence model

Minimalni claim zapis:

```json
{
  "id": "CLAIM-H1-SIZE",
  "label": "Veličina biračkog tijela",
  "analysis_type": "confirmatory",
  "status": "strongly_supported",
  "result_key": "H1.size_effect",
  "paper": {
    "section": "6",
    "table": "C1",
    "figures": ["9", "16"]
  },
  "web_anchor": "claim-h1-size",
  "limitations": [],
  "artifacts": []
}
```

Schema se formalizira i validira testovima. ID-jevi postaju stabilni nakon prvog javnog releasea.

---

## 9. Provenijencija i izvori

Za svaki izvorni dokument registar čuva najmanje:

- ciklus;
- sastavnicu;
- vrstu dokumenta;
- naslov;
- izvorni URL;
- arhivski URL gdje postoji;
- datum pristupa;
- status dostupnosti;
- način ekstrakcije: strojni / ručni-vizualni;
- status kontrolne provjere;
- napomenu;
- lokalni hash ako se datoteka legalno pohranjuje.

Repozitorij neće automatski redistribuirati službene PDF-ove kada prava distribucije nisu jasna. U takvim slučajevima čuvaju se metapodatci, stabilne poveznice, arhivski trag i dokazna napomena.

Budući da je repo trenutačno public, prije svakog commita treba provjeriti da se ne objavljuju privatni podatci, pristupni tokeni, lokalne putanje s osjetljivim informacijama ili dokumenti za koje ne postoji opravdanje za redistribuciju.

---

## 10. Manifest i integritet

`build_manifest.py` generira `MANIFEST.json` za zaključane artefakte. Manifest mora sadržavati najmanje:

- relativnu putanju;
- SHA-256;
- veličinu datoteke;
- ulogu artefakta;
- release ID;
- oznaku je li artefakt kanonski, generiran ili pomoćni.

Validator mora pasti ako hash zaključanog artefakta više ne odgovara manifestu bez promjene lock cyclea/releasea.

`MANIFEST.json` ne smije uključivati samoga sebe u vlastiti hash skup, a generirani `release-build.json` također se ne tretira kao kanonski zaključani ulaz.

---

## 11. Validacija protiv drifta

`validate_sync.py` mora barem provjeravati:

1. `release.json` ima valjanu shemu;
2. `claims.json` ima valjanu shemu i jedinstvene ID-jeve;
3. svaki claim referencira postojeći `results_snapshot` ključ;
4. ključne brojke u paper layeru podudaraju se s kanonskim rezultatima;
5. ključne brojke u web layeru podudaraju se s kanonskim rezultatima;
6. 180/178/175 je konzistentno u svim slojevima;
7. H2 34 naspram 11/34 nije semantički pogrešno prikazan;
8. status H4' i H4b ostaje eksplorativan;
9. H3 se ne prikazuje kao potvrđen nalaz;
10. H2 se ne prikazuje kao potpuno potvrđena kauzalna hipoteza;
11. broj testova i lock cycle ne driftaju;
12. manifest hash vrijednosti odgovaraju datotekama;
13. svi unutarnji web-anchor linkovi postoje;
14. svi Claim-to-Evidence linkovi upućuju na postojeće objekte;
15. svi kanonski artefakti uključeni su u manifest.

Validator je read-only: otkriva problem i vraća non-zero exit code, ali ne popravlja podatke automatski.

---

## 12. Testiranje

Razvoj sinkronizacijskog sustava slijedi TDD.

### Dataset tests

- očekivani broj redaka;
- jedinstvenost ključeva sastavnica-ciklus;
- dozvoljeni missing statusi;
- formule izlaznosti gdje su brojnik i nazivnik dostupni;
- osnovni checksum totals.

### Result tests

- kanonske vrijednosti postoje;
- tipovi i jedinice su valjani;
- intervali su numerički konzistentni;
- claim status odgovara snapshotu.

### Sync tests

- paper ↔ snapshot;
- web ↔ snapshot;
- paper ↔ release;
- web ↔ release;
- claim ↔ paper ↔ web.

### Reproducibility tests

- PSPP usporedba ključnih brojki;
- deterministički generatori;
- fiksirana sjemena gdje postoje stohastičke operacije;
- dokumentirane verzije paketa.

---

## 13. GitHub Actions CI

`.github/workflows/reproducibility.yml` pokreće se na:

- `push` na glavnu granu;
- svaki pull request;
- ručno pokretanje;
- release/tag workflow kada bude uveden.

Minimalni CI pipeline:

1. checkout;
2. postavljanje podržane Python verzije;
3. instalacija zaključanih dependencija;
4. JSON/schema validacija;
5. dataset tests;
6. result/claim tests;
7. manifest provjera;
8. paper-web drift provjera;
9. web link/internal anchor provjera;
10. reproducibility validator;
11. objava sažetka provjera.

CI mora biti blokirajući za sinkronizacijski drift. Crveni CI znači da release nije reproducibilno konzistentan.

---

## 14. Release proces

Release se smije označiti kao finalan samo kada:

- svi zaključani ulazi imaju hash;
- svi testovi prolaze;
- `validate_sync.py` prolazi;
- `MANIFEST.json` je svježe generiran;
- rad i web prikazuju iste ključne rezultate;
- svi claimovi imaju dokazni trag;
- nema nedokumentiranih ručnih promjena zaključanih vrijednosti;
- Git tag pokazuje na commit koji je prošao završni CI.

Plan oznaka:

- razvojne verzije: `v0.x` ili interni `SYNC*`;
- prvi javni kanonski release: verzija definirana finalnim stanjem rada;
- svaki kasniji podatkovni ili analitički lock dobiva novu verziju.

Javni release kasnije se može povezati sa Zenodo/OSF DOI-em bez promjene temeljnog modela.

---

## 15. README kao javni ulaz

README mora jednostavno objasniti:

1. što istraživanje proučava;
2. da je riječ o grupnom radu;
3. što se nalazi u repozitoriju;
4. kako provjeriti rezultat;
5. kako reproducirati ključne brojke;
6. što znače 180 → 178 → 175;
7. gdje su ograničenja podataka;
8. kako citirati rad/dataset;
9. koji je aktualni release i lock status.

README ne smije preuveličavati stupanj kauzalne identifikacije ili potpunost dokumentacije.

---

## 16. Licenciranje i citiranje

Repo mora odvojiti:

- licencu autorskog koda;
- status/licencu izvedenih podatkovnih artefakata;
- prava trećih strana nad službenim izvornim dokumentima.

`CITATION.cff` mora sadržavati sve autore grupnog rada redoslijedom koji koristi finalni rad. Imena autora ne pretpostavljaju se iz GitHub računa; preuzimaju se iz zaključane finalne verzije rada/release metapodataka.

---

## 17. Error handling i fail-closed pravila

Sustav koristi princip **fail closed**:

- nepoznat rezultat → build pada;
- nedostajući claim reference → build pada;
- hash mismatch → build pada;
- neočekivana promjena zaključanog panela → build pada;
- nedostajući obvezni release field → build pada;
- broj koji se razlikuje između weba i snapshota → build pada.

Za nestabilne vanjske URL-ove pristup je drugačiji: link checker prijavljuje status, ali povijesni nestanak službenog dokumenta ne smije sam po sebi mijenjati zaključane analitičke podatke. Takav slučaj prelazi u provenance status i arhivski workflow.

---

## 18. Sigurnost od nenamjernih izmjena

Finalni analitički podatci tretiraju se kao immutable artefakti unutar pojedinog releasea.

Preporučeni workflow za promjene:

1. promjena ide na feature/review branch;
2. testovi moraju proći;
3. ako se mijenja zaključani podatak, mora se eksplicitno otvoriti novi lock cycle;
4. ažuriraju se snapshot, claims, release i manifest;
5. svi downstream prikazi regeneriraju se ili ponovno validiraju;
6. tek tada merge.

---

## 19. Što se namjerno NE radi u ovoj fazi

Radi kontrole opsega, prva implementacija neće:

- prepisati cijeli Word rad u Quarto/LaTeX;
- automatski mijenjati znanstvene zaključke;
- automatski imputirati nedostajuće podatke;
- redistribuirati sve službene PDF-ove bez provjere prava;
- uvoditi bazu podataka ili backend ako statički reproducibilni repo to ne zahtijeva;
- mijenjati zaključane statističke modele bez zasebne metodološke odluke.

---

## 20. Kriteriji uspjeha prve pune implementacije

Prva implementacija smatra se završenom kada vrijedi sve sljedeće:

1. repo ima definiranu strukturu i jasnu dokumentaciju;
2. postoje kanonski `release.json` i `claims.json`;
3. postoje finalni podatkovni i analitički artefakti potrebni za validaciju;
4. `MANIFEST.json` generira se automatski;
5. web companion nalazi se u `web/` i koristi sinkronizirane vrijednosti;
6. Word rad nalazi se u `paper/` i prolazi paper sync provjeru;
7. sampling funnel je identičan u svim slojevima;
8. H2 34/11 razlika je eksplicitna i testirana;
9. claim registry pokriva H1, H2, H3, H4, H4', H4b i H5;
10. CI prolazi na glavnoj grani;
11. namjerno uveden drift uzrokuje pad CI-ja;
12. reproducibility README omogućuje trećoj osobi razumjeti kako provjeriti ključni rezultat;
13. finalni release može se izvesti bez ručnog prepisivanja zaključanih brojki između rada i weba.

---

## 21. Preporučeni implementacijski redoslijed

1. osnovna struktura repoa i README;
2. kanonski release/claim schema;
3. uvoz zaključanih artefakata;
4. manifest generator;
5. validator i TDD testovi;
6. paper sync provjera;
7. web sync i generiranje;
8. CI workflow;
9. intentional-drift test;
10. finalni release audit;
11. tek nakon stabilizacije: javni DOI/arhiviranje.

Ovaj redoslijed minimizira rizik da se prvo izgradi atraktivan prikaz, a tek kasnije otkrije da nema strogo definiran izvor istine.
