import cloudberry_netjson
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
        "containers": [
            {
                "uuid": "abc123",
                "key": "123abc",
                "ports": [{"host": 4711, "guest": 4712, "proto": "tcp"},
                          {"host": 4713, "guest": 4713, "proto": "tcp"}]
            },
            {
                "uuid": "abc123",
                "key": "123abc",
                "image": "openwrt-lede"
            }
        ]
    }

    def test_zone(self):
        parsed = json.loads(cloudberry_netjson.OpenWrt(
            native=cloudberry_netjson.OpenWrt(self.zone_json).generate()
        ).json())
        assert parsed == self.zone_json
        
    def test_forwarding(self):
        parsed = json.loads(cloudberry_netjson.OpenWrt(
            native=cloudberry_netjson.OpenWrt(self.forwarding_json).generate()
        ).json())
        assert parsed == self.forwarding_json

    def test_container(self):
        parsed = json.loads(cloudberry_netjson.OpenWrt(
            native=cloudberry_netjson.OpenWrt(self.container_json).generate()
        ).json())
        assert parsed == self.container_json
