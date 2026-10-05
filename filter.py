import urllib.request
import re

SOURCE_URL = "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_italy.m3u8"
CHANNELS_FILE = "channels.txt"
OUTPUT_FILE = "custom_italy.m3u8"

# 1. Carica i canali consentiti (in minuscolo e puliti dagli spazi)
with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
    allowed_channels = {
        line.strip().lower() 
        for line in f 
        if line.strip() and not line.startswith("#")
    }

# 2. Scarica la playlist sorgente
req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as response:
    content = response.read().decode("utf-8")

lines = content.splitlines()

# 3. Filtra le tracce
output_lines = ["#EXTM3U"]
include_next_url = False

for line in lines:
    line_clean = line.strip()
    if not line_clean:
        continue
    
    if line_clean.startswith("#EXTINF"):
        # Estrai il nome visualizzato (tutto ciò che c'è dopo l'ultima virgola)
        display_name = line_clean.split(",")[-1].strip().lower() if "," in line_clean else None
        
        # Estrai tvg-name come fallback
        tvg_match = re.search(r'tvg-name="([^"]+)"', line_clean, re.IGNORECASE)
        tvg_name = tvg_match.group(1).strip().lower() if tvg_match else None
        
        # Match esatto: prima verifica il nome completo dopo la virgola, poi tvg-name
        matched = False
        if display_name and display_name in allowed_channels:
            matched = True
        elif tvg_name and tvg_name in allowed_channels and (not display_name or display_name == tvg_name):
            matched = True

        if matched:
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

print(f"Playlist generata con successo: {len(output_lines)} righe scritte.")
