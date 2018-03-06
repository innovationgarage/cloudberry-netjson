import netjsonconfig
import netjsonconfig.backends.openwrt.converters.base

import json
from collections import OrderedDict


class ZoneConverter(netjsonconfig.backends.base.converter.BaseConverter):
    netjson_key = 'zones'
    intermediate_key = 'firewall'

    def to_intermediate_loop(self, block, result, index=None):        
        result.setdefault('firewall', [])
        rule = dict(block)
        rule['.type'] = 'zone'
        rule['.name'] = rule['name']
        if 'network' in rule: rule['network'] = ' '.join(rule['network'])
        result['firewall'].append(rule)
        return result

    def should_skip_block(self, block):
        return block.get(".type") != 'zone'

    def to_netjson_loop(self, block, result, index=None):
        result.setdefault('zones', [])
        block.pop(".type")
        block.pop(".name")
        if 'network' in block: block['network'] = block['network'].split(" ")
        result['zones'].append(block)
        return result
    
class ForwardingConverter(netjsonconfig.backends.base.converter.BaseConverter):
    netjson_key = 'forwarding'
    intermediate_key = 'firewall'

    def to_intermediate_loop(self, block, result, index=None):
        result.setdefault('firewall', [])
        rule = dict(block)
        rule['.type'] = 'forwarding'
        rule['.name'] = "%(src)s_%(dest)s" % rule
        result['firewall'].append(rule)
        return result

    def should_skip_block(self, block):
        return block.get(".type") != 'forwarding'

    def to_netjson_loop(self, block, result, index=None):
        result.setdefault('forwarding', [])
        block.pop(".type")
        block.pop(".name")
        result['forwarding'].append(block)
        return result
    
class ContainerConverter(netjsonconfig.backends.base.converter.BaseConverter):
    netjson_key = 'containers'
    intermediate_key = 'containers'

    def to_intermediate_loop(self, block, result, index=None):
        result.setdefault('containers', [])
        rule = dict(block)
        rule['.type'] = 'container'
        rule['.name'] = rule['uuid']
        if 'ports' in rule:
            rule['ports'] = [
                "%s/%s: %s" % (
                    port.get('host', port.get("guest")),
                    port.get("proto", "tcp"),
                    port.get("guest"))
                for port in rule['ports']]
        result['containers'].append(rule)
        return result

    def to_netjson_loop(self, block, result, index=None):
        result.setdefault('containers', [])
        block.pop(".type")
        block.pop(".name")
        if 'ports' in block:
            def parse_port(port):
                host, guest = port.split(": ")
                host, proto = host.split("/")
                return {"host": int(host),
                        "guest": int(guest),
                        "proto": proto} 
            block['ports'] = [parse_port(port) for port in block['ports']]
        result['containers'].append(block)
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
            "container-port": {
                "type": "object",
                "properties": {
                    "host": {"type": "integer"},
                    "guest": {"type": "integer"},
                    "proto": {"type": "string", "enum": ["tcp", "udp"]}
                }
            },
            "container": {
                "type": "object",
                "properties": {
                    "uuid": {"type": "string"},
                    "key": {"type": "string"},
                    "image": {"type": "string"},
                    "ports": {
                        "type": "array",
                        "items": { "$ref": "#/definitions/container-port" }
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
    converters = [ZoneConverter, ForwardingConverter, ContainerConverter] + netjsonconfig.OpenWrt.converters
    
