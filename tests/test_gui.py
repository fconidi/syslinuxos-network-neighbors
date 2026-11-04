import time
import unittest

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from app import NeighborWindow
from backend import Neighbor


@unittest.skipUnless(Gtk.init_check()[0], "GTK display unavailable")
class WindowTests(unittest.TestCase):
    def test_neighbor_is_visible_with_details(self):
        sample = Neighbor("enp2s0", "switch-a", "Gi1/0/24", "Desk 12",
                          "aa:bb:cc:dd:ee:ff", "192.0.2.10", "LLDP", "1")
        window = NeighborWindow(reader=lambda: [sample], language="it")
        window.show_all()
        until = time.monotonic() + 3
        while not window.refresh_button.get_sensitive() and time.monotonic() < until:
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)
            time.sleep(0.01)
        self.assertTrue(window.refresh_button.get_sensitive())
        self.assertEqual(window.status.get_text(), "Vicini trovati: 1")
        self.assertEqual(window.model[0][1:4], ["enp2s0", "switch-a", "Gi1/0/24"])
        self.assertEqual(window.model[0][4], "1")
        window._selection.select_path(0)
        self.assertEqual(window.detail_values["vlan_pvid"].get_text(), "1")
        self.assertEqual(window.detail_values["management_ip"].get_text(), "192.0.2.10")
        window.destroy()


if __name__ == "__main__":
    unittest.main()
