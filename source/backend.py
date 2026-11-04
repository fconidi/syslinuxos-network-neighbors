"""Read the local LLDP daemon without changing its configuration."""

from dataclasses import dataclass
import json
import subprocess


class NeighborError(Exception):
    pass


@dataclass(frozen=True)
class Neighbor:
    local_interface: str
    name: str
    remote_port: str
    port_description: str
    chassis_id: str
    management_ip: str
    protocol: str
    vlan_pvid: str


def _items(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    return []


def _first_text(value):
    if isinstance(value, str):
        return value.strip()
    for item in _items(value):
        if isinstance(item, dict):
            result = _first_text(item.get("value", ""))
            if result:
                return result
    return ""


def parse_neighbors(output):
    try:
        document = json.loads(output)
    except (ValueError, TypeError) as exc:
        raise NeighborError("invalid_data") from exc
    if not isinstance(document, dict) or not isinstance(document.get("lldp"), (list, dict)):
        raise NeighborError("invalid_data")

    rows = []
    for group in _items(document["lldp"]):
        if not isinstance(group, dict):
            continue
        for interface in _items(group.get("interface")):
            if not isinstance(interface, dict):
                continue
            chassis = next((v for v in _items(interface.get("chassis")) if isinstance(v, dict)), {})
            port = next((v for v in _items(interface.get("port")) if isinstance(v, dict)), {})
            chassis_id = _first_text(chassis.get("id"))
            vlan_pvid = next((
                _first_text(vlan.get("vlan-id"))
                for vlan in _items(interface.get("vlan"))
                if isinstance(vlan, dict) and vlan.get("pvid") in (True, "yes")
            ), "")
            rows.append(Neighbor(
                local_interface=_first_text(interface.get("name")),
                name=_first_text(chassis.get("name")) or chassis_id,
                remote_port=_first_text(port.get("id")),
                port_description=_first_text(port.get("descr")),
                chassis_id=chassis_id,
                management_ip=_first_text(chassis.get("mgmt-ip")),
                protocol=_first_text(interface.get("via")),
                vlan_pvid=vlan_pvid,
            ))
    return sorted(rows, key=lambda row: (row.local_interface, row.name, row.remote_port))


def read_neighbors(runner=subprocess.run):
    argv = ["/usr/sbin/lldpcli", "-f", "json0", "show", "neighbors", "details"]
    permission_denied = False
    try:
        result = runner(argv, capture_output=True, text=True, timeout=8, check=False)
    except FileNotFoundError as exc:
        raise NeighborError("not_installed") from exc
    except PermissionError:
        permission_denied = True
        result = None
    except subprocess.TimeoutExpired as exc:
        raise NeighborError("timeout") from exc
    if permission_denied or (result.returncode and "permission denied" in result.stderr.lower()):
        try:
            result = runner(["/usr/bin/pkexec", "/usr/lib/syslinuxos-network-neighbors/read-helper"],
                            capture_output=True, text=True, timeout=90, check=False)
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            raise NeighborError("authorization_failed") from exc
        if result.returncode:
            raise NeighborError("authorization_failed")
    if result.returncode:
        raise NeighborError("daemon_unavailable")
    return parse_neighbors(result.stdout)
