# Custom Simple Netbox Inventory Plugin

This Inventory plugin was developed for a friend, and it is a quite opinionated simple version of the ansible netbox inventory plugin
to return only the needed values for a faster inventory result

- Device Role filtering
- Support removal of domain names
- Custom tag prefix
- Site filtering

## Usage

- Copy **ansible/inventory_plugins/an_netbox.py** in your custom inventory_plugins directory
- Create a new **an_netbox_inventory.yml** in your inventory folder like /ansible/inventory/an_netbox_inventory.yml

  ```yaml
  plugin: an_netbox
  netbox_server_url: http://10.0.0.110:8080
  netbox_api_key: 7a096c1182f928637a6441c23119ecee042439b2
  # device_role slug to filter, if not defined it will be 'server
  device_role: server
  # if not defined it tag_prefx will be 'tag_'
  tag_prefix: "tag_"
  # if true it will cutout the domainname and pass only ansiblehost=<device_name>
  cut_domain_name: true
  # filter out a specific webfaction_site
  filter_site: Interxion
  ```

- Ensure inventoryplug is enabled in your ansible.cfg

  ```ini
  [inventory]
  enable_plugins = an_netbox
  ```

## Propertys

### netbox_server_url - **Required**

Url to connect to netbox api

### netbox_api_key - **Required**

API Key to use for the autorization

### device_role

Device Role to filter for ( Slug Name)

Device Role typical in a Netbox Installation

- access-switch
- console-server
- core-switch
- distribution-switch
- firewall
- management-switch
- pdu
- router
- server

> **Default:** server

### tag_prefix

Host Group Prefix for each device tag

> **Default:** tag_

### cut_domain_name

Cut out Domains from device name

> linux1.test.com will be linux1

> **Default:** True

### filter_site

Will filter devices of a specific site

> If not defined it will return all netbox devices and virtualmachines