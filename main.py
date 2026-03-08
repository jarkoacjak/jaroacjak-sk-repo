import sys
import urllib.parse
import xbmcgui
import xbmcplugin
from datetime import datetime, timedelta

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    try:
        handle = int(sys.argv[1])
        arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
        params = dict(urllib.parse.parse_qsl(arg_string))
    except:
        return

    # HLAVIČKY (Dôležité pre funkčnosť JOJ streamov)
    joj_headers = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://videoportal.joj.sk/"
    common_headers = "|User-Agent=Mozilla/5.0"
    now = datetime.now()

    # --- 1. HLAVNÉ MENU ---
    if not params:
        url_live = build_url({'mode': 'list_live_sk'})
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        url_archive = build_url({'mode': 'archive_days'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV TV JOJ[/B]")
        xbmcplugin.addDirectoryItem(handle, url_archive, li_archive, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. ŽIVÉ VYSIELANIE (Všetky stanice musia fungovať) ---
    elif params.get('mode') == 'list_live_sk':
        tv_stanice = [
            {"nazov": "TV JOJ", "url": "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + joj_headers},
            {"nazov": "JOJ Plus", "url": "https://live.cdn.joj.sk/live/andromeda/plus-1080.m3u8" + joj_headers},
            {"nazov": "JOJ Krimi", "url": "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8" + joj_headers},
            {"nazov": "JOJ Šport", "url": "https://live.cdn.joj.sk/live/andromeda/joj_sport-1080.m3u8" + joj_headers},
            {"nazov": "JOJ 24", "url": "https://live.cdn.joj.sk/live/andromeda/joj_news-1080.m3u8" + joj_headers},
            {"nazov": "Jojko", "url": "https://live.cdn.joj.sk/live/andromeda/jojko-1080.m3u8" + joj_headers},
            {"nazov": "JOJ Cinema", "url": "https://live.cdn.joj.sk/live/andromeda/cinema-1080.m3u8" + joj_headers},
            {"nazov": "JOJ Family", "url": "https://live.cdn.joj.sk/live/andromeda/family-1080.m3u8" + joj_headers},
            {"nazov": "Senzi TV", "url": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers}
        ]
        
        for tv in tv_stanice:
            li = xbmcgui.ListItem(label=tv["nazov"])
            li.setInfo('video', {'title': tv["nazov"]})
            li.setProperty('IsPlayable', 'true')
            # Pridáme k odkazu informáciu, že ide o živé vysielanie
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
            
        xbmcplugin.endOfDirectory(handle)

    # --- 3. ARCHÍV - VÝBER DŇA ---
    elif params.get('mode') == 'archive_days':
        for i in range(7):
            date_obj = now - timedelta(days=i)
            date_str = date_obj.strftime('%d.%m.%Y')
            label = f"Dnes ({date_str})" if i == 0 else date_str
            
            url = build_url({'mode': 'archive_list', 'date': date_str, 'day_offset': str(i)})
            li = xbmcgui.ListItem(label=label)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 4. ARCHÍV - ČO BOLO V TV (Prehrávanie minulosti) ---
    elif params.get('mode') == 'archive_list':
        day_offset = int(params.get('day_offset'))
        target_date = now - timedelta(days=day_offset)

        # Program (To čo bolo v TV)
        program = [
            {"time": "08:00", "title": "Ranné noviny", "dur": 120},
            {"time": "12:15", "title": "James Bond: Casino Royale", "dur": 150},
            {"time": "15:25", "title": "Hviezdy nad hlavou", "dur": 60},
            {"time": "19:00", "title": "Krimi", "dur": 30},
            {"time": "19:30", "title": "Noviny TV JOJ", "dur": 45}
        ]

        for r in program:
            # Vypočítame čas začiatku relácie
            start_dt = datetime.strptime(r["time"], "%H:%M").replace(
                year=target_date.year, month=target_date.month, day=target_date.day)
            
            # Zobrazíme iba tie, ktoré už skončili
            if now > (start_dt + timedelta(minutes=r["dur"])):
                start_ts = int(start_dt.timestamp())
                # ARCHÍVNY LINK: Používame parameter ?start= pre posun v čase
                archive_url = f"https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8?start={start_ts}" + joj_headers
                
                li = xbmcgui.ListItem(label=f"{r['time']} - {r['title']}")
                li.setInfo('video', {'title': r['title'], 'plot': "Prehrávanie z archívu"})
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle, archive_url, li, False)
            
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
