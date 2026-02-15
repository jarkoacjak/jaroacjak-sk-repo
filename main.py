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

    # --- 1. HLAVNÉ MENU ---
    if not params:
        # Slovenské rádiá
        url_sk = build_url({'mode': 'list_radios', 'country': 'sk'})
        li_sk = xbmcgui.ListItem(label="[B]🇸🇰 SLOVENSKÉ RÁDIÁ[/B]")
        li_sk.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Flag_of_Slovakia.svg/200px-Flag_of_Slovakia.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_sk, li_sk, True)

        # České rádiá
        url_cz = build_url({'mode': 'list_radios', 'country': 'cz'})
        li_cz = xbmcgui.ListItem(label="[B]🇨🇿 ČESKÉ RÁDIÁ[/B]")
        li_cz.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/200px-Flag_of_the_Czech_Republic.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_cz, li_cz, True)

        # NOVINKA: FREE TV SEKCIÁ
        url_tv = build_url({'mode': 'list_tv'})
        li_tv = xbmcgui.ListItem(label="[B]📺 FREE TV SK/CZ[/B]")
        li_tv.setArt({'icon': 'https://cdn-icons-png.flaticon.com/512/716/716429.png'})
        xbmcplugin.addDirectoryItem(handle, url_tv, li_tv, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. LOGIKA PRE RÁDIÁ ---
    elif params.get('mode') == 'list_radios':
        krajina = params.get('country')
        if krajina == 'sk':
            polozky = [
                {"nazov": "Fresh Rádio", "url": "https://icecast2.radionet.sk/freshradio.sk", "logo": "https://myonlineradio.sk/public/uploads/radio_img/fresh-radio/play_250_250.webp"},
                {"nazov": "Rádio Rock", "url": "https://stream.bauermedia.sk/rock-hi.mp3", "logo": "https://radiorock.sk/intro-v2.png"},
                {"nazov": "Europa 2", "url": "https://stream.bauermedia.sk/europa2-hi.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/europa2.png"},
                {"nazov": "Rádio Slovensko", "url": "https://icecast.stv.livebox.sk/slovensko_128.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-slovensko/play_250_250.webp"}
            ]
        else: # CZ rádia
            polozky = [
                {"nazov": "Rádio Kiss", "url": "https://ice.actve.net/fm-kiss-128", "logo": "https://www.kiss.cz/assets/img/logo.png"},
                {"nazov": "Rádio Impuls", "url": "http://icecast5.play.cz/impuls128.mp3", "logo": "https://www.impuls.cz/img/logo-impuls.png"}
            ]
        zobraz_obsah(handle, polozky, is_video=False)

    # --- 3. LOGIKA PRE TV ---
    elif params.get('mode') == 'list_tv':
        tv_kanaly = [
            {"nazov": "RTVS Jednotka", "url": "https://cdn.example.com/jednotka.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/RTVS_Jednotka_logo.svg/512px-RTVS_Jednotka_logo.svg.png"},
            {"nazov": "RTVS Dvojka", "url": "https://cdn.example.com/dvojka.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/RTVS_Dvojka_logo.svg/512px-RTVS_Dvojka_logo.svg.png"}
        ]
        zobraz_obsah(handle, tv_kanaly, is_video=True)

# Spoločná funkcia na zobrazenie
def zobraz_obsah(handle, zoznam, is_video):
    for p in zoznam:
        li = xbmcgui.ListItem(label=p["nazov"])
        li.setArt({'thumb': p["logo"], 'icon': p["logo"]})
        if is_video:
            li.setInfo('video', {'title': p["nazov"]})
        else:
            li.setInfo('music', {'title': p["nazov"]})
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle, p["url"], li, False)
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
