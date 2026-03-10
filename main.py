import xbmcgui
import xbmc
import urllib.request
import time

def run_wifi_speedtest():
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Speed Test', 'Pripravujem test...')
    
    # Použijeme iný, veľmi stabilný testovací súbor (10MB)
    test_url = "https://speed.hetzner.de/10MB.bin"
    
    # Nastavenie hlavičiek, aby server neodmietol spojenie
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        start_time = time.time()
        
        # Vytvorenie požiadavky s hlavičkami
        req = urllib.request.Request(test_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        
        chunk_size = 1024 * 256 # 256KB bloky
        downloaded = 0
        total_size = 10485760 # 10MB
        
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            downloaded += len(chunk)
            
            percent = int((downloaded / total_size) * 100)
            if percent > 100: percent = 100
            
            pDialog.update(percent, 'Testujem rýchlosť tvojej Wi-Fi...', 
                           'Stiahnuté: {} MB / 10 MB'.format(downloaded // 1048576))
            
            if pDialog.iscanceled():
                return

        end_time = time.time()
        pDialog.close()
        
        duration = end_time - start_time
        # Výpočet: (80 megabitov / čas v sekundách)
        speed_mbps = round((80 / duration), 2)
        
        xbmcgui.Dialog().ok('Výsledok testu', 
                            'Tvoja Wi-Fi rýchlosť: [B]{} Mbps[/B]'.format(speed_mbps))
                            
    except Exception as e:
        if pDialog: pDialog.close()
        # Vypíše presnú chybu, aby sme vedeli, čo opraviť
        xbmcgui.Dialog().ok('Chyba testu', 'Nastal problém: {}'.format(str(e)))

if __name__ == '__main__':
    run_wifi_speedtest()


