import urllib.request
import re
import os

SOURCE_URL = "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_italy.m3u8"
CHANNELS_FILE = "channels.txt"
OUTPUT_FILE = "custom_italy.m3u8"

# 1. Carica i canali richiesti preservando la grafia originale per i log
requested_channels = []
with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        clean = line.strip()
        if clean and not clean.startswith("#"):
            requested_channels.append(clean)

# Mappa per il confronto normalizzato (chiave minuscola -> nome originale)
allowed_map = {ch.lower(): ch for ch in requested_channels}

# 2. Scarica la playlist sorgente
req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as response:
    content = response.read().decode("utf-8")

lines = content.splitlines()

# 3. Filtra le tracce e traccia i canali trovati
output_lines = ["#EXTM3U"]
matched_channels = set()
include_next_url = False

for line in lines:
    line_clean = line.strip()
    if not line_clean:
        continue
    
    if line_clean.startswith("#EXTINF"):
        # Estrai nome visualizzato dopo l'ultima virgola
        display_name = line_clean.split(",")[-1].strip().lower() if "," in line_clean else None
        
        # Estrai tvg-name come fallback
        tvg_match = re.search(r'tvg-name="([^"]+)"', line_clean, re.IGNORECASE)
        tvg_name = tvg_match.group(1).strip().lower() if tvg_match else None
        
        matched_key = None
        if display_name and display_name in allowed_map:
            matched_key = display_name
        elif tvg_name and tvg_name in allowed_map and (not display_name or display_name == tvg_name):
            matched_key = tvg_name

        if matched_key:
            matched_channels.add(allowed_map[matched_key])
            include_next_url = True
            output_lines.append(line_clean)
        else:
            include_next_url = False
            
    elif line_clean.startswith("#") and include_next_url:
        output_lines.append(line_clean)
        
    elif not line_clean.startswith("#") and include_next_url:
        output_lines.append(line_clean)
        include_next_url = False

# 4. Scrivi il nuovo file M3U8
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines) + "\n")

# 5. Calcola i canali mancanti
missing_channels = [ch for ch in requested_channels if ch not in matched_channels]

# Stampa nei log della console
print("========================================")
print(f"Canali richiesti: {len(requested_channels)}")
print(f"Canali trovati:   {len(matched_channels)}")
print(f"Canali mancanti:  {len(missing_channels)}")
print("========================================")

if missing_channels:
    print("\n[ATTENZIONE] Canali non trovati nella sorgente:")
    for ch in missing_channels:
        print(f" - {ch}")
        # Notifica visiva nell'interfaccia Actions
        print(f"::warning::Canale non trovato nella sorgente IPTV: {ch}")
else:
    print("\nTutti i canali richiesti sono stati trovati con successo!")

# 6. Scrivi il riepilogo nel GitHub Step Summary (se eseguito su Actions)
summary_file = os.getenv("GITHUB_STEP_SUMMARY")
if summary_file:
    with open(summary_file, "a", encoding="utf-8") as sf:
        sf.write("### 📺 Riepilogo Aggiornamento Playlist\n\n")
        sf.write(f"- **Canali richiesti:** {len(requested_channels)}\n")
        sf.write(f"- **Canali inseriti con successo:** {len(matched_channels)}\n")
        sf.write(f"- **Canali non trovati:** {len(missing_channels)}\n\n")
        
        if missing_channels:
            sf.write("#### ⚠️ Canali mancanti / non trovati:\n")
            for ch in missing_channels:
                sf.write(f"- `{ch}`\n")
            sf.write("\n> *Suggerimento: controlla se il nome o simbolo è cambiato nella playlist sorgente.*\n")
        else:
            sf.write("✅ **Tutti i canali di `channels.txt` sono stati agganciati correttamente.**\n")
