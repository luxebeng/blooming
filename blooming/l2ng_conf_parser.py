#!/usr/bin/env python
""" l2ng_conf.py -- API suite for l2ng_conf parser
Usage:
    the test suite for l2ng module

"""
import json


class ConfParser:
    """This is the L2ng test case class. """

    def __init__(self, dev_name):
        """TODO: to be defined1. """
        self.dev_name = dev_name
        with open('l2ng_conf.json', 'r') as f:
            self.conf = json.load(f)

    def l3_intf_ip_get(self, l3_intf_name):
        """TODO: Docstring for l3_intf_ip_get.
        :returns: TODO

        """
        return self.conf[self.dev_name]["l3 intf"][l3_intf_name]["ip addr"]

    def l2_port_peer(self, l2_port):
        """get peer information by l2 port.
        :returns: return peer information(device and port)

        """
        dev = self.conf[self.dev_name]["l2 port"][l2_port]["peer"]["dev"]
        port = self.conf[self.dev_name]["l2 port"][l2_port]["peer"]["port"]
        return dev, port
