# Fill up Netbox Service with Demo data
# 100 Windows Servers
# 100 Linux Servers

import pynetbox
import json
import sys

nb = pynetbox.api('http://192.168.99.20:80', token='7a096c1182f928637a6441c23119ecee042439b2')

def ensure_device_type(device_type, model, manufacturer, slug):
  dts = nb.dcim.device_types.filter(name=device_type)

  if dts:
    return dts[0]
  else:
    mfs = nb.dcim.manufacturers.filter(name=manufacturer)
    if mfs[0]:
      nb.dcim.device_types.create(
        name=device_type,
        model=model,
        slug=slug,
        manufacturer=mfs[0].id
      )
      return nb.cim.device_types.filter(name=device_type)[0]
    else:
      sys.exit('could not found manufactorer ', manufacturer)

def ensure_site(site_name):
  sites = nb.dcim.sites.filter(name=site_name)
  if sites:
    return sites[0]
  else:
    nb.dcim.sites.create(name="Interxion",slug=desired_site.lower())
    sites = nb.dcim.sites.filter(name=site_name)
    if sites:
      return sites[0]

def get_device_role_id(device_role):
  device_roles = nb.dcim.device_roles.filter(name=device_role)
  if(device_roles):
    return device_roles[0]
  else:
    return None

desired_site="Interxion"
site = ensure_site(desired_site)

server_dt = ensure_device_type('HP DL380 G10','DL380G10','HP','hp_dl380_g10')
server_device_role = get_device_role_id('Server')

windows_servers = []
for x in range(0, 100):
  windows_servers.append({
    "name": ("win-srv-" + str(x)),
    "device_role": server_device_role.id,
    "device_type": server_dt.id,
    "site": site.id,
    "tags": ["windows","update"]
  })

linux_servers = []
for x in range(0, 100):
  linux_servers.append({
    "name": ("linux-" + str(x)),
    "device_role": server_device_role.id,
    "device_type": server_dt.id,
    "site": site.id,
    "tags": ["linux","update"]
  })

nb.dcim.devices.create(windows_servers)
nb.dcim.devices.create(linux_servers)