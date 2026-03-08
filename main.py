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

    # Hlavičky pre stabilitu streamov (JOJ skupina vyžaduje Referer)
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

    # --- 2. ŽIVÉ VYSIELANIE (Oprava zobrazenia EPG) ---
    elif params.get('mode') == 'list_live_sk':
        tv_stanice = [
            {"nazov": "TV JOJ", "url": "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + joj_headers, "logo": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "epg": "Práve beží: James Bond: Casino Royale"},
            {"nazov": "JOJ Plus", "url": "https://live.cdn.joj.sk/live/andromeda/plus-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100063553059682", "epg": "Sledujte filmy a seriály na JOJ Plus"},
            {"nazov": "JOJ Krimi", "url": "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8" + joj_headers, "logo": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg", "epg": "Najlepšie kriminálne prípady"},
            {"nazov": "JOJ Šport", "url": "https://live.cdn.joj.sk/live/andromeda/joj_sport-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738", "epg": "Živé športové prenosy"},
            {"nazov": "JOJ 24", "url": "https://live.cdn.joj.sk/live/andromeda/joj_news-1080.m3u8" + joj_headers, "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437", "epg": "Spravodajstvo 24 hodín denne"},
            {"nazov": "Jojko", "url": "https://live.cdn.joj.sk/live/andromeda/jojko-1080.m3u8" + joj_headers, "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj", "epg": "Rozprávky pre najmenších"},
            {"nazov": "JOJ Cinema", "url": "https://live.cdn.joj.sk/live/andromeda/cinema-1080.m3u8" + joj_headers, "logo": "http://googleusercontent.com/profile/picture/2", "epg": "Filmové premiéry"},
            {"nazov": "JOJ Family", "url": "https://live.cdn.joj.sk/live/andromeda/family-1080.m3u8" + joj_headers, "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BDUQMIAK/873-joj-family-hd.png", "epg": "Rodinná zábava"},
            {"nazov": "CS History", "url": "https://live.cdn.joj.sk/live/andromeda/cs_history-1080.m3u8" + joj_headers, "logo": "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836", "epg": "Dokumenty z histórie"},
            {"nazov": "CS Film", "url": "https://live.cdn.joj.sk/live/andromeda/cs_film-1080.m3u8" + joj_headers, "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png", "epg": "Československá klasika"},
            {"nazov": "CS Mystery", "url": "https://live.cdn.joj.sk/live/andromeda/cs_mystery-1080.m3u8" + joj_headers, "logo": "https://img.joj.sk/90e3d390-9f4f-48cb-9773-98a0a119dfa8", "epg": "Záhady a paranormálne javy"},
            {"nazov": "Senzi TV", "url": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers, "logo": "http://googleusercontent.com/profile/picture/3", "epg": "Hudobné hity pre každého"}
        ]
        
        for tv in tv_stanice:
            # Spojíme názov a aktuálny program pre lepšiu prehľadnosť
            display_label = f"{tv['nazov']} | [COLOR yellow]{tv['epg']}[/COLOR]"
            li = xbmcgui.ListItem(label=display_label)
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"]})
            li.setInfo('video', {'title': tv["nazov"], 'plot': tv["epg"]})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
            
        xbmcplugin.endOfDirectory(handle)

    # --- 3. ARCHÍV - VÝBER DŇA ---
    elif params.get('mode') == 'list_archive_sk':
        for i in range(7):
            date_obj = datetime.now() - timedelta(days=i)
            date_str = date_obj.strftime('%d.%m.%Y')
            day_label = f"Dnes ({date_str})" if i == 0 else date_str
            
            url = build_url({'mode': 'archive_programs', 'date': date_str})
            li = xbmcgui.ListItem(label=day_label)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 4. ARCHÍV - ZOZNAM RELÁCIÍ (Oprava prehrávania) ---
    elif params.get('mode') == 'archive_programs':
        date = params.get('date')
        # Simulované relácie z tvojho obrázka (pre TV JOJ)
        relacie = [
            {"time": "12:15", "title": "James Bond: Casino Royale", "id": "casino_royale"},
            {"time": "15:25", "title": "Hviezdy nad hlavou 9", "id": "hviezdy"},
            {"time": "16:45", "title": "Na chalupe", "id": "chalupa"},
            {"time": "19:00", "title": "Krimi", "id": "krimi"},
            {"time": "19:30", "title": "Noviny TV JOJ", "id": "noviny"}
        ]
        
        for r in relacie:
            label = f"{r['time']} - {r['title']}"
            # URL musí smerovať na funkčný stream, aby archív nezlyhal
            # Pre test účely používame živý stream JOJ, kým nenapojíme konkrétne video z archívu
            play_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + joj_headers
            
            li = xbmcgui.ListItem(label=label)
            li.setInfo('video', {'title': r['title']})
            li.setProperty('IsPlayable', 'true') # TOTO OPRAVÍ CHYBU PREHRÁVANIA
            xbmcplugin.addDirectoryItem(handle, play_url, li, False)
            
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
