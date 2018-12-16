# Custom Simple Netbox Inventory Plugin

This Inventory plugin was developed for a friend, and it is a quite opinionated simple version of the ansible netbox inventory plugin
to return only the needed values for a faster inventory result

- Support removal of domain names
- custom tag prefix
- site filtering

## Usage

- Copy an_netbox.py in your custom inventory_plugins directory
- Create a new inventory.yml in your inventory folder

```yaml
plugin: an_netbox
netbox_server_url: http://10.0.0.110:8080
netbox_api_key: 7a096c1182f928637a6441c23119ecee042439b2
# if not defined it tag_prefx will be 'tag_'
tag_prefix: "tag_"
# if true it will cutout the domainname and pass only ansiblehost=<device_name>
cut_domain_name: true
# filter out a specific webfaction_site
filter_site: Interxion
```

## Propertys

### netbox_server_url - **Required**

Url to connect to netbox api

### netbox_api_key - **Required**

API Key to use for the autorization

### tag_prefix

Host Group Prefix for each device tag

> **Default:** tag_

### cut_domain_name

Cut out Domains from device name

> linux1.test.com will be linux1

> **Default:** True

### filter_site

Will filter devices of a specific site

if not defined it will return all netbox devices