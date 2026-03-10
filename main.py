import sys
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon

# Načítanie doplnku a nastavení
addon = xbmcaddon.Addon()

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    # Načítanie údajov z nastavení (resources/settings.xml)
    user_email = addon.getSetting('email')
    user_password = addon.getSetting('password')

    # --- KONTROLA PRIHLÁSENIA ---
    if user_email == "Admin" and user_password == "Kanianka8":
        # Ak sú údaje správne, pokračujeme do menu
        rozcestnik()
    else:
        # Ak sú údaje nesprávne
        xbmcgui.Dialog().ok('Flow play', 'Nesprávne prihlasovacie údaje!\nZadajte: Admin / Kanianka8')
        return

def rozcestnik():
    handle = int(sys.argv[1])
    arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
    params = dict(urllib.parse.parse_qsl(arg_string))

    # --- HLAVNÉ MENU ---
    if not params:
        kategorie = [
            {"label": "[B]Relácie[/B]", "mode": "relacie"},
            {"label": "[B]Logistika[/B]", "mode": "logistika"},
            {"label": "[B]Filmy[/B]", "mode": "filmy"}
        ]

        for kat in kategorie:
            li = xbmcgui.ListItem(label=kat["label"])
            url = build_url({'mode': kat["mode"]})
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        
        xbmcplugin.endOfDirectory(handle)

    # --- SEKCIA RELÁCIE ---
    elif params.get('mode') == 'relacie':
        xbmcgui.Dialog().notification('Flow play', 'Už čoskoro pripravujeme...', xbmcgui.NOTIFICATION_INFO, 5000)
        li = xbmcgui.ListItem(label="[I]Relácie - Už čoskoro pripravujeme[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- SEKCIA LOGISTIKA ---
    elif params.get('mode') == 'logistika':
        xbmcgui.Dialog().notification('Flow play', 'Už čoskoro pripravujeme...', xbmcgui.NOTIFICATION_INFO, 5000)
        li = xbmcgui.ListItem(label="[I]Logistika - Už čoskoro pripravujeme[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- SEKCIA FILMY ---
    elif params.get('mode') == 'filmy':
        xbmcgui.Dialog().notification('Flow play', 'Filmy pripravujeme...', xbmcgui.NOTIFICATION_INFO, 5000)
        li = xbmcgui.ListItem(label="[I]Filmy pripravujeme...[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
