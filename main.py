import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Funkcia na generovanie URL adries pre menu
def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    handle = int(sys.argv[1])
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

    # --- 1. HLAVNÉ MENU (Pridaná TV sekcia) ---
    if not params:
        # Slovensko
        url_sk = build_url({'country': 'sk'})
        li_sk = xbmcgui.ListItem(label="[B]🇸🇰 SLOVENSKÉ RÁDIÁ[/B]")
        li_sk.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Flag_of_Slovakia.svg/200px-Flag_of_Slovakia.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_sk, li_sk, True)

        # Česko
        url_cz = build_url({'country': 'cz'})
        li_cz = xbmcgui.ListItem(label="[B]🇨🇿 ČESKÉ RÁDIÁ[/B]")
        li_cz.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/200px-Flag_of_the_Czech_Republic.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_cz, li_cz, True)

        # --- NOVÁ SEKCIA: FREE TV ---
        url_tv = build_url({'mode': 'tv'})
        li_tv = xbmcgui.ListItem(label="[B]📺 FREE TV SK/CZ[/B]")
        li_tv.setArt({'icon': 'https://cdn-icons-png.flaticon.com/512/716/716429.png'})
        xbmcplugin.addDirectoryItem(handle, url_tv, li_tv, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. ZOZNAM SLOVENSKÝCH RÁDIÍ ---
    elif params.get('country') == 'sk':
        radia_sk = [
            {"nazov": "Fresh Rádio", "url": "https://icecast2.radionet.sk/freshradio.sk", "logo": "https://myonlineradio.sk/public/uploads/radio_img/fresh-radio/play_250_250.webp"},
            {"nazov": "Rádio Rock", "url": "https://stream.bauermedia.sk/rock-hi.mp3", "logo": "https://radiorock.sk/intro-v2.png"},
            # ... (ostatné tvoje rádiá)
            {"nazov": "Rádio Vlna", "url": "https://stream.radiovlna.sk/vlna-128.mp3", "logo": "https://www.radiovlna.sk/static/images/logo.png"}
        ]
        zobraz_polozky(handle, radia_sk)

    # --- 3. ZOZNAM ČESKÝCH RÁDIÍ ---
    elif params.get('country') == 'cz':
        radia_cz = [
            {"nazov": "Rádio Kiss", "url": "https://ice.actve.net/fm-kiss-128", "logo": "https://www.kiss.cz/assets/img/logo.png"},
            # ... (ostatné české rádiá)
        ]
        zobraz_polozky(handle, radia_cz)

    # --- 4. NOVÁ LOGIKA: ZOZNAM TV STANÍC ---
    elif params.get('mode') == 'tv':
        tv_kanaly = [
            {"nazov": "RTVS Jednotka", "url": "URL_STREAMU_JEDNOTKA", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/RTVS_Jednotka_logo.svg/512px-RTVS_Jednotka_logo.svg.png"},
            {"nazov": "RTVS Dvojka", "url": "URL_STREAMU_DVOJKA", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/RTVS_Dvojka_logo.svg/512px-RTVS_Dvojka_logo.svg.png"},
            {"nazov": "ČT 24", "url": "URL_STREAMU_CT24", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/CT24_logo.svg/512px-CT24_logo.svg.png"}
        ]
        zobraz_polozky(handle, tv_kanaly)

# Univerzálna funkcia na zobrazenie (premenovaná zo zobraz_radia)
def zobraz_polozky(handle, zoznam):
    for polozka in zoznam:
        li = xbmcgui.ListItem(label=polozka["nazov"])
        li.setArt({
            'thumb': polozka["logo"],
            'icon': polozka["logo"]
        })
        li.setInfo('video', {'title': polozka["nazov"]})
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle, polozka["url"], li, False)
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
