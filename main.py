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

    # --- 1. HLAVNÉ MENU (Živé vysielanie / Archív) ---
    if not params:
        url_live = build_url({'mode': 'select_country_live'})
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        url_archive = build_url({'mode': 'msg_archive'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV[/B]")
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

    # --- 3. ZOZNAM SLOVENSKÝCH TV ---
    elif params.get('mode') == 'list_live_sk':
        # Overené hlavičky pre stabilitu JOJ streamov
        headers = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://videoportal.joj.sk/"
        
        tv_stanice = [
            {
                "nazov": "TV JOJ", 
                "url": "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + headers, 
                "logo": "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"
            },
            {
                "nazov": "JOJ Krimi", 
                "url": "https://live.cdn.joj.sk/live/andromeda/wau-1080.m3u8" + headers, 
                "logo": "https://www.interez.sk/wp-content/uploads/2026/02/krimi-joj-wau-televizia.jpg"
            },
            {
                "nazov": "JOJ Šport", 
                "url": "https://live.cdn.joj.sk/live/andromeda/joj_sport-1080.m3u8" + headers, 
                "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100072427963738"
            },
            {
                "nazov": "JOJ 24", 
                "url": "https://live.cdn.joj.sk/live/andromeda/joj_news-1080.m3u8" + headers, 
                "logo": "https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=100086546375437"
            },
            {
                "nazov": "Jojko", 
                "url": "https://live.cdn.joj.sk/live/andromeda/jojko-1080.m3u8" + headers, 
                "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k5JuOcgs57bLqO5jeAGqVWKskOxWRaYh1_mD7PYcE4Wg=s900-c-k-c0x00ffffff-no-rj"
            },
            {
                "nazov": "JOJ Cinema", 
                "url": "https://live.cdn.joj.sk/live/andromeda/cinema-1080.m3u8" + headers, 
                "logo": "http://googleusercontent.com/profile/picture/2"
            }
        ]
        
        for tv in tv_stanice:
            li = xbmcgui.ListItem(label=tv["nazov"])
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"], 'fanart': tv["logo"]})
            li.setInfo('video', {'title': tv["nazov"], 'mediatype': 'video'})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
            
        xbmcplugin.endOfDirectory(handle)

    # --- 4. OZNAM PRE ARCHÍV ---
    elif params.get('mode') == 'msg_archive':
        xbmcgui.Dialog().ok("Informácia", "Archív pripravujeme")
        xbmcplugin.endOfDirectory(handle, False)

if __name__ == '__main__':
    main()
    
