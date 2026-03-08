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
        # Slovensko
        url_sk = build_url({'mode': 'list_live_sk'})
        li_sk = xbmcgui.ListItem(label="[B]🇸🇰 SLOVENSKÉ TELEVÍZIE[/B]")
        li_sk.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Flag_of_Slovakia.svg/200px-Flag_of_Slovakia.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_sk, li_sk, True)

        # Česko
        url_cz = build_url({'mode': 'msg_archive'}) 
        li_cz = xbmcgui.ListItem(label="[B]🇨🇿 ČESKÉ TELEVÍZIE[/B]")
        li_cz.setArt({'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/200px-Flag_of_the_Czech_Republic.svg.png'})
        xbmcplugin.addDirectoryItem(handle, url_cz, li_cz, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 3. ZOZNAM SLOVENSKÝCH TV (Iba TV JOJ) ---
    elif params.get('mode') == 'list_live_sk':
        # Tvoj opravený stream a logo
        joj_url = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8"
        # Priamy odkaz na logo z tvojho vyhľadávania
        joj_logo = "https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj"
        
        li = xbmcgui.ListItem(label="TV JOJ")
        li.setArt({'thumb': joj_logo, 'icon': joj_logo, 'fanart': joj_logo})
        
        # Nastavenie videa
        li.setInfo('video', {'title': 'TV JOJ', 'mediatype': 'video'})
        li.setProperty('IsPlayable', 'true')
        
        # Pridanie položky (isFolder=False znamená, že sa hneď spustí prehrávanie)
        xbmcplugin.addDirectoryItem(handle, joj_url, li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- 4. OZNAM PRE ARCHÍV ---
    elif params.get('mode') == 'msg_archive':
        xbmcgui.Dialog().ok("Informácia", "Archív pripravujeme")
        xbmcplugin.endOfDirectory(handle, False)

if __name__ == '__main__':
    main()
    
