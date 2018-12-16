# Custom Netbox Inventory Plugin for Antares Netlogix
# Made with Love from David Baumann(Github: daBONDi)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import logging
import json

try:
    import pynetbox
    HAS_PYNETBOX = True
except:
    HAS_PYNETBOX = False

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = 'an_netbox'

    def __init__(self):
        super(InventoryModule, self).__init__()

        self.config_data = None
        self.netbox_server_url = None
        self.netbox_api_key = None
        self.netbox = None
        self.tag_prefix = None
        self.cut_domain_name = True
        self.filter_site = None

    def _get_unique_tags(self, devices):
        """
        Return unique tag list of all devices
        :param devices:
        :return: tags[]
        """
        tag_list = []
        for device in devices:
            for tag in device.tags:
                if tag not in tag_list:
                    tag_list.append("tag_" + tag)
        return tag_list

    def _cut_domain_name(self, device_name):
        if device_name.find('.'):
            return device_name.split('.')[0]
        else:
            return device_name

    def _populate(self, devices):

        # Generate Ansible Group based on Tags
        for tag in self._get_unique_tags(devices):
            self.inventory.add_group(tag)

        # Add Hosts
        for device in devices:
            if self.cut_domain_name:
                host = self._cut_domain_name(device.name)
            else:
                host = device.name

            # Add Ansible Host Object
            self.inventory.add_host(host)

            # set ansible_host variable
            self.inventory.set_variable(host, 'ansible_host', host)

            # Add host to Tag Groups
            for tag in device.tags:
                self.inventory.add_child(self.tag_prefix + tag, host)

    def _set_config_property(self, config_property, required=True, default_value=None):
        if config_property in self.config_data:
            return self.config_data[config_property]
        else:
            if default_value or required is False:
                return default_value
            else:
                raise AnsibleError("an_netbox inventory plugin: missing configuration property: " + config_property)

    def _set_configuration(self):
        self.netbox_api_key = self._set_config_property("netbox_api_key")
        self.netbox_server_url = self._set_config_property("netbox_server_url")
        self.tag_prefix = self._set_config_property("tag_prefix", default_value="tag_")
        self.cut_domain_name = self._set_config_property("cut_domain_name", default_value=True)
        self.filter_site = self._set_config_property("filter_site", required=False)

    def _connect_to_netbox_api(self):
        try:
            self.netbox = pynetbox.api(str(self.netbox_server_url), token=self.netbox_api_key)
        except Exception:
            raise AnsibleError("an_netbox inventory plugin: Failed to establish connection to Netbox API")

    def parse(self, inventory, loader, path, cache=False):

        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self.config_data = self._read_config_data(path=path)

        # Test for pynetbox python module
        if not HAS_PYNETBOX:
            raise AnsibleError("an_netbox inventory plugin requires pynetbox module, install missing moduel with 'sudo pip install pynetbox'")

        self._set_configuration()
        self._connect_to_netbox_api()

        device_data = self.netbox.dcim.devices.all()
        vm_device_data = self.netbox.virtualization.virtual_machines.all()
        if vm_device_data:
            device_data = device_data + vm_device_data

        if self.filter_site:
            device_data = [d for d in device_data if d.site.name == self.filter_site]
        self._populate(device_data)
