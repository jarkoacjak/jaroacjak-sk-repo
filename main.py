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

    # --- 1. HLAVNÉ MENU ---
    if not params:
        for mode, label in [('select_country_live', "📺 ŽIVÉ VYSIELANIE / PROGRAM"), ('select_country_archive', "📂 ARCHÍV (7 DNÍ)")]:
            url = build_url({'mode': mode})
            li = xbmcgui.ListItem(label=f"[B]{label}[/B]")
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 2. VÝBER KRAJINY (ŽIVÉ AJ ARCHÍV) ---
    elif params.get('mode') in ['select_country_live', 'select_country_archive']:
        current_mode = params.get('mode')
        dest_mode = 'list_live_sk' if current_mode == 'select_country_live' else 'list_archive_sk'
        
        # Slovensko
        url_sk = build_url({'mode': dest_mode})
        li_sk = xbmcgui.ListItem(label="[B]🇸🇰 SLOVENSKÉ TELEVÍZIE[/B]")
        li_sk.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Flag_of_Slovakia.svg/200px-Flag_of_Slovakia.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_sk, li_sk, True)

        # Česko (Zatiaľ oznam)
        url_cz = build_url({'mode': 'msg_pripravujeme'})
        li_cz = xbmcgui.ListItem(label="[B]🇨🇿 ČESKÉ TELEVÍZIE[/B]")
        li_cz.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/200px-Flag_of_the_Czech_Republic.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_cz, li_cz, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 3. ZOZNAM STANÍC PRE ARCHÍV ---
    elif params.get('mode') == 'list_archive_sk':
        # Zatiaľ len JOJka, postupne pridáme ďalšie
        url = build_url({'mode': 'archive_days', 'channel': 'TV JOJ'})
        li = xbmcgui.ListItem(label="TV JOJ (Archív)")
        li.setArt({'icon': 'https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj'})
        xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 4. VÝBER DŇA (7 DNÍ) ---
    elif params.get('mode') == 'archive_days':
        channel = params.get('channel')
        for i in range(7):
            date_obj = datetime.now() - timedelta(days=i)
            date_str = date_obj.strftime('%d.%m.%Y')
            day_name = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Sobota", "Nedeľa"][date_obj.weekday()]
            
            label = f"{day_name} ({date_str})"
            if i == 0: label = f"[COLOR yellow]Dnes - {label}[/COLOR]"
            
            url = build_url({'mode': 'archive_list_programs', 'channel': channel, 'date': date_str})
            li = xbmcgui.ListItem(label=label)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 5. ZOZNAM PROGRAMOV (UKÁŽKA) ---
    elif params.get('mode') == 'archive_list_programs':
        # Tu sa neskôr napojí reálne získavanie relácií z webu
        xbmcgui.Dialog().ok("Archív", f"Tu bude zoznam relácií pre {params.get('channel')} zo dňa {params.get('date')}")
        xbmcplugin.endOfDirectory(handle, False)

    # --- ŠTANDARDNÝ ZOZNAM ŽIVÝCH TV ---
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
            li.setInfo('video', {'title': tv["nazov"]})
            li.setProperty('epg_id', tv["epg_id"])
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
        xbmcplugin.endOfDirectory(handle)

    elif params.get('mode') == 'msg_pripravujeme':
        xbmcgui.Dialog().ok("Informácia", "Túto sekciu pripravujeme")
        xbmcplugin.endOfDirectory(handle, False)

if __name__ == '__main__':
    main()
    
