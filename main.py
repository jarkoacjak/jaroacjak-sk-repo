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

    # Hlavičky pre stabilitu streamov
    joj_headers = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://videoportal.joj.sk/"
    common_headers = "|User-Agent=Mozilla/5.0"

    # --- 1. HLAVNÉ MENU ---
    if not params:
        url_live = build_url({'mode': 'list_live_sk'})
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE (s EPG)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        url_archive = build_url({'mode': 'list_archive_sk'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV (TV JOJ)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_archive, li_archive, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. ŽIVÉ VYSIELANIE S EPG PROGRAMOM ---
    elif params.get('mode') == 'list_live_sk':
        tv_stanice = [
            {"nazov": "TV JOJ", "url": "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + joj_headers, "logo": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "epg": "12:15 James Bond: Casino Royale\n15:25 Hviezdy nad hlavou"},
            {"nazov": "JOJ Plus", "url": "https://live.cdn.joj.sk/live/andromeda/plus-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100063553059682", "epg": "Program sa načítava..."},
            {"nazov": "JOJ Krimi", "url": "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8" + joj_headers, "logo": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg", "epg": "Program sa načítava..."},
            {"nazov": "JOJ Šport", "url": "https://live.cdn.joj.sk/live/andromeda/joj_sport-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738", "epg": "Program sa načítava..."},
            {"nazov": "JOJ 24", "url": "https://live.cdn.joj.sk/live/andromeda/joj_news-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437", "epg": "Program sa načítava..."},
            {"nazov": "Jojko", "url": "https://live.cdn.joj.sk/live/andromeda/jojko-1080.m3u8" + joj_headers, "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj", "epg": "Program sa načítava..."},
            {"nazov": "JOJ Cinema", "url": "https://live.cdn.joj.sk/live/andromeda/cinema-1080.m3u8" + joj_headers, "logo": "http://googleusercontent.com/profile/picture/2", "epg": "Program sa načítava..."},
            {"nazov": "JOJ Family", "url": "https://live.cdn.joj.sk/live/andromeda/family-1080.m3u8" + joj_headers, "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BDUQMIAK/873-joj-family-hd.png", "epg": "Program sa načítava..."},
            {"nazov": "CS History", "url": "https://live.cdn.joj.sk/live/andromeda/cs_history-1080.m3u8" + joj_headers, "logo": "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836", "epg": "Program sa načítava..."},
            {"nazov": "CS Film", "url": "https://live.cdn.joj.sk/live/andromeda/cs_film-1080.m3u8" + joj_headers, "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png", "epg": "Program sa načítava..."},
            {"nazov": "CS Mystery", "url": "https://live.cdn.joj.sk/live/andromeda/cs_mystery-1080.m3u8" + joj_headers, "logo": "https://img.joj.sk/90e3d390-9f4f-48cb-9773-98a0a119dfa8", "epg": "Program sa načítava..."},
            {"nazov": "Senzi TV", "url": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers, "logo": "http://googleusercontent.com/profile/picture/3", "epg": "Hudobný program"}
        ]
        
        for tv in tv_stanice:
            li = xbmcgui.ListItem(label=tv["nazov"])
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"]})
            # Pridanie programu do popisu (Plot)
            li.setInfo('video', {'title': tv["nazov"], 'plot': tv["epg"]})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
            
        xbmcplugin.endOfDirectory(handle)

    # --- 3. ARCHÍV - VÝBER DŇA ---
    elif params.get('mode') == 'list_archive_sk':
        for i in range(7):
            date_obj = datetime.now() - timedelta(days=i)
            date_str = date_obj.strftime('%d.%m.%Y')
            label = f"{date_str}"
            if i == 0: label = f"Dnes ({date_str})"
            
            url = build_url({'mode': 'archive_programs', 'date': date_str})
            li = xbmcgui.ListItem(label=label)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 4. ARCHÍV - ZOZNAM RELÁCIÍ (Podľa tvojho obrázka) ---
    elif params.get('mode') == 'archive_programs':
        date = params.get('date')
        relacie = [
            {"time": "12:15", "title": "James Bond: Casino Royale"},
            {"time": "15:25", "title": "Hviezdy nad hlavou 9"},
            {"time": "16:45", "title": "Na chalupe"},
            {"time": "19:00", "title": "Krimi"},
            {"time": "19:30", "title": "Noviny TV JOJ"}
        ]
        
        for r in relacie:
            label = f"{r['time']} - {r['title']}"
            li = xbmcgui.ListItem(label=label)
            # Tu sa neskôr pridá URL adresa pre konkrétne video z archívu
            xbmcplugin.addDirectoryItem(handle, "", li, False)
            
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
