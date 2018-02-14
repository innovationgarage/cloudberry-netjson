# cloudberry-netjson

Extra nejson format for OpenWRT firewall config for django-netjsonconfig

Add 

    NETJSONCONFIG_BACKENDS = (
        ('dualog_netjson.OpenWrt', 'OpenWRT/Dualog'),
        ('netjsonconfig.OpenWrt', 'OpenWRT/LEDE'),
        ('netjsonconfig.OpenWisp', 'OpenWISP Firmware 1.x'))

to settings.py in Django.
