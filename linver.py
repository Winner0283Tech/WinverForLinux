#!/usr/bin/env python3

import gi
import platform
import os
import datetime
import subprocess

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk


def get_os_info():
    info = {}
    with open("/etc/os-release") as f:
        for l in f:
            if "=" in l:
                k, v = l.strip().split("=", 1)
                info[k] = v.strip('"')
    return info


def cmd_output(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().splitlines()[0]
    except Exception:
        return "unbekannt"


class Linver(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.linver.app")

    def do_activate(self):
        os_info = get_os_info()
        year = datetime.datetime.now().year

        shell = os.path.basename(os.environ.get("SHELL", "unbekannt"))
        shell_version = cmd_output([shell, "--version"])
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "unbekannt")
        session = os.environ.get("XDG_SESSION_TYPE", "unbekannt")

        win = Gtk.ApplicationWindow(application=self)
        win.set_title("Über Linux")
        win.set_default_size(520, 360)
        win.set_resizable(False)

        Gtk.Settings.get_default().set_property(
            "gtk-application-prefer-dark-theme", True
        )

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        root.set_margin_top(12)
        root.set_margin_bottom(12)
        root.set_margin_start(12)
        root.set_margin_end(12)
        win.set_child(root)

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        root.append(header)

        #Custom App-Logo
        logo = Gtk.Image.new_from_icon_name(os_info.get("LOGO", "computer"))
        logo.set_pixel_size(64)
        header.append(logo)

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header.append(title_box)

        title = Gtk.Label()
        title.set_markup("<b>Linux-Version</b>")
        title.set_xalign(0)
        title_box.append(title)

        subtitle = Gtk.Label(label=f"{os_info.get('NAME')} {os_info.get('VERSION')}")
        subtitle.set_xalign(0)
        title_box.append(subtitle)

        # Body text
        body_text = (
            f"Kernel: {platform.release()}\n"
            f"Architektur: {platform.machine()}\n"
            f"Build-ID: {os_info.get('BUILD_ID', 'n/a')}\n"
            f"Hostname: {platform.node()}\n"
            f"Benutzer: {os.environ.get('USER', 'unbekannt')}\n"
            f"Desktop: {desktop}\n"
            f"Session: {session}\n"
            f"Shell: {shell}\n"
            f"Shell-Version: {shell_version}\n"
            f"Python: {platform.python_version()}\n\n"
            f"© {year} {os_info.get('NAME')}. All rights reserved."
        )

        body = Gtk.Label(label=body_text)
        body.set_xalign(0)
        body.set_wrap(True)
        root.append(body)

        root.append(Gtk.Separator())

        # Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        root.append(btn_box)

        copy_btn = Gtk.Button(label="Copy information")
        copy_btn.connect(
            "clicked",
            lambda *_: Gdk.Display.get_default()
            .get_clipboard()
            .set(body_text),
        )
        btn_box.append(copy_btn)

        btn_box.append(Gtk.Box())

        ok = Gtk.Button(label="OK")
        ok.connect("clicked", lambda *_: win.close())
        btn_box.append(ok)

        win.present()


app = Linver()
app.run()
