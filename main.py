import xbmcgui
import xbmc
import urllib.request
import time

def run_wifi_speedtest():
    # Vytvorenie okna pre priebeh testu
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Speed Test', 'Pripravujem test tvojej Wi-Fi...')
    
    # Adresa pre testovací súbor (10MB)
    test_url = "https://speed.hetzner.de/10MB.bin"
    
    try:
        start_time = time.time()
        
        # Otvorenie spojenia so serverom
        response = urllib.request.urlopen(test_url)
        chunk_size = 1024 * 512  # 512KB bloky pre plynulosť
        downloaded = 0
        total_size = 10485760  # 10MB
        
        # Samotné sťahovanie dát
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            downloaded += len(chunk)
            
            # Výpočet percent pre lištu v Kodi
            percent = int((downloaded / total_size) * 100)
            pDialog.update(percent, 'Testujem rýchlosť tvojej Wi-Fi...', 
                           'Sťahujem 10 MB dát...')
            
            # Ak používateľ klikne na "Zrušiť"
            if pDialog.iscanceled():
                return

        end_time = time.time()
        pDialog.close()
        
        # Výpočet výsledku
        duration = end_time - start_time
        # Prevod na Megabity za sekundu (Mbps)
        speed_mbps = round((80 / duration), 2)
        
        # Zobrazenie konečného výsledku
        xbmcgui.Dialog().ok('Výsledok testu', 
                            'Tvoja Wi-Fi rýchlosť: [B]{} Mbps[/B]\n'
                            'Čas sťahovania: {} sekúnd'.format(speed_mbps, round(duration, 2)))
                            
    except Exception as e:
        pDialog.close()
        xbmcgui.Dialog().ok('Chyba', 'Nepodarilo sa vykonať test: {}'.format(str(e)))

if __name__ == '__main__':
    run_wifi_speedtest()
    
