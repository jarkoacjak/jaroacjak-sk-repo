import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Funkcia na generovanie URL adries pre menu
def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    try:
        handle = int(sys.argv[1])
        arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
        params = dict(urllib.parse.parse_qsl(arg_string))
    except:
        return

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
            {"nazov": "Rádio Viva", "url": "http://stream.sepia.sk:8000/viva320.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-viva/play_250_250.webp"},
            {"nazov": "Fresh Rádio", "url": "https://icecast2.radionet.sk/freshradio.sk", "logo": "https://myonlineradio.sk/public/uploads/radio_img/fresh-radio/play_250_250.webp"},
            {"nazov": "Rádio Rock", "url": "https://stream.bauermedia.sk/rock-hi.mp3", "logo": "https://radiorock.sk/intro-v2.png"},
            {"nazov": "Rádio Maria Slovakia", "url": "https://dreamsiteradiocp5.com/proxy/radiomariaslomp3?mp=/stream.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-maria-slovensko/play_250_250.webp"},
            {"nazov": "Rádio Lumen", "url": "https://audio.lumen.sk/live128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/lumen.png"},
            {"nazov": "Na vlne Novohradu", "url": "https://radioserver.online/proxy/navlnenovohradu/novohradHQ.mp3", "logo": "https://www.radia.sk/_radia/loga/app/na-vlne-novohradu.webp?v=2"},
            {"nazov": "Na vlne Liptova", "url": "http://radioserver.online:8009/hq.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/na-vlne-liptova.png"},
            {"nazov": "Mirjam Radio", "url": "https://dreamsiteradiocp5.com/proxy/rmslo?mp=/stream", "logo": "https://www.radia.sk/_radia/loga/app/mirjam.webp?v=1"},
            {"nazov": "METALSCENA netRADIO", "url": "https://listen.radioking.com/radio/263218/stream/308365", "logo": "https://www.radia.sk/_radia/loga/coverflow/metalscena.png"},
            {"nazov": "Mars Dance Rádio", "url": "https://stream.zenolive.com/683gf5xrxfeuv?1686916511841", "logo": "https://www.radia.sk/_radia/loga/app/mars-dance.webp?v=2"},
            {"nazov": "HITRÁDIO SLOVAKIA", "url": "https://hitradioslovakia.stream.laut.fm/hitradioslovakia", "logo": "https://myonlineradio.sk/public/uploads/radio_img/hitradio-slovakia/play_250_250.webp"},
            {"nazov": "G - Rádio", "url": "http://88.212.34.18:8000/aacphighband.aac", "logo": "https://www.radia.sk/_radia/loga/coverflow/g-radio.png"},
            {"nazov": "Fun Rádio Mileniálky", "url": "https://stream.funradio.sk:8000/milenialky128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/fun-milenialky.png"},
            {"nazov": "Fun Rádio Leto", "url": "https://stream.funradio.sk:8000/summer128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/fun-letne-hity.png"},
            {"nazov": "Fun Rádio Chill", "url": "https://stream.funradio.sk/chill128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/fun-chill.png"},
            {"nazov": "Fun Rádio Dance", "url": "http://stream.funradio.sk:8000/dance128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/fun-dance.png"},
            {"nazov": "Fun Rádio CZ - SK", "url": "http://stream.funradio.sk:8000/cs128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/fun-cz-sk.png"},
            {"nazov": "Fun Rádio 80s - 90s", "url": "http://stream.funradio.sk:8000/80-90-128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/fun-80-90-roky.png"},
            {"nazov": "BB FM", "url": "http://stream.bbfm.sk:8000/bbfm128.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/bb-fm-radio/play_250_250.webp"},
            {"nazov": "Rádio Regina - Západ", "url": "https://icecast.stv.livebox.sk/regina-ba_128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/regina-zapad.png"},
            {"nazov": "Rádio Regina - Stred", "url": "https://icecast.stv.livebox.sk/regina-bb_128.mp3", "logo": "https://www.radia.sk/_radia/loga/app/regina-stred.webp?v=2"},
            {"nazov": "Rádio Regina - Východ", "url": "https://icecast.stv.livebox.sk/regina-ke_128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/regina-vychod.png"},
            {"nazov": "Rádio Devín", "url": "https://icecast.stv.livebox.sk/devin_128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/devin.png"},
            {"nazov": "Europa 2", "url": "https://stream.bauermedia.sk/europa2-hi.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/europa2.png"},
            {"nazov": "Dobré Rádio", "url": "https://stream.dobreradio.sk/dobreradio.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/dobre.png"},
            {"nazov": "Rádio InfoVojna", "url": "https://stream1.infovojna.com:8000/live", "logo": "https://topradio.sk/_next/image?url=%2Fimages%2Finfovojna.jpg&w=640&q=75"},
            {"nazov": "Rádio_FM", "url": "https://icecast.stv.livebox.sk/fm_128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/fm.png"},
            {"nazov": "Rádio Dychovka", "url": "https://epanel.mediacp.eu:7661/stream", "logo": "https://www.radia.sk/_radia/loga/app/dychovka.webp?v=1"},
            {"nazov": "Rádio Košice", "url": "http://stream.ecce.sk:8000/radiokosice-128.mp3", "logo": "https://data.tvkosice.sk/images/cm/1000x0xresize/r/a/d/radiokosice/8e/fe/8efe9b31-bd08-4f5d-9168-fa656184fdd2.jpg"},
            {"nazov": "FIT Family RADIO", "url": "http://solid67.streamupsolutions.com:8052/;", "logo": "https://www.radia.sk/_radia/loga/app/fit-family.webp?v=1"},
            {"nazov": "Rádio WOW", "url": "https://radioserver.online:9816/radiowow.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/wow.png"},
            {"nazov": "Rádio Slovensko", "url": "https://icecast.stv.livebox.sk/slovensko_128.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-slovensko/play_250_250.webp"},
            {"nazov": "Detské Rádio", "url": "https://stream.21.sk/detskeradio-192.mp3", "logo": "https://data.tvkosice.sk/images/cm/1000x0xresize/r/a/d/radiokosice/08/80/0880daa2-a629-4ce0-9bf9-ab7765572c2f.jpg"},
            {"nazov": "Rádio Frontinus", "url": "http://stream.frontinus.sk:8000/frontinus128.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-frontinus/play_250_250.webp"},
            {"nazov": "Rádio Expres", "url": "https://stream.expres.sk/128.mp3", "logo": "https://www.radia.sk/_radia/loga/coverflow/expres.png"},
            {"nazov": "Rádio Melody", "url": "https://stream.bauermedia.sk/melody-hi.mp3", "logo": "https://www.radiomelody.sk/cover.png?f=raw"},
            {"nazov": "Rádio Beta", "url": "http://109.71.67.102:8000/beta_live_high.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-beta/play_250_250.webp"},
            {"nazov": "Fun Rádio", "url": "https://stream.funradio.sk:8000/fun128.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/fun-radio/play_250_250.webp"},
            {"nazov": "Rádio Vlna", "url": "http://stream.radiovlna.sk/vlna-hi.mp3", "logo": "https://myonlineradio.sk/public/uploads/radio_img/radio-vlna/play_250_250.webp"}
        ]
        zobraz_radia(handle, radia_sk)

    # --- 3. ZOZNAM ČESKÝCH RÁDIÍ ---
    elif params.get('country') == 'cz':
        radia_cz = [
            {"nazov": "Rádio Kiss", "url": "https://n25a-eu.rcs.revma.com/asn0cmvb938uv", "logo": "https://i1.sndcdn.com/artworks-000055555247-hukx9y-t500x500.jpg"},
            {"nazov": "Rádio Impuls", "url": "http://icecast5.play.cz/impuls128.mp3", "logo": "https://www.impuls.cz/img/logo-impuls.png"},
            {"nazov": "Evropa 2", "url": "https://ice.actve.net/fm-evropa2-128", "logo": "https://www.evropa2.cz/wp-content/themes/evropa2/assets/img/logo.png"},
            {"nazov": "Frekvence 1", "url": "https://ice.actve.net/fm-frekvence1-128", "logo": "https://www.frekvence1.cz/img/logo-f1.png"},
            {"nazov": "Rádio Blaník", "url": "http://ice.abradio.cz/blanikfm128.mp3", "logo": "https://radioblanik.cz/wp-content/themes/blanik/img/logo.png"}
        ]
        zobraz_radia(handle, radia_cz)

# Univerzálna funkcia na zobrazenie zoznamu
def zobraz_radia(handle, zoznam):
    for radio in zoznam:
        li = xbmcgui.ListItem(label=radio["nazov"])
        li.setArt({
            'thumb': radio["logo"],
            'icon': radio["logo"],
            'poster': radio["logo"],
            'fanart': radio["logo"]
        })
        li.setInfo('audio', {
            'title': radio["nazov"],
            'mediatype': 'music',
            'comment': 'Live Stream'
        })
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle, radio["url"], li, False)
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
