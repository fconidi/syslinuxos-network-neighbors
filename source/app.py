#!/usr/bin/python3
"""Graphical viewer for directly connected LLDP neighbors."""

import threading

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

from backend import NeighborError, read_neighbors
from i18n import choose_language, tr


class NeighborWindow(Gtk.Window):
    def __init__(self, reader=read_neighbors, language=None):
        self.language = language or choose_language()
        self.reader = reader
        self.rows = []
        super().__init__(title=tr(self.language, "title"))
        self.set_default_size(880, 530)
        self.set_border_width(20)

        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        self.add(layout)

        heading = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        layout.pack_start(heading, False, False, 0)
        titles = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        heading.pack_start(titles, True, True, 0)
        title = Gtk.Label(label=tr(self.language, "title"), xalign=0)
        title.get_style_context().add_class("title")
        titles.pack_start(title, False, False, 0)
        subtitle = Gtk.Label(label=tr(self.language, "subtitle"), xalign=0)
        subtitle.set_line_wrap(True)
        titles.pack_start(subtitle, False, False, 0)
        self.refresh_button = Gtk.Button.new_with_label(tr(self.language, "refresh"))
        self.refresh_button.connect("clicked", self.refresh)
        heading.pack_end(self.refresh_button, False, False, 0)

        self.status = Gtk.Label(xalign=0)
        self.status.set_line_wrap(True)
        layout.pack_start(self.status, False, False, 0)

        self.model = Gtk.ListStore(int, str, str, str, str, str)
        tree = Gtk.TreeView(model=self.model)
        tree.set_headers_visible(True)
        tree.set_hexpand(True)
        tree.set_vexpand(True)
        for index, key in enumerate(("interface", "device", "port", "vlan_pvid", "protocol"), start=1):
            cell = Gtk.CellRendererText()
            cell.set_property("ellipsize", 3)
            column = Gtk.TreeViewColumn(tr(self.language, key), cell, text=index)
            column.set_resizable(True)
            column.set_expand(index == 2)
            tree.append_column(column)
        self._selection = tree.get_selection()
        self._selection.connect("changed", self.on_selection_changed)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(tree)
        layout.pack_start(scroll, True, True, 0)

        details_frame = Gtk.Frame(label=tr(self.language, "details"))
        layout.pack_start(details_frame, False, False, 0)
        grid = Gtk.Grid(column_spacing=16, row_spacing=7, margin=12)
        details_frame.add(grid)
        self.detail_values = {}
        for row, key in enumerate(("port_description", "vlan_pvid", "chassis_id", "management_ip")):
            label = Gtk.Label(label=tr(self.language, key), xalign=0)
            value = Gtk.Label(label=tr(self.language, "none"), xalign=0)
            value.set_selectable(True)
            value.set_line_wrap(True)
            grid.attach(label, 0, row, 1, 1)
            grid.attach(value, 1, row, 1, 1)
            self.detail_values[key] = value

        note = Gtk.Label(label=tr(self.language, "read_only"), xalign=0)
        note.set_line_wrap(True)
        note.get_style_context().add_class("dim-label")
        layout.pack_start(note, False, False, 0)
        self.refresh()

    def on_selection_changed(self, selection):
        model, iterator = selection.get_selected()
        neighbor = self.rows[model[iterator][0]] if iterator is not None else None
        for key, widget in self.detail_values.items():
            value = getattr(neighbor, key) if neighbor else ""
            widget.set_text(value or tr(self.language, "none"))

    def refresh(self, _button=None):
        self.refresh_button.set_sensitive(False)
        self.status.set_text(tr(self.language, "scanning"))
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        try:
            rows, error = self.reader(), None
        except NeighborError as exc:
            rows, error = [], str(exc)
        GLib.idle_add(self._show_result, rows, error)

    def _show_result(self, rows, error):
        self.rows = rows
        self.model.clear()
        for index, neighbor in enumerate(rows):
            self.model.append((index, neighbor.local_interface, neighbor.name,
                               neighbor.remote_port, neighbor.vlan_pvid or tr(self.language, "none"),
                               neighbor.protocol))
        self.on_selection_changed(self._selection)
        self.status.set_text(tr(self.language, error) if error else
                             tr(self.language, "found", count=len(rows)) if rows else
                             tr(self.language, "empty"))
        self.refresh_button.set_sensitive(True)
        return GLib.SOURCE_REMOVE


def main():
    window = NeighborWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
