# Reproducibility artifact recovery status

Datum provjere: 2026-08-09

## Verificirano pronađeni zaključani artefakti

Sljedeći artefakti pronađeni su u izvornom `rektorova_reproducibility_v2_H2_LOCK.zip` i njihovi SHA-256 otisci podudaraju se sa završnim `REKTOROVA_SNAPSHOT_INDEX_UNDER_50MB.zip` manifestom:

| Artefakt | SHA-256 |
|---|---|
| `data/final/panel_wide.csv` | `13f8b3f1e50b9711a3c3e18bb1c460122104a713dbd488a7e926869658666263` |
| `data/final/panel_long.csv` | `888cd692e2c0c90c408390f5d4059d6a95c1acb709ffcf08e007e064f9edef29` |
| `data/final/sources.csv` | `0db833ed8ecc35cef554eed0cf447f90ba787a7d06922f09aeb250d3680a2df7` |
| `analysis/results_snapshot.json` | `d9dad0baab73b41682a0dda8cac3242678bd43c36891d9bb8e56e3f661b8d354` |
| `evidence/DECISIONS.md` | `868d641f6cdfcdd0d624a81643608f2163f290f46b330c5d11f2c55636bd6c3c` |

Panel ima 178 redaka, a `izlaznost_sveuc` je potpuna u 175 redaka. To je konzistentno s release funnelom `180 → 178 → 175`.

## Originalni artefakti koji nisu pronađeni

Prema odobrenom fail-closed planu ne smiju se rekonstruirati iz Worda ili HTML-a:

- `evidence/provenance.json`
- `analysis/replication/provjera.sps`
- `analysis/replication/usporedba.csv`

Pretraženi su: korisnički Library, `REKTOROVA_SNAPSHOT_INDEX_UNDER_50MB.zip`, `REKTOROVA_SNAPSHOT_DIO_11_OD_13_UNDER_50MB.zip`, `rektorova_reproducibility_v2_H2_LOCK.zip`, `REKTOROVA_APSOLUTNO_SVE_MASTER_ARCHIV.zip` i `REKTOROVA_v3_H2_JURY_FINAL_REVIEW_PACKAGE.zip`.

## Posljedica

Task 3 ne smije biti označen GREEN, a Tasks 4–12 ne smiju tvrditi punu reproducibilnost dok se ne dogodi jedno od sljedećeg:

1. pronađu se i uvezu originalna tri artefakta; ili
2. autori eksplicitno odobre stvaranje novog, transparentno označenog replikacijskog/provenance sloja iz zaključane baze, uz novi research release identifikator bez promjene zaključanih empirijskih podataka.
