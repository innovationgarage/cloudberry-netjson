import dualog_netjson
import json

class Tests(object):
    zone_json = {
        'type': 'DeviceConfiguration',
        "zones": [{
            "name": "MyZone",
            "devize": "eth0",
            "network": ["lan", "wan"],
            "output": "ACCEPT",
            "input": "ACCEPT",
            "forward": "ACCEPT",
            "masq": "1"
        }]
    }
    forwarding_json = {
        'type': 'DeviceConfiguration',
        "forwarding": [{
            "src": "lan",
            "dest": "was"
        }]
    }
    container_json = {
        'type': 'DeviceConfiguration',
        "containers": [{
            "uuid": "abc123",
            "key": "123abc",
            "ports": [4711, 4712]
        }]
    }

    def test_zone(self):
        parsed = json.loads(dualog_netjson.OpenWrt(
            native=dualog_netjson.OpenWrt(self.zone_json).generate()
        ).json())
        assert parsed == self.zone_json
        
    def test_forwarding(self):
        parsed = json.loads(dualog_netjson.OpenWrt(
            native=dualog_netjson.OpenWrt(self.forwarding_json).generate()
        ).json())
        assert parsed == self.forwarding_json

    def test_container(self):
        parsed = json.loads(dualog_netjson.OpenWrt(
            native=dualog_netjson.OpenWrt(self.container_json).generate()
        ).json())
        assert parsed == self.container_json
