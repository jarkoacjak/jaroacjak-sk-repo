import sys
import urllib.parse
import xbmcgui
import xbmcplugin

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    handle = int(sys.argv[1])
    arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
    params = dict(urllib.parse.parse_qsl(arg_string))

    # --- 1. HLAVNÉ MENU (Živé vysielanie / Archív) ---
    if not params:
        # Tlačidlo Živé vysielanie
        url_live = build_url({'mode': 'select_country_live'})
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        # Tlačidlo Archív
        url_archive = build_url({'mode': 'select_country_archive'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV[/B]")
        xbmcplugin.addDirectoryItem(handle, url_archive, li_archive, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. VÝBER KRAJINY PRE ŽIVÉ TV ---
    elif params.get('mode') == 'select_country_live':
        # Slovensko Live
        url_sk = build_url({'mode': 'list_live_sk'})
        li_sk = xbmcgui.ListItem(label="[B]🇸🇰 Slovenské TV (Živo)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_sk, li_sk, True)

        # Česko Live
        url_cz = build_url({'mode': 'list_live_cz'})
        li_cz = xbmcgui.ListItem(label="[B]🇨🇿 České TV (Živo)[/B]")
        xbmcplugin.addDirectoryItem(handle, url_cz, li_cz, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 3. VÝBER KRAJINY PRE ARCHÍV ---
    elif params.get('mode') == 'select_country_archive':
        # Slovensko Archív
        url_sk_arc = build_url({'mode': 'msg_archive'})
        li_sk_arc = xbmcgui.ListItem(label="[B]🇸🇰 Slovensko - ARCHÍV[/B]")
        xbmcplugin.addDirectoryItem(handle, url_sk_arc, li_sk_arc, True)

        # Česko Archív
        url_cz_arc = build_url({'mode': 'msg_archive'})
        li_cz_arc = xbmcgui.ListItem(label="[B]🇨🇿 Česko - ARCHÍV[/B]")
        xbmcplugin.addDirectoryItem(handle, url_cz_arc, li_cz_arc, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 4. ZOZNAM ŽIVÝCH SK STANÍC ---
    elif params.get('mode') == 'list_live_sk':
        tv_list = [
            {"nazov": "TV JOJ", "url": "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/TV_JOJ_logo_2015.svg/1200px-TV_JOJ_logo_2015.svg.png"},
            {"nazov": "TA3", "url": "https://live.ta3.com/live/ta3/ta3.m3u8", "logo": "https://www.ta3.com/img/logo-ta3.png"},
        ]
        for tv in tv_list:
            li = xbmcgui.ListItem(label=tv["nazov"])
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"]})
            li.setInfo('video', {'title': tv["nazov"], 'mediatype': 'video'})
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- 5. OZNAM PRE ARCHÍV ---
    elif params.get('mode') == 'msg_archive':
        xbmcgui.Dialog().ok("Informácia", "Archív pripravujeme")
        # Vráti používateľa späť do menu
        xbmcplugin.endOfDirectory(handle, False)

if __name__ == '__main__':
    main()
    
