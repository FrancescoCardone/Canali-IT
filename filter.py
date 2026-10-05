import urllib.request
import re

SOURCE_URL = "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_italy.m3u8"
CHANNELS_FILE = "channels.txt"
OUTPUT_FILE = "custom_italy.m3u8"

# 1. Carica i canali consentiti
with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
    allowed_channels = [line.strip().lower() for line in f if line.strip() and not line.startswith("#")]

# 2. Scarica la playlist sorgente
req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as response:
    content = response.read().decode("utf-8")

lines = content.splitlines()

# 3. Filtra le tracce
output_lines = ["#EXTM3U"]
include_next_url = False
current_extinf = ""

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if line.startswith("#EXTINF"):
        current_extinf = line
        line_lower = line.lower()
        # Verifica se uno dei nomi canale corrisponde a tvg-name o al titolo finale
        if any(ch in line_lower for ch in allowed_channels):
            include_next_url = True
            output_lines.append(current_extinf)
        else:
            include_next_url = False
            
    elif line.startswith("#") and include_next_url:
        # Mantiene eventuali tag intermedi (#EXTVLCOPT, ecc.)
        output_lines.append(line)
        
    elif not line.startswith("#") and include_next_url:
        # Aggiunge l'URL dello stream
        output_lines.append(line)
        include_next_url = False

# 4. Scrivi il nuovo file M3U8
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines) + "\n")

print(f"Playlist generata con successo: {len(output_lines)} righe scritte.")