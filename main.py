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
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        url_archive = build_url({'mode': 'archive_days'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV (Dovysielané relácie)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_archive, li_archive, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 2. ŽIVÉ VYSIELANIE (Všetky kanály späť, EPG iba pre JOJ) ---
    elif params.get('mode') == 'list_live_sk':
        tv_stanice = [
            {"nazov": "TV JOJ", "url": "joj-1080.m3u8", "logo": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj", "epg": "James Bond: Casino Royale"},
            {"nazov": "JOJ Plus", "url": "plus-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100063553059682"},
            {"nazov": "JOJ Krimi", "url": "wau-1080.m3u8", "logo": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg"},
            {"nazov": "JOJ Šport", "url": "joj_sport-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738"},
            {"nazov": "JOJ 24", "url": "joj_news-1080.m3u8", "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437"},
            {"nazov": "Jojko", "url": "jojko-1080.m3u8", "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj"},
            {"nazov": "JOJ Cinema", "url": "cinema-1080.m3u8", "logo": "http://googleusercontent.com/profile/picture/2"},
            {"nazov": "JOJ Family", "url": "family-1080.m3u8", "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BDUQMIAK/873-joj-family-hd.png"},
            {"nazov": "CS History", "url": "cs_history-1080.m3u8", "logo": "https://img.joj.sk/418430b1-b598-40d1-8552-39b473c73836"},
            {"nazov": "CS Film", "url": "cs_film-1080.m3u8", "logo": "https://staticeu.sweet.tv/images/cache/channel_icons/BCTQOIAK/935-cs-film-hd.png"},
            {"nazov": "CS Mystery", "url": "cs_mystery-1080.m3u8", "logo": "https://img.joj.sk/90e3d390-9f4f-48cb-9773-98a0a119dfa8"},
            {"nazov": "Senzi TV", "url": "https://lb.streaming.sk/senzi/stream/playlist.m3u8" + common_headers, "logo": "http://googleusercontent.com/profile/picture/3", "is_custom": True}
        ]
        
        for tv in tv_stanice:
            full_url = tv["url"] if "is_custom" in tv else "https://live.cdn.joj.sk/live/andromeda/" + tv["url"] + joj_headers
            
            # EPG sa zobrazí iba pri TV JOJ, ostatné stanice majú čistý názov
            label = f"{tv['nazov']} | [COLOR yellow]{tv['epg']}[/COLOR]" if "epg" in tv else tv["nazov"]
            
            li = xbmcgui.ListItem(label=label)
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"]})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, full_url, li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- 3. ARCHÍV - DNI ---
    elif params.get('mode') == 'archive_days':
        for i in range(7):
            date_obj = now - timedelta(days=i)
            date_str = date_obj.strftime('%d.%m.%Y')
            url = build_url({'mode': 'archive_list', 'date': date_str, 'day_offset': str(i)})
            li = xbmcgui.ListItem(label=date_str)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 4. ARCHÍV - ZOZNAM (Prehrávanie toho, čo už skončilo) ---
    elif params.get('mode') == 'archive_list':
        day_offset = int(params.get('day_offset'))
        target_date = now - timedelta(days=day_offset)
        joj_logo = "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"

        # Program, ktorý sa po odvysielaní "uloží" do archívu
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
            
            # ARCHÍV: Pustí reláciu len ak už v TV skončila
            if now > (start_dt + timedelta(minutes=r["dur"])):
                start_ts = int(start_dt.timestamp())
                archive_url = f"https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8?start={start_ts}" + joj_headers
                
                li = xbmcgui.ListItem(label=f"{r['time']} - {r['title']}")
                li.setArt({'thumb': joj_logo, 'icon': joj_logo})
                li.setInfo('video', {'title': r['title'], 'plot': "Archívny záznam - spustí sa od začiatku."})
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle, archive_url, li, False)
            
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
