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

    # --- PROGRAM TV JOJ (Podľa tvojho obrázka) ---
    epg_data = [
        {"time": "12:15", "title": "James Bond: Casino Royale", "dur": 190},
        {"time": "15:25", "title": "Hviezdy nad hlavou 9", "dur": 80},
        {"time": "16:45", "title": "Na chalupe", "dur": 65},
        {"time": "17:50", "title": "Nové bývanie", "dur": 70},
        {"time": "19:00", "title": "Krimi", "dur": 30},
        {"time": "19:30", "title": "Noviny TV JOJ", "dur": 45},
        {"time": "20:40", "title": "Sanitka", "dur": 120}
    ]

    # --- MENU ---
    if not params:
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE[/B]")
        xbmcplugin.addDirectoryItem(handle, build_url({'mode': 'list_live'}), li_live, True)
        
        li_arch = xbmcgui.ListItem(label="[B]📂 ARCHÍV TV JOJ[/B]")
        xbmcplugin.addDirectoryItem(handle, build_url({'mode': 'archive_days'}), li_arch, True)
        xbmcplugin.endOfDirectory(handle)

    # --- ŽIVÉ VYSIELANIE ---
    elif params.get('mode') == 'list_live':
        # Zistíme, čo práve beží na JOJke pre EPG
        current_joj = "Sledujte TV JOJ"
        for item in epg_data:
            start = datetime.strptime(item["time"], "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if now >= start:
                current_joj = item["title"]

        channels = [
            {"name": "TV JOJ", "url": "joj-1080.m3u8", "logo": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "epg": current_joj},
            {"name": "JOJ Plus", "url": "plus-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100063553059682"},
            {"name": "JOJ Krimi", "url": "wau-1080.m3u8", "logo": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg"},
            {"name": "JOJ Šport", "url": "joj_sport-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738"},
            {"name": "JOJ 24", "url": "joj_news-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437"},
            {"name": "Jojko", "url": "jojko-1080.m3u8", "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj"},
            {"name": "JOJ Cinema", "url": "cinema-1080.m3u8", "logo": "http://googleusercontent.com/profile/picture/2"},
            {"name": "JOJ Family", "url": "family-1080.m3u8", "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BDUQMIAK/873-joj-family-hd.png"},
            {"name": "CS History", "url": "cs_history-1080.m3u8", "logo": "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836"},
            {"name": "CS Film", "url": "cs_film-1080.m3u8", "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png"},
            {"name": "CS Mystery", "url": "cs_mystery-1080.m3u8", "logo": "https://img.joj.sk/90e3d390-9f4f-48cb-9773-98a0a119dfa8"},
            {"name": "Senzi TV", "url": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers, "logo": "http://googleusercontent.com/profile/picture/3", "is_full": True}
        ]

        for ch in channels:
            link = ch["url"] if ch.get("is_full") else "https://live.cdn.joj.sk/live/andromeda/" + ch["url"] + joj_headers
            label = f"{ch['name']} | [COLOR yellow]{ch.get('epg', '')}[/COLOR]" if ch.get('epg') else ch["name"]
            
            li = xbmcgui.ListItem(label=label)
            li.setArt({'thumb': ch["logo"], 'icon': ch["logo"]})
            li.setInfo('video', {'title': ch["name"]})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, link, li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- ARCHÍV DNI ---
    elif params.get('mode') == 'archive_days':
        for i in range(7):
            day = now - timedelta(days=i)
            d_str = day.strftime('%d.%m.%Y')
            li = xbmcgui.ListItem(label=d_str)
            xbmcplugin.addDirectoryItem(handle, build_url({'mode': 'archive_list', 'offset': str(i)}), li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- ARCHÍV RELÁCIE (Oprava prehrávania od začiatku) ---
    elif params.get('mode') == 'archive_list':
        offset = int(params.get('offset'))
        target_day = now - timedelta(days=offset)
        
        for r in epg_data:
            start_time = datetime.strptime(r["time"], "%H:%M").replace(year=target_day.year, month=target_day.month, day=target_day.day)
            
            # Ukážeme len tie, čo už skončili
            if now > (start_time + timedelta(minutes=r["dur"])):
                ts = int(start_time.timestamp())
                # Start parameter zabezpečí, že relácia ide od začiatku
                arch_link = f"https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8?start={ts}" + joj_headers
                
                li = xbmcgui.ListItem(label=f"{r['time']} - {r['title']}")
                li.setArt({'thumb': "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"})
                li.setInfo('video', {'title': r['title'], 'plot': "Prehrávanie z archívu"})
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle, arch_link, li, False)
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
