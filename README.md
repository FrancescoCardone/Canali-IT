# Custom Italy IPTV Playlist Generator

Uno script leggero per filtrare la playlist M3U8 italiana di [Free-TV/IPTV](https://github.com/Free-TV/IPTV) ed estrarre solo i canali di proprio interesse.

L'obiettivo è consentire a chiunque, tramite un semplice **fork** del repository, di mantenere la propria lista personalizzata e sempre accessibile via URL raw.

---

## 🚀 Caratteristiche

- **Sorgente aggiornata**: legge direttamente dalla playlist ufficiale `playlist_italy.m3u8`.
- **Filtro su misura**: include solo le voci elencate nel file locale `channels.txt`.
- **Output standard**: genera un file `custom_italy.m3u8` compatibile con i principali player (VLC, Kodi, TiviMate, ecc.).
- **Fork-ready**: personalizzabile direttamente dal browser o integrabile con GitHub Actions per aggiornamenti automatici.

---

## 📁 Struttura dei File

- `channels.txt`: contiene l'elenco dei nomi esatti dei canali da includere (uno per riga).
- `custom_italy.m3u8`: la playlist generata contenente solo i canali selezionati.

---

## 🛠️ Come Usarlo

### 1. Fai il Fork
Clicca sul pulsante **Fork** in alto a destra per creare una copia personale del repository nel tuo account GitHub.

### 2. Modifica la lista dei canali
Apri il file `channels.txt` e inserisci i canali desiderati (uno per riga), rispettando i nomi presenti nella sorgente upstream:

```text
Rai 1
Rai 2
Rai 3
Rete 4
Canale 5
Italia 1
LA7
