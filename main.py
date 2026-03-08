import sys
import urllib.parse
import xbmcgui
import xbmcplugin
from datetime import datetime

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    try:
        handle = int(sys.argv[1])
        arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
        params = dict(urllib.parse.parse_qsl(arg_string))
    except:
        return

    # HLAVIČKY PRE STABILITU JOJ STREAMOV
    joj_headers = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://videoportal.joj.sk/"
    common_headers = "|User-Agent=Mozilla/5.0"
    now = datetime.now()

    # --- HLAVNÉ MENU (VÝBER KRAJINY) ---
    if not params:
        xbmcplugin.addDirectoryItem(handle, build_url({'mode': 'list_sk'}), xbmcgui.ListItem(label="[B]🇸🇰 SLOVENSKÉ A CS STANICE[/B]"), True)
        xbmcplugin.addDirectoryItem(handle, build_url({'mode': 'list_cz'}), xbmcgui.ListItem(label="[B]🇨🇿 ČESKÉ STANICE[/B]"), True)
        xbmcplugin.endOfDirectory(handle)

    # --- SLOVENSKÉ A CS STANICE (Všetko v jednom zozname) ---
    elif params.get('mode') == 'list_sk':
        # EPG pre JOJ (podľa tvojho obrázka)
        epg_joj = [
            {"time": "12:15", "title": "James Bond: Casino Royale"},
            {"time": "15:25", "title": "Hviezdy nad hlavou 9"},
            {"time": "16:45", "title": "Na chalupe"},
            {"time": "17:50", "title": "Nové bývanie"},
            {"time": "19:00", "title": "Krimi"},
            {"time": "19:30", "title": "Noviny TV JOJ"}
        ]
        
        current_joj = "Sledujte TV JOJ"
        for item in epg_joj:
            start = datetime.strptime(item["time"], "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if now >= start:
                current_joj = item["title"]

        vsetky_stanice = [
            {"n": "TV JOJ", "u": "joj-1080.m3u8", "l": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "e": current_joj},
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

        for s in vsetky_stanice:
            url = s["u"] if s.get("custom") else "https://live.cdn.joj.sk/live/andromeda/" + s["u"] + joj_headers
            name = f"{s['n']} | [COLOR yellow]{s.get('e', '')}[/COLOR]" if s.get('e') else s["n"]
            
            li = xbmcgui.ListItem(label=name)
            li.setArt({'thumb': s["l"], 'icon': s["l"]})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, url, li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- ČESKÉ STANICE (Ostatné) ---
    elif params.get('mode') == 'list_cz':
        cz_stanice = [
            {"n": "ČT 1", "u": "https://example.com/ct1.m3u8", "l": "https://upload.wikimedia.org/wikipedia/commons/e/ed/Ceskatelevize.svg"}
        ]
        for s in cz_stanice:
            li = xbmcgui.ListItem(label=s["n"])
            li.setArt({'thumb': s["l"]})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, s["u"], li, False)
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
