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

    # --- 1. HLAVNÉ MENU (Výber krajiny) ---
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

        xbmcplugin.endOfDirectory(handle)

    # --- 2. ZOZNAM SLOVENSKÝCH RÁDIÍ ---
    elif params.get('country') == 'sk':
        radia_sk = [
            {"nazov": "Rádio Slovensko", "url": "https://icecast.stv.livebox.sk/slovensko_128.mp3", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/R%C3%A1dio_Slovensko.svg/1200px-R%C3%A1dio_Slovensko.svg.png"},
            {"nazov": "Detské Rádio", "url": "https://stream.21.sk/detskeradio-192.mp3", "logo": "https://data.tvkosice.sk/images/cm/1000x0xresize/r/a/d/radiokosice/08/80/0880daa2-a629-4ce0-9bf9-ab7765572c2f.jpg"},
            {"nazov": "Rádio Expres", "url": "https://stream.expres.sk/128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/expres.png"},
            {"nazov": "Rádio Melody", "url": "https://stream.bauermedia.sk/melody-hi.mp3", "logo": "https://www.radiomelody.sk/cover.png?f=raw"},
            {"nazov": "Rádio Beta", "url": "http://109.71.67.102:8000/beta_live_high.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-beta/play_250_250.webp"},
            {"nazov": "Fun Rádio", "url": "https://stream.funradio.sk:8000/fun128.mp3", "logo": "https://static.skm.funradio.sk/images/funradio_logo_og.png"},
            {"nazov": "Rádio Vlna", "url": "https://stream.radiovlna.sk/vlna-128.mp3", "logo": "https://www.radiovlna.sk/static/images/logo.png"}
        ]
        zobraz_radia(handle, radia_sk)

    # --- 3. ZOZNAM ČESKÝCH RÁDIÍ ---
    elif params.get('country') == 'cz':
        radia_cz = [
            {"nazov": "Rádio Kiss", "url": "https://ice.actve.net/fm-kiss-128", "logo": "https://www.kiss.cz/assets/img/logo.png"},
            {"nazov": "Rádio Impuls", "url": "http://icecast5.play.cz/impuls128.mp3", "logo": "https://www.impuls.cz/img/logo-impuls.png"},
            {"nazov": "Evropa 2", "url": "https://ice.actve.net/fm-evropa2-128", "logo": "https://www.evropa2.cz/wp-content/themes/evropa2/assets/img/logo.png"},
            {"nazov": "Frekvence 1", "url": "https://ice.actve.net/fm-frekvence1-128", "logo": "https://www.frekvence1.cz/img/logo-f1.png"},
            {"nazov": "Rádio Blaník", "url": "http://ice.abradio.cz/blanikfm128.mp3", "logo": "https://radioblanik.cz/wp-content/themes/blanik/img/logo.png"}
        ]
        zobraz_radia(handle, radia_cz)

# Univerzálna funkcia na vykreslenie zoznamu staníc
def zobraz_radia(handle, zoznam):
    for radio in zoznam:
        li = xbmcgui.ListItem(label=radio["nazov"])
        li.setArt({
            'thumb': radio["logo"],
            'icon': radio["logo"],
            'poster': radio["logo"],
            'fanart': radio["logo"]
        })
        li.setInfo('video', {
            'title': radio["nazov"]
        })
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle, radio["url"], li, False)
    
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
