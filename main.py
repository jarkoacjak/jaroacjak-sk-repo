import sys
import urllib.parse
import xbmcgui
import xbmcplugin

def main():
    # Zakladne nastavenie handle a parametrov
    try:
        handle = int(sys.argv[1])
        arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
        params = dict(urllib.parse.parse_qsl(arg_string))
    except:
        return

    # --- 1. HLAVNE MENU ---
    if not params:
        # Slovensko
        li = xbmcgui.ListItem(label="[B]🇸🇰 SLOVENSKÉ RÁDIÁ[/B]")
        li.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Flag_of_Slovakia.svg/200px-Flag_of_Slovakia.svg.png'})
        url = sys.argv[0] + "?" + urllib.parse.urlencode({'country': 'sk'})
        xbmcplugin.addDirectoryItem(handle, url, li, True)

        # Cesko
        li = xbmcgui.ListItem(label="[B]🇨🇿 ČESKÉ RÁDIÁ[/B]")
        li.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/200px-Flag_of_the_Czech_Republic.svg.png'})
        url = sys.argv[0] + "?" + urllib.parse.urlencode({'country': 'cz'})
        xbmcplugin.addDirectoryItem(handle, url, li, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. SLOVENSKE RADIA ---
    elif params.get('country') == 'sk':
        radia = [
            {"n": "Rádio Viva", "u": "http://stream.sepia.sk:8000/viva320.mp3", "l": "https://myonlineradio.sk/public/uploads/radio_img/radio-viva/play_250_250.webp"},
            {"n": "Fresh Rádio", "u": "https://icecast2.radionet.sk/freshradio.sk", "l": "https://myonlineradio.sk/public/uploads/radio_img/fresh-radio/play_250_250.webp"},
            {"n": "Rádio Rock", "u": "https://stream.bauermedia.sk/rock-hi.mp3", "l": "https://radiorock.sk/intro-v2.png"},
            {"n": "Europa 2", "u": "https://stream.bauermedia.sk/europa2-hi.mp3", "l": "https://www.radia.sk/_radia/loga/coverflow/europa2.png"},
            {"n": "Dobré Rádio", "u": "https://stream.dobreradio.sk/dobreradio.mp3", "l": "https://www.radia.sk/_radia/loga/coverflow/dobre.png"},
            {"n": "Rádio InfoVojna", "u": "https://stream1.infovojna.com:8000/live", "l": "https://topradio.sk/_next/image?url=%2Fimages%2Finfovojna.jpg&w=640&q=75"},
            {"n": "Rádio_FM", "u": "https://icecast.stv.livebox.sk/fm_128.mp3", "l": "https://www.radia.sk/_radia/loga/coverflow/fm.png"},
            {"n": "Rádio Dychovka", "u": "https://epanel.mediacp.eu:7661/stream", "l": "https://www.radia.sk/_radia/loga/app/dychovka.webp?v=1"},
            {"n": "Rádio Košice", "u": "http://stream.ecce.sk:8000/radiokosice-128.mp3", "l": "https://data.tvkosice.sk/images/cm/1000x0xresize/r/a/d/radiokosice/8e/fe/8efe9b31-bd08-4f5d-9168-fa656184fdd2.jpg"},
            {"n": "FIT Family RADIO", "u": "http://solid67.streamupsolutions.com:8052/;", "l": "https://www.radia.sk/_radia/loga/app/fit-family.webp?v=1"},
            {"n": "Rádio WOW", "u": "https://radioserver.online:9816/radiowow.mp3", "l": "https://www.radia.sk/_radia/loga/coverflow/wow.png"},
            {"n": "Rádio Slovensko", "u": "https://icecast.stv.livebox.sk/slovensko_128.mp3", "l": "https://myonlineradio.sk/public/uploads/radio_img/radio-slovensko/play_250_250.webp"},
            {"n": "Detské Rádio", "u": "https://stream.21.sk/detskeradio-192.mp3", "l": "https://data.tvkosice.sk/images/cm/1000x0xresize/r/a/d/radiokosice/08/80/0880daa2-a629-4ce0-9bf9-ab7765572c2f.jpg"},
            {"n": "Rádio Frontinus", "u": "http://stream.frontinus.sk:8000/frontinus128.mp3", "l": "https://myonlineradio.sk/public/uploads/radio_img/radio-frontinus/play_250_250.webp"},
            {"n": "Rádio Expres", "u": "https://stream.expres.sk/128.mp3", "l": "https://www.radia.sk/_radia/loga/coverflow/expres.png"},
            {"n": "Rádio Melody", "u": "https://stream.bauermedia.sk/melody-hi.mp3", "l": "https://www.radiomelody.sk/cover.png?f=raw"},
            {"n": "Rádio Beta", "u": "http://109.71.67.102:8000/beta_live_high.mp3", "l": "https://myonlineradio.sk/public/uploads/radio_img/radio-beta/play_250_250.webp"},
            {"n": "Fun Rádio", "u": "https://stream.funradio.sk:8000/fun128.mp3", "l": "https://myonlineradio.sk/public/uploads/radio_img/fun-radio/play_250_250.webp"},
            {"n": "Rádio Vlna", "u": "https://stream.radiovlna.sk/vlna-128.mp3", "l": "https://www.radiovlna.sk/static/images/logo.png"}
        ]
        for r in radia:
            item = xbmcgui.ListItem(label=r["n"])
            item.setArt({'icon': r["l"], 'thumb': r["l"]})
            item.setInfo('audio', {'title': r["n"]})
            item.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, r["u"], item, False)
        xbmcplugin.endOfDirectory(handle)

    # --- 3. CESKE RADIA ---
    elif params.get('country') == 'cz':
        radia_cz = [
            {"n": "Rádio Kiss", "u": "https://ice.actve.net/fm-kiss-128", "l": "https://www.kiss.cz/assets/img/logo.png"},
            {"n": "Rádio Impuls", "u": "http://icecast5.play.cz/impuls128.mp3", "l": "https://www.impuls.cz/img/logo-impuls.png"},
            {"n": "Evropa 2", "u": "https://ice.actve.net/fm-evropa2-128", "l": "https://www.evropa2.cz/wp-content/themes/evropa2/assets/img/logo.png"},
            {"n": "Frekvence 1", "u": "https://ice.actve.net/fm-frekvence1-128", "l": "https://www.frekvence1.cz/img/logo-f1.png"},
            {"n": "Rádio Blaník", "u": "http://ice.abradio.cz/blanikfm128.mp3", "l": "https://radioblanik.cz/wp-content/themes/blanik/img/logo.png"}
        ]
        for r in radia_cz:
            item = xbmcgui.ListItem(label=r["n"])
            item.setArt({'icon': r["l"], 'thumb': r["l"]})
            item.setInfo('audio', {'title': r["n"]})
            item.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, r["u"], item, False)
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()

