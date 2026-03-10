import sys
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon

# Načítanie doplnku a jeho nastavení
addon = xbmcaddon.Addon()

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    # 1. NAČÍTANIE ÚDAJOV Z NASTAVENÍ (vytvoril si v resources/settings.xml)
    user_name = addon.getSetting('email')
    user_pass = addon.getSetting('password')

    # 2. KONTROLA ADMINA
    if user_name == "Admin" and user_pass == "Kanianka8":
        # Ak je meno a heslo správne, otvoríme menu
        zobraz_menu()
    else:
        # Ak sú údaje prázdne alebo zlé, ukážeme chybu
        xbmcgui.Dialog().ok('Flow play', 'Prístup zamietnutý!\nZadajte správne údaje v nastaveniach.\n\nMeno: Admin\nHeslo: Kanianka8')
        # Otvorí nastavenia automaticky, aby to mal používateľ ľahšie
        addon.openSettings()
        return

def zobraz_menu():
    handle = int(sys.argv[1])
    arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
    params = dict(urllib.parse.parse_qsl(arg_string))

    # --- HLAVNÁ OBRAZOVKA DOPLNKU ---
    if not params:
        kategorie = [
            {"label": "Relácie", "mode": "relacie"},
            {"label": "Logistika", "mode": "logistika"},
            {"label": "Filmy", "mode": "filmy"}
        ]

        for kat in kategorie:
            # Vytvorenie položky v zozname
            li = xbmcgui.ListItem(label="[B]" + kat["label"] + "[/B]")
            url = build_url({'mode': kat['mode']})
            # True znamená, že ide o priečinok (otvorí ďalšiu úroveň)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        
        xbmcplugin.endOfDirectory(handle)

    # --- SEKCIA RELÁCIE ---
    elif params.get('mode') == 'relacie':
        xbmcgui.Dialog().notification('Flow play', 'Už čoskoro pripravujeme...', xbmcgui.NOTIFICATION_INFO, 4000)
        li = xbmcgui.ListItem(label="[I]Relácie - Už čoskoro pripravujeme[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- SEKCIA LOGISTIKA ---
    elif params.get('mode') == 'logistika':
        xbmcgui.Dialog().notification('Flow play', 'Už čoskoro pripravujeme...', xbmcgui.NOTIFICATION_INFO, 4000)
        li = xbmcgui.ListItem(label="[I]Logistika - Už čoskoro pripravujeme[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- SEKCIA FILMY ---
    elif params.get('mode') == 'filmy':
        xbmcgui.Dialog().notification('Flow play', 'Filmy pripravujeme...', xbmcgui.NOTIFICATION_INFO, 4000)
        li = xbmcgui.ListItem(label="[I]Filmy pripravujeme...[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()


