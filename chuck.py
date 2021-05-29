import gi
import signal
import json
import urllib.request
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3
from gi.repository import Notify as notify

APPINDICATOR_ID = 'cndbappindicator'

def main():
    indicator = AppIndicator3.Indicator.new(
            APPINDICATOR_ID,
            "network-idle-symbolic",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_joke = gtk.MenuItem(label='Joke')
    item_joke.connect('activate', joke)
    menu.append(item_joke)
    item_geoip = gtk.MenuItem(label='Geoip')
    item_quit = gtk.MenuItem(label='Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def fetch_joke():
    request = urllib.request.Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
    response = urllib.request.urlopen(request)
    joke = json.loads(response.read())['value']['joke']
    return joke

def joke(_):
    notify.Notification.new("Joke", fetch_joke(), None).show()


def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
