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

    joj_headers = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://videoportal.joj.sk/"
    common_headers = "|User-Agent=Mozilla/5.0"
    now = datetime.now()

    # --- 1. HLAVNÉ MENU ---
    if not params:
        url_live = build_url({'mode': 'list_live_sk'})
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE (EPG)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        url_archive = build_url({'mode': 'archive_days'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV TV JOJ[/B]")
        xbmcplugin.addDirectoryItem(handle, url_archive, li_archive, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 2. ŽIVÉ VYSIELANIE (EPG PRE KAŽDÚ STANICU) ---
    elif params.get('mode') == 'list_live_sk':
        tv_stanice = [
            {"nazov": "TV JOJ", "url": "joj-1080.m3u8", "logo": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "epg": "James Bond: Casino Royale"},
            {"nazov": "JOJ Plus", "url": "plus-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100063553059682", "epg": "Profesionáli"},
            {"nazov": "JOJ Krimi", "url": "wau-1080.m3u8", "logo": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg", "epg": "CSI: Las Vegas"},
            {"nazov": "JOJ Šport", "url": "joj_sport-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738", "epg": "Hokej: Tipos Extraliga"},
            {"nazov": "JOJ 24", "url": "joj_news-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437", "epg": "Správy o 17:00"},
            {"nazov": "Jojko", "url": "jojko-1080.m3u8", "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj", "epg": "Spongebob v nohaviciach"},
            {"nazov": "JOJ Cinema", "url": "cinema-1080.m3u8", "logo": "http://googleusercontent.com/profile/picture/2", "epg": "Vlk z Wall Street"},
            {"nazov": "JOJ Family", "url": "family-1080.m3u8", "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BDUQMIAK/873-joj-family-hd.png", "epg": "Na chalupe"},
            {"nazov": "CS History", "url": "cs_history-1080.m3u8", "logo": "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836", "epg": "Druhá svetová vojna"},
            {"nazov": "CS Film", "url": "cs_film-1080.m3u8", "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png", "epg": "S tebou mě baví svět"},
            {"nazov": "CS Mystery", "url": "cs_mystery-1080.m3u8", "logo": "https://img.joj.sk/90e3d390-9f4f-48cb-9773-98a0a119dfa8", "epg": "Záhady vesmíru"},
            {"nazov": "Senzi TV", "url": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers, "logo": "http://googleusercontent.com/profile/picture/3", "epg": "Senzi hity", "is_custom": True}
        ]
        
        for tv in tv_stanice:
            full_url = tv["url"] if "is_custom" in tv else "https://live.cdn.joj.sk/live/andromeda/" + tv["url"] + joj_headers
            # Zobrazenie stanice s jej aktuálnym programom (EPG)
            label = f"{tv['nazov']} | [COLOR yellow]{tv['epg']}[/COLOR]"
            li = xbmcgui.ListItem(label=label)
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"]})
            li.setInfo('video', {'title': tv["nazov"], 'plot': f"Aktuálne: {tv['epg']}"})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, full_url, li, False)
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

    # --- 4. ARCHÍV - SKUTOČNÉ PREHRÁVANIE MINULOSTI ---
    elif params.get('mode') == 'archive_list':
        day_offset = int(params.get('day_offset'))
        target_date = now - timedelta(days=day_offset)
        joj_logo = "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"

        # Program podľa tvojho obrázka (pre TV JOJ)
        program = [
            {"time": "12:15", "title": "James Bond: Casino Royale", "dur": 150},
            {"time": "15:25", "title": "Hviezdy nad hlavou 9", "dur": 60},
            {"time": "16:45", "title": "Na chalupe", "dur": 60},
            {"time": "19:00", "title": "Krimi", "dur": 30},
            {"time": "19:30", "title": "Noviny TV JOJ", "dur": 45}
        ]

        for r in program:
            start_dt = datetime.strptime(r["time"], "%H:%M").replace(
                year=target_date.year, month=target_date.month, day=target_date.day)
            
            # Zobrazíme len to, čo už bolo odvysielané
            if now > (start_dt + timedelta(minutes=10)): # 10 minút rezerva na spracovanie
                start_ts = int(start_dt.timestamp())
                # Kľúčová zmena: Archívny link s časovým posunom (?start=)
                archive_url = f"https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8?start={start_ts}" + joj_headers
                
                li = xbmcgui.ListItem(label=f"{r['time']} - {r['title']}")
                li.setArt({'thumb': joj_logo, 'icon': joj_logo})
                li.setInfo('video', {'title': r['title'], 'plot': f"Vysielané: {r['time']}. Toto je záznam z archívu."})
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle, archive_url, li, False)
            
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
