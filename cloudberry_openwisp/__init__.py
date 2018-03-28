import requests
import io
import netjsonconfig
import cloudberry_netjson
import json
import os.path

class Config(object):
    def __init__(self, path, base_url=None, uuid=None, key=None):
        self.path = path
        self.config = {
            "base_url": base_url,
            "uuid": uuid,
            "key": key
        }
        
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.config = json.load(f)
        elif base_url is not None:
            with open(self.path, "w") as f:
                json.dump(self.config, f)
                 
    @property
    def base_url(self):
        return self.config['base_url']

    @property
    def uuid(self):
        return self.config['uuid']

    @property
    def key(self):
        return self.config['key']

    def update(self):
        r = requests.get("%s/controller/checksum/%s/?key=%s" % (self.base_url, self.uuid, self.key))
        checksum = r.content.decode("utf-8")
        if 'data' in self.config and self.config['data']['checksum'] == checksum:
            return
        data = {"checksum": checksum, "config": {}}
        
        r = requests.get("%s/controller/download-config/%s/?key=%s" % (self.base_url, self.uuid, self.key))

        data['config'] = json.loads(cloudberry_netjson.OpenWrt(native=io.BytesIO(r.content)).json())
        
        self.config['data'] = data
        with open(self.path, "w") as f:
            json.dump(self.config, f)
                    
    def report_status(self, status):
        r = requests.post("%s/controller/report-status/%s/" % (self.base_url, self.uuid),
                          data = {"key": self.key, "status": status})
