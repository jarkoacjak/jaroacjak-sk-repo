import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Pomocná funkcia na navigáciu v menu
def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    handle = int(sys.argv[1])
    arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
    params = dict(urllib.parse.parse_qsl(arg_string))

    # HLAVNÉ MENU (zobrazí sa hneď po otvorení)
    if not params:
        kategorie = [
            {"label": "Relácie", "mode": "relacie"},
            {"label": "Logistika", "mode": "logistika"},
            {"label": "Filmy", "mode": "filmy"}
        ]

        for kat in kategorie:
            li = xbmcgui.ListItem(label="[B]" + kat["label"] + "[/B]")
            url = build_url({'mode': kat['mode']})
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        
        xbmcplugin.endOfDirectory(handle)

    # SEKCIE (čo sa stane po kliknutí)
    else:
        mode = params.get('mode')
        oznam = "Už čoskoro pripravujeme..."
        
        # Vytvoríme jednoduchý riadok s informáciou
        if mode == 'relacie':
            li = xbmcgui.ListItem(label="[I]Relácie - " + oznam + "[/I]")
        elif mode == 'logistika':
            li = xbmcgui.ListItem(label="[I]Logistika - " + oznam + "[/I]")
        elif mode == 'filmy':
            li = xbmcgui.ListItem(label="[I]Filmy - " + oznam + "[/I]")
        
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()

