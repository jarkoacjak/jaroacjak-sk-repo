import xbmcgui
import xbmc
import urllib.request
import time

def run_real_speedtest():
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Speed Test', 'Pripravujem reálne meranie...')
    
    # URL adresa súboru na test (10MB testovací súbor)
    # Použijeme stabilný server
    test_url = "https://speed.hetzner.de/10MB.bin"
    
    try:
        start_time = time.time()
        
        # Otvorenie spojenia
        req = urllib.request.urlopen(test_url)
        chunk_size = 1024 * 256 # 256KB bloky
        downloaded = 0
        total_size = 10485760 # 10MB v bajtoch
        
        data = []
        
        while True:
            chunk = req.read(chunk_size)
            if not chunk:
                break
            downloaded += len(chunk)
            data.append(chunk)
            
            # Výpočet percent pre lištu
            percent = int((downloaded / total_size) * 100)
            if percent > 100: percent = 100
            
            pDialog.update(percent, 'Sťahujem testovacie dáta (10MB)...', 
                           'Rýchlosť sa počíta v reálnom čase.')
            
            if pDialog.iscanceled():
                return

        end_time = time.time()
        pDialog.close()
        
        # Výpočet rýchlosti
        duration = end_time - start_time
        # Rýchlosť v Megabitoch za sekundu (Mbps)
        # (10MB * 8 bitov) / čas
        speed_mbps = round((80 / duration), 2)
        
        xbmcgui.Dialog().ok('Výsledok merania', 
                            'Test úspešne dokončený!\n\n'
                            'Reálna rýchlosť sťahovania: {} Mbps\n'
                            'Čas sťahovania: {} s'.format(speed_mbps, round(duration, 2)))
                            
    except Exception as e:
        pDialog.close()
        xbmcgui.Dialog().ok('Chyba', 'Nepodarilo sa spojiť so serverom: {}'.format(str(e)))

if __name__ == '__main__':
    run_real_speedtest()


