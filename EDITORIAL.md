# News.Raimondo.it — regole editoriali e istruzioni per l'edizione automatica

Questo file è la fonte di verità per chi prepara l'edizione del mattino (persona o agente AI).
Il sito legge un solo file: `edition.json`. Ogni mattina va riscritto per intero.

## Pubblico e posizionamento

Lettori: imprenditori e manager di PMI italiane B2B (manifattura, industria, 500K–5M€ di fatturato),
interessati a pubblicità digitale, intelligenza artificiale e industria.
Curatore: Federico Raimondo (raimondo.it), consulente di marketing e AI per PMI industriali.
Tono: italiano chiaro, professionale ma accessibile. Niente sensazionalismo.

## Sezioni pubbliche (id → nome)

- `ads` → Pubblicità e AI (Google Ads, Meta, ChatGPT Ads, AI Mode, misurazione)
- `ia` → Intelligenza artificiale (modelli, aziende, sicurezza, adozione nelle imprese)
- `regole` → Regole sull'AI (AI Act, norme italiane, autorità, sanzioni)
- `ind` → Industria e robotica (congiuntura manifatturiera, robotica, automazione)
- `lavoro` → Lavoro e formazione (competenze, lavoratori senior e AI, fondi interprofessionali, bandi)
- `succ` → Passaggio generazionale (successione d'impresa, PMI senza successore)

Le sezioni private (Politica, Formula 1, UAP, Astronomia e spazio, Rimini e Romagna) NON vanno mai
in questo repository: sono pubblico. Vivono solo nella pagina privata su claude.ai (vedi in fondo).

## Regole (decise con Federico il 26/11/2026)

1. **Freschezza.** Solo notizie pubblicate nelle ultime 48 ore. Se una sezione non ne ha, quel giorno
   non compare. Meglio un'edizione corta che una notizia vecchia.
2. **Verifica.** Leggere SEMPRE l'articolo intero (WebFetch) prima di riassumerlo, mai solo gli estratti
   di ricerca. Una sola fonte basta solo se è primaria (comunicato ufficiale, documento dell'ente,
   blog dell'azienda, atto ufficiale). Altrimenti servono due fonti indipendenti.
   Nessun numero, data o citazione che non sia nelle fonti lette.
3. **Fonti, gerarchia a livelli.**
   - Livello 1, primarie: Google Ads/Search Central blog e help, Microsoft Advertising, Meta for Business,
     blog ufficiali dei laboratori AI, atti giudiziari, Gazzetta Ufficiale/Normattiva, Commissione UE,
     AgID, ACN, Garante privacy, Istat, Banca d'Italia, S&P Global PMI, Confindustria, CNA, Unioncamere,
     Ministero del Lavoro, MIMIT, siti dei fondi interprofessionali, IFR.
   - Livello 2, testate generaliste: ANSA, Il Sole 24 Ore, Corriere della Sera, Il Post, Avvenire,
     Milano Finanza, Reuters, AP, Bloomberg, Financial Times, BBC, NPR, The Verge, MIT Technology Review,
     Ars Technica, Caixin, South China Morning Post.
   - Livello 3, specializzate (sempre insieme a un'altra fonte): Search Engine Land, Search Engine
     Roundtable, Search Engine Journal, Agenda Digitale, Key4biz, IEEE Spectrum, The Robot Report,
     PMI.it, IPSOA, Edotto.
   - Solo spunto, mai citati come fonte: newsletter, aggregatori, blog personali, LinkedIn, canali
     YouTube che non sono di testate o aziende.
   - Esclusi: siti senza autore o data, siti che riscrivono notizie altrui.
   - Media statali cinesi (Xinhua, China Securities Journal…): lingua "GOV" = etichetta "fonte governativa".
4. **Quantità.** Al massimo 2 notizie per sezione e 10 in tutto, 1vs1 compresi.
5. **Lingue.** Per AI, robotica e temi tecnici usare anche fonti in inglese e cinese; scrivere sempre
   in italiano. Indicare la lingua della fonte: "EN", "ZH", "GOV" (governativa), "" per italiano.
6. **1vs1.** Ogni notizia divisiva (politica, regolazione contesa, cause legali, scontri tra aziende…)
   esce in formato 1vs1: fatti neutri + le due tesi più nette, ciascuna ATTRIBUITA a chi la sostiene,
   con 2-4 punti per lato, senza inventare posizioni né citazioni. Il giornale non prende posizione.
   Vanno nella fascia "Il confronto del giorno" in cima.
7. **Immagini.** Nessuna foto. Copertina tipografica (numero o parola chiave + riga di spiegazione),
   oppure uno schema semplice se la notizia ha 2-3 numeri confrontabili o una sequenza chiara.
8. **Video.** Facoltativi, solo da canali di testate o aziende ufficiali.
9. **Perché conta.** 1-2 frasi per il lettore imprenditore: cosa cambia per lui. Mai riferimenti
   personali al curatore o ai suoi clienti.
10. **Diritti.** Riassumere con parole proprie, mai copiare frasi delle fonti (al massimo una breve
    citazione tra virgolette per articolo, sotto le 15 parole).

## Formato di edition.json

```json
{
  "date": "2026-11-27",
  "label": "Venerdì 27 novembre 2026",
  "lead": "id-della-notizia-di-apertura",
  "secs": [["ads","Pubblicità e AI"],["ia","Intelligenza artificiale"],["regole","Regole sull'AI"],
           ["ind","Industria e robotica"],["lavoro","Lavoro e formazione"],["succ","Passaggio generazionale"]],
  "stories": [
    {
      "id": "slug-minuscolo-con-trattini",
      "sec": "ads",
      "kick": "Google Ads",
      "date": "26 novembre",
      "title": "Titolo informativo, non sensazionalistico",
      "sum": "Riassunto di 2-4 frasi con i fatti verificati.",
      "why": "Perché conta per un imprenditore, 1-2 frasi.",
      "src": [["Nome testata", "https://...", "EN"]],
      "yt": [["Titolo video", "https://www.youtube.com/watch?v=..."]],
      "cover": {"t": "num", "big": "4", "small": "annunci dentro una sola risposta AI"}
    }
  ]
}
```

Copertine ammesse:
- `{"t":"num","big":"33","small":"anni alla guida di Nvidia"}` — `big` cortissimo (max 7 caratteri).
- `{"t":"bars","rows":[["Etichetta",40,"oltre 40.000",0],["Etichetta",100,"oltre 100.000",1]],"caption":"...","min":0,"max":100,"mark":50}`
  — l'ultimo valore 1 evidenzia la barra; `min`, `max`, `mark` facoltativi.
- `{"t":"dots","n":10,"on":5,"caption":"..."}`
- `{"t":"flow","steps":["A","B","C"],"hi":[2],"caption":"..."}`

Per un 1vs1 aggiungere: `"vs": true`, `"facts": ["fatto neutro", ...]`,
`"a": {"h":"Sì: ...","who":"La tesi di ...","pts":["...","..."]}`, `"b": {...}`.
La notizia di apertura (`lead`) non può essere un 1vs1.

Regole tecniche: `id` solo lettere minuscole, cifre e trattini (max 40); tutti i link `https://`;
JSON valido (verificarlo con `python3 -m json.tool edition.json` prima del commit).

## Procedura del mattino

1. Cercare le notizie delle ultime 48 ore per ogni sezione (WebSearch, anche in inglese e cinese).
2. Aprire e leggere per intero le fonti candidate (WebFetch). Scartare ciò che non passa le regole.
3. Scegliere al massimo 2 per sezione e 10 in tutto; scegliere l'apertura (la più rilevante non divisiva).
4. Scrivere `edition.json`, salvare la precedente in `archive/AAAA-MM-GG.json`.
5. Validare il JSON, fare commit su `main` con messaggio "Edizione AAAA-MM-GG" e push.
6. Sezioni private: se lo strumento claude-artifacts `db_write` è disponibile, aggiornare il documento
   `private/edition` dell'artifact `875cc5e6-43d8-45cc-9048-20f51d1e2bc2` con lo stesso formato
   (`secs` private + `stories`, al massimo 1 notizia per sezione privata, stesse regole). Altrimenti saltare.
