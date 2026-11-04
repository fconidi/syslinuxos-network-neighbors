import json
import unittest

from backend import NeighborError, parse_neighbors, read_neighbors


SAMPLE = {"lldp": [{"interface": [
    {"name": "enp2s0", "via": "LLDP", "chassis": [{"name": [{"value": "switch-a"}], "id": [{"value": "aa:bb:cc:dd:ee:ff"}], "mgmt-ip": [{"value": "192.0.2.10"}]}],
     "port": [{"id": [{"value": "Gi1/0/24"}], "descr": [{"value": "Desk 12"}]}],
     "vlan": [{"vlan-id": "1", "pvid": True}, {"vlan-id": "20", "pvid": False}]},
    {"name": "enp3s0", "via": "LLDP", "chassis": [{"id": [{"value": "11:22:33:44:55:66"}]}],
     "port": [{"id": [{"value": "Ethernet1"}]}]},
]}]}


class BackendTests(unittest.TestCase):
    def test_parses_neighbors_and_fallback_name(self):
        rows = parse_neighbors(json.dumps(SAMPLE))
        self.assertEqual(len(rows), 2)
        self.assertEqual((rows[0].local_interface, rows[0].name, rows[0].remote_port),
                         ("enp2s0", "switch-a", "Gi1/0/24"))
        self.assertEqual(rows[0].management_ip, "192.0.2.10")
        self.assertEqual(rows[0].vlan_pvid, "1")
        self.assertEqual(rows[1].name, "11:22:33:44:55:66")
        self.assertEqual(rows[1].vlan_pvid, "")

    def test_empty_and_malformed_data(self):
        self.assertEqual(parse_neighbors('{"lldp":[]}'), [])
        with self.assertRaises(NeighborError):
            parse_neighbors('{bad')

    def test_read_uses_fixed_command_and_reports_failure(self):
        seen = []
        def runner(argv, **kwargs):
            seen.append((argv, kwargs))
            return type("Result", (), {"returncode": 1, "stdout": "", "stderr": "socket unavailable"})()
        with self.assertRaises(NeighborError):
            read_neighbors(runner=runner)
        self.assertEqual(seen[0][0], ["/usr/sbin/lldpcli", "-f", "json0", "show", "neighbors", "details"])
        self.assertEqual(seen[0][1]["timeout"], 8)

    def test_permission_denied_uses_read_only_helper(self):
        seen = []
        def runner(argv, **kwargs):
            seen.append(argv)
            if len(seen) == 1:
                return type("Result", (), {"returncode": 1, "stdout": "", "stderr": "Permission denied"})()
            return type("Result", (), {"returncode": 0, "stdout": json.dumps(SAMPLE), "stderr": ""})()
        self.assertEqual(len(read_neighbors(runner=runner)), 2)
        self.assertEqual(seen[1], ["/usr/bin/pkexec", "/usr/lib/syslinuxos-network-neighbors/read-helper"])

    def test_permission_error_uses_read_only_helper(self):
        seen = []
        def runner(argv, **kwargs):
            seen.append(argv)
            if len(seen) == 1:
                raise PermissionError(13, "Permission denied", argv[0])
            return type("Result", (), {"returncode": 0, "stdout": '{"lldp":[]}', "stderr": ""})()
        self.assertEqual(read_neighbors(runner=runner), [])
        self.assertEqual(seen[1], ["/usr/bin/pkexec", "/usr/lib/syslinuxos-network-neighbors/read-helper"])


if __name__ == "__main__":
    unittest.main()
