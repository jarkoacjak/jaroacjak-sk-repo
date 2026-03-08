import sys
import urllib.parse
import xbmcgui
import xbmcplugin

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    try:
        handle = int(sys.argv[1])
        arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
        params = dict(urllib.parse.parse_qsl(arg_string))
    except:
        return

    # Spoločné hlavičky
    joj_headers = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://videoportal.joj.sk/"
    common_headers = "|User-Agent=Mozilla/5.0"

    # --- 1. HLAVNÉ MENU ---
    if not params:
        url_live = build_url({'mode': 'select_country_live'})
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE (s EPG)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        url_archive = build_url({'mode': 'list_archive_channels'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV (Pripravuje sa)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_archive, li_archive, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. VÝBER KRAJINY PRE ŽIVÉ TV ---
    elif params.get('mode') == 'select_country_live':
        url_sk = build_url({'mode': 'list_live_sk'})
        li_sk = xbmcgui.ListItem(label="[B]🇸🇰 SLOVENSKÉ TELEVÍZIE[/B]")
        li_sk.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Flag_of_Slovakia.svg/200px-Flag_of_Slovakia.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_sk, li_sk, True)

        url_cz = build_url({'mode': 'msg_archive'}) 
        li_cz = xbmcgui.ListItem(label="[B]🇨🇿 ČESKÉ TELEVÍZIE[/B]")
        li_cz.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/200px-Flag_of_the_Czech_Republic.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_cz, li_cz, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 3. ŽIVÉ TV S PRÍPRAVOU PRE EPG ---
    elif params.get('mode') == 'list_live_sk':
        tv_stanice = [
            {"nazov": "TV JOJ", "url": "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + joj_headers, "logo": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "epg_id": "JOJ.sk"},
            {"nazov": "JOJ Plus", "url": "https://live.cdn.joj.sk/live/andromeda/plus-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100063553059682", "epg_id": "PLUS.sk"},
            {"nazov": "JOJ Krimi", "url": "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8" + joj_headers, "logo": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg", "epg_id": "WAU.sk"},
            {"nazov": "JOJ Šport", "url": "https://live.cdn.joj.sk/live/andromeda/joj_sport-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738", "epg_id": "JOJSPORT.sk"},
            {"nazov": "JOJ 24", "url": "https://live.cdn.joj.sk/live/andromeda/joj_news-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437", "epg_id": "JOJ24.sk"},
            {"nazov": "Jojko", "url": "https://live.cdn.joj.sk/live/andromeda/jojko-1080.m3u8" + joj_headers, "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj", "epg_id": "JOJKO.sk"},
            {"nazov": "JOJ Cinema", "url": "https://live.cdn.joj.sk/live/andromeda/cinema-1080.m3u8" + joj_headers, "logo": "http://googleusercontent.com/profile/picture/2", "epg_id": "JOJCINEMA.sk"},
            {"nazov": "JOJ Family", "url": "https://live.cdn.joj.sk/live/andromeda/family-1080.m3u8" + joj_headers, "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BDUQMIAK/873-joj-family-hd.png", "epg_id": "JOJFAMILY.sk"},
            {"nazov": "CS History", "url": "https://live.cdn.joj.sk/live/andromeda/cs_history-1080.m3u8" + joj_headers, "logo": "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836", "epg_id": "CSHISTORY.sk"},
            {"nazov": "CS Film", "url": "https://live.cdn.joj.sk/live/andromeda/cs_film-1080.m3u8" + joj_headers, "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png", "epg_id": "CSFILM.sk"},
            {"nazov": "CS Mystery", "url": "https://live.cdn.joj.sk/live/andromeda/cs_mystery-1080.m3u8" + joj_headers, "logo": "https://img.joj.sk/90e3d390-9f4f-48cb-9773-98a0a119dfa8", "epg_id": "CSMYSTERY.sk"},
            {"nazov": "Senzi TV", "url": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers, "logo": "http://googleusercontent.com/profile/picture/3", "epg_id": "SENZI.sk"}
        ]
        
        for tv in tv_stanice:
            li = xbmcgui.ListItem(label=tv["nazov"])
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"]})
            # Nastavenie EPG ID pre PVR klientov
            li.setInfo('video', {'title': tv["nazov"], 'plot': 'Načítavam program...'})
            li.setProperty('epg_id', tv["epg_id"])
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
            
        xbmcplugin.endOfDirectory(handle)

    # --- 4. ZOZNAM STANÍC PRE ARCHÍV (PRÍPRAVA) ---
    elif params.get('mode') == 'list_archive_channels':
        # Tu budeme postupne pridávať logiku pre získavanie dní a relácií
        xbmcgui.Dialog().notification("Archív", "Pracujeme na sprístupnení relácií", xbmcgui.NOTIFICATION_INFO, 5000)
        
        # Zatiaľ zobrazíme zoznam staníc, ktoré budú mať archív ako prvé
        channels = ["TV JOJ", "JOJ Plus", "JOJ Krimi"]
        for chan in channels:
            url = build_url({'mode': 'archive_days', 'channel': chan})
            li = xbmcgui.ListItem(label=f"Archív {chan}")
            xbmcplugin.addDirectoryItem(handle, url, li, True)
            
        xbmcplugin.endOfDirectory(handle)

    elif params.get('mode') == 'msg_archive':
        xbmcgui.Dialog().ok("Informácia", "Táto sekcia sa pripravuje")
        xbmcplugin.endOfDirectory(handle, False)

if __name__ == '__main__':
    main()
    
