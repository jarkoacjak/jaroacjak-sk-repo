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

    # --- PROGRAM TV JOJ (Presne podľa tvojho obrázka) ---
    epg_joj = [
        {"time": "12:15", "title": "James Bond: Casino Royale", "dur": 190},
        {"time": "15:25", "title": "Hviezdy nad hlavou 9", "dur": 80},
        {"time": "16:45", "title": "Na chalupe", "dur": 65},
        {"time": "17:50", "title": "Nové bývanie", "dur": 70},
        {"time": "19:00", "title": "Krimi", "dur": 30},
        {"time": "19:30", "title": "Noviny TV JOJ", "dur": 45},
        {"time": "20:15", "title": "Informácie pre tipujúcich", "dur": 5},
        {"time": "20:20", "title": "Šport", "dur": 10},
        {"time": "20:30", "title": "Najlepšie počasie", "dur": 10},
        {"time": "20:40", "title": "Sanitka", "dur": 120},
        {"time": "23:40", "title": "Pravidlá zabíjania", "dur": 100}
    ]

    if not params:
        # HLAVNÉ MENU
        xbmcplugin.addDirectoryItem(handle, build_url({'mode': 'list_live'}), xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE[/B]"), True)
        xbmcplugin.addDirectoryItem(handle, build_url({'mode': 'archive_days'}), xbmcgui.ListItem(label="[B]📂 ARCHÍV TV JOJ[/B]"), True)
        xbmcplugin.endOfDirectory(handle)

    elif params.get('mode') == 'list_live':
        # ŽIVÉ VYSIELANIE (EPG iba pre TV JOJ)
        current_show = ""
        for item in epg_joj:
            start = datetime.strptime(item["time"], "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if now >= start:
                current_show = item["title"]

        stanice = [
            {"n": "TV JOJ", "u": "joj-1080.m3u8", "l": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "e": current_show},
            {"n": "JOJ Plus", "u": "plus-1080.m3u8", "l": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100063553059682"},
            {"n": "JOJ Krimi", "u": "wau-1080.m3u8", "l": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg"},
            {"n": "JOJ Šport", "u": "joj_sport-1080.m3u8", "l": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738"},
            {"n": "JOJ 24", "u": "joj_news-1080.m3u8", "l": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437"},
            {"n": "Jojko", "u": "jojko-1080.m3u8", "l": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj"},
            {"n": "JOJ Cinema", "u": "cinema-1080.m3u8", "l": "http://googleusercontent.com/profile/picture/2"},
            {"n": "JOJ Family", "u": "family-1080.m3u8", "l": "https://staticeu.sweet.tv/images/cache/channel_icons/BDUQMIAK/873-joj-family-hd.png"},
            {"n": "CS History", "u": "cs_history-1080.m3u8", "l": "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836"},
            {"n": "CS Film", "u": "cs_film-1080.m3u8", "l": "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png"},
            {"n": "CS Mystery", "u": "cs_mystery-1080.m3u8", "l": "https://img.joj.sk/90e3d390-9f4f-48cb-9773-98a0a119dfa8"},
            {"n": "Senzi TV", "u": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers, "l": "http://googleusercontent.com/profile/picture/3", "custom": True}
        ]

        for s in stanice:
            url = s["u"] if s.get("custom") else "https://live.cdn.joj.sk/live/andromeda/" + s["u"] + joj_headers
            name = f"{s['n']} | [COLOR yellow]{s['e']}[/COLOR]" if s.get("e") else s["n"]
            li = xbmcgui.ListItem(label=name)
            li.setArt({'thumb': s["l"], 'icon': s["l"]})
            li.setInfo('video', {'title': s["n"]})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, url, li, False)
        xbmcplugin.endOfDirectory(handle)

    elif params.get('mode') == 'archive_days':
        # VÝBER DŇA - OPRAVA CHYBY
        for i in range(7):
            d = now - timedelta(days=i)
            d_str = d.strftime('%d.%m.%Y')
            label = f"Dnes ({d_str})" if i == 0 else d_str
            url = build_url({'mode': 'archive_list', 'offset': str(i)})
            li = xbmcgui.ListItem(label=label)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    elif params.get('mode') == 'archive_list':
        # ZOZNAM RELÁCIÍ V ARCHÍVE
        offset = int(params.get('offset'))
        target_date = now - timedelta(days=offset)
        
        for r in epg_joj:
            start_dt = datetime.strptime(r["time"], "%H:%M").replace(year=target_date.year, month=target_date.month, day=target_date.day)
            
            # Zobraziť iba relácie, ktoré už skončili
            if now > (start_dt + timedelta(minutes=r["dur"])):
                ts = int(start_dt.timestamp())
                # Start parameter pre archív
                url = f"https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8?start={ts}" + joj_headers
                
                li = xbmcgui.ListItem(label=f"{r['time']} - {r['title']}")
                li.setArt({'thumb': "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"})
                li.setInfo('video', {'title': r['title'], 'plot': "Prehrávanie z archívu od začiatku"})
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle, url, li, False)
        
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
