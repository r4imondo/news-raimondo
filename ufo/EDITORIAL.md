# UFO · News.Raimondo.it — regole per l'edizione automatica

Giornale gemello di News.Raimondo.it, pubblicato in `/ufo/` e NON linkato da nessuna parte.
Grafica e funzionamento sono identici al giornale principale; cambiano solo argomento e quantità.
Valgono TUTTE le regole di `../EDITORIAL.md` (verifica, fonti lette per intero, freschezza 48 ore,
1vs1, approfondimento, copyright, sicurezza, formato di `edition.json`), salvo quanto scritto qui.

## Sezione

Una sola sezione: `uap` → UAP, UFO e alieni (audizioni e documenti di governi e parlamenti, AARO e
Pentagono, NASA, avvistamenti documentati, testimoni con nome e ruolo, ricerca scientifica su vita
extraterrestre, tecnosegnature e SETI, smentite e spiegazioni).

`secs` è sempre `[["uap","UAP, UFO e alieni"]]`. Ogni notizia ha `"sec": "uap"`.
`lead` è la notizia di apertura più rilevante che non sia un 1vs1.

## Quantità e consumo

Al massimo 6 notizie. Al massimo 3 fonti aperte per notizia (più una per la controparte del 1vs1).
Per questo giornale la finestra di freschezza è di 72 ore (non 48): le notizie sul tema sono poche.
Meglio un'edizione corta (anche 1-3 notizie) che notizie vecchie o deboli.

Registro obbligatorio: a OGNI esecuzione aggiungere in fondo a `ufo/LOG.md` una riga
`AAAA-MM-GG HH:MM · notizie pubblicate N (1vs1 M) · ricerche X · pagine aperte Y · note`
e fare commit anche quando non si pubblica una nuova edizione (in quel caso spiegare il motivo
nella riga: per esempio "nessuna notizia valida nelle ultime 72 ore", "push fallito", ecc.).

## Fonti: gerarchia specifica

- Livello 1, primarie: AARO e Dipartimento della Difesa USA, Congresso USA (audizioni, testi di
  legge), NASA, ministeri della Difesa e agenzie di altri Paesi, archivi nazionali, articoli
  scientifici pubblicati, comunicati di osservatori e istituti di ricerca (SETI Institute, ESO…).
- Livello 2, testate generaliste: Reuters, AP, BBC, New York Times, Washington Post, Politico,
  The Guardian, Scientific American, New Scientist, ANSA, Il Post, Corriere, South China Morning Post.
- Livello 3, specializzate (sempre insieme a un'altra fonte di livello 1 o 2): The Debrief,
  NewsNation, Liberation Times, Popular Mechanics, Space.com, Live Science.
- Fonti cinesi e russe: utili per avvistamenti e posizioni ufficiali; i media statali hanno
  l'etichetta "GOV" e la loro posizione va sempre attribuita.
- Solo spunto, mai citati come fonte: canali YouTube e podcast non giornalistici, forum, X/Twitter,
  TikTok, siti senza autore o data.
- Esclusi: video e foto non verificati presentati come prova, siti che vendono prodotti o corsi.

## Rigore

- Distinguere SEMPRE tra fatto verificato, dichiarazione attribuita e ipotesi. Mai presentare
  un'affermazione straordinaria come fatto: scrivere chi la fa e su quale base.
- **1vs1 come formato predefinito: idealmente OGNI notizia è un 1vs1.** Per ogni notizia cercare
  attivamente la controparte: chi propone la spiegazione convenzionale o fa il debunk dello STESSO
  caso (AARO e autorità, astronomi e piloti esperti, analisti di immagini, Mick West/Metabunk,
  Skeptical Inquirer/CSI, CICAP in Italia, scienziati citati da testate di livello 1-2), oppure, se
  la notizia è una smentita, chi sostiene la tesi non convenzionale.
  Per cercare la controparte si può aprire UNA fonte in più oltre alle 3 previste.
  La controparte deve riguardare quel caso specifico, con nome e ruolo, e argomenti verificabili:
  niente scetticismo generico ("gli UFO non esistono"), niente posizioni inventate o ricostruite.
  Se una controparte così non si trova, o non regge, la notizia esce in formato normale: meglio una
  notizia normale che un 1vs1 forzato.
- Il "Perché conta" spiega l'importanza della notizia per il dibattito pubblico o scientifico,
  senza riferimenti alle PMI.

## Procedura

1. Leggere `../EDITORIAL.md` e questo file.
2. Cercare notizie delle ultime 48 ore (anche in inglese; in cinese quando utile), leggere le fonti.
3. Scrivere `ufo/edition.json` con data di oggi nel fuso Europe/Rome, copia identica in
   `ufo/archive/AAAA-MM-GG.json`, voce `{"date","label","n"}` in fondo a `ufo/archive/index.json`
   (senza duplicati).
4. Eseguire `python3 scripts/share.py ufo/edition.json ufo` (se manca Pillow:
   `pip install --break-system-packages pillow`); se fallisce, proseguire.
5. Validare il JSON, commit "Edizione UFO AAAA-MM-GG" su `main` e push (in caso di conflitto:
   `git pull --rebase` e nuovo push). Toccare SOLO file dentro `ufo/`.
6. Non modificare `ufo/index.html`, i file della radice né le regole.
