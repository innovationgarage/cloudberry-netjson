import netjsonconfig
import netjsonconfig.backends.openwrt.converters.base

import json
from collections import OrderedDict


class ZoneConverter(netjsonconfig.backends.openwrt.converters.base.OpenWrtConverter):
    netjson_key = 'zones'

    def to_intermediate_loop(self, block, result, index=None):        
        result.setdefault('firewall', [])
        rule = dict(block)
        rule['.type'] = 'zone'
        rule['.name'] = rule['name']
        if 'network' in rule: rule['network'] = ' '.join(rule['network'])
        result['firewall'].append(rule)
        return result

class ForwardingConverter(netjsonconfig.backends.openwrt.converters.base.OpenWrtConverter):
    netjson_key = 'forwarding'

    def to_intermediate_loop(self, block, result, index=None):
        result.setdefault('firewall', [])
        rule = dict(block)
        rule['.type'] = 'forwarding'
        rule['.name'] = "%(src)s_%(dest)s" % rule
        result['firewall'].append(rule)
        return result

class ContainerConverter(netjsonconfig.backends.openwrt.converters.base.OpenWrtConverter):
    netjson_key = 'containers'

    def to_intermediate_loop(self, block, result, index=None):
        result.setdefault('containers', [])
        rule = dict(block)
        rule['.type'] = 'container'
        rule['.name'] = "%(uuid)s" % rule
        result['containers'].append(rule)
        return result

class OpenWrt(netjsonconfig.OpenWrt):
    schema = netjsonconfig.utils.merge_config(netjsonconfig.OpenWrt.schema, {
        "definitions": {
            "zone": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "device": {"type": "string"},
                    "network": {"type": "array", "items": {"type": "string"}},
                    "output": {"type": "string", "enum": ["ACCEPT", "DENY"]},
                    "input": {"type": "string", "enum": ["ACCEPT", "DENY"]},
                    "forward": {"type": "string", "enum": ["ACCEPT", "DENY"]},
                    "masq": {"type": "string", "enum": ["1", "0"]},
                }
            },
            "forwarding": {
                "type": "object",
                "properties": {
                    "src": {"type": "string"},
                    "dest": {"type": "string"}
                }
            },
            "container": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string"},
                    "key": {"type": "string"},
                    "ports": {
                        "type": "array",
                        "items": {"type": "integer"}
                    }
                }
            }
        },
        "properties": {
            "zones": {
                "type": "array",
                "title": "Zones",
                "items": { "$ref": "#/definitions/zone" }
            },
            "forwarding": {
                "type": "array",
                "title": "Forwarding",
                "items": { "$ref": "#/definitions/forwarding" }
            },
            "containers": {
                "type": "array",
                "title": "Containers",
                "items": { "$ref": "#/definitions/container" }
            }
        }
    })
    converters = netjsonconfig.OpenWrt.converters + [ZoneConverter, ForwardingConverter, ContainerConverter]
    
