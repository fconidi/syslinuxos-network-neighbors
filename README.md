# SysLinuxOS Network Neighbors

Graphical viewer for the network device directly connected to each of this computer's interfaces. It shows the local interface, device name, remote port, protocol and available LLDP details. The app reads `lldpcli`; it does not change network settings.

The interface follows the desktop language in English, Italian, French, German and Spanish.

## Requirements

Installing this package also installs `lldpd` on SysLinuxOS 13 or Debian 13. Its service may start and announce this computer. To receive LLDP without announcing the computer, set `DAEMON_ARGS="-r"` in `/etc/default/lldpd` and restart `lldpd.service`. Consult your network policy before enabling it.

The package does not change the daemon configuration. If the daemon is unavailable, the window shows a status message. If access to the `lldpd` control socket is restricted, the app requests desktop authorization and uses a helper that runs only the fixed read-only neighbor query.

## Use

Open **SysLinuxOS Network Neighbors** from **Networking** or **SysLinuxOS Tools**, or run `syslinuxos-network-neighbors`. Select a row for details and use **Refresh** to read the current neighbor list. An empty list can mean that the connected switch does not send LLDP, the cable is disconnected, or no announcement has arrived yet. The app shows directly connected devices; it does not map the whole network.

## Build

Run `./build-deb.sh OUTPUT_DIRECTORY` and install the resulting `.deb` with APT.

Copyright 2026 Franco Conidi. Licensed under GPL-3.0-only.
