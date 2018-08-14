#!/usr/local/bin/python3
""" dev_parser.py -- API suite for parser the device information
Usage:
    Interpret the informaton from data file 'dev.json'.
    Provide the API for other module. so the implementation is depend on the
data within data.
"""
import json
import time
import threading

import paramiko

import commands_jnpr


class Dev_Entry:
    def __init__(self, dev_name):
        """class initial
        """
        self.dev_name = dev_name
        with open('dev.json', 'r') as f:
            self.conf = json.load(f)

    def dev_probe(self, count):

        status = False

        host = self.conf[self.dev_name]["MGT IP address"]
        port = self.conf[self.dev_name]["port number"]
        user = self.conf[self.dev_name]["ssh user"]
        passwd = self.conf[self.dev_name]["passwd"]

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while True:
            try:
                client.connect(
                    hostname=host, port=port, username=user, password=passwd)
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                count -= 1
                print('%s: SSH transport is not ready...%d' %
                      (threading.current_thread().getName(), count))
                time.sleep(10)
                if count <= 0:
                    status = False
                    break
            except TimeoutError as e:
                # system is under reboot, not reachable yet.
                count -= 1
                print(' %s: Waiting for system timeout %d' %
                      (threading.current_thread().getName(), count))
                if count <= 0:
                    status = False
                    break
            else:
                # system is available now
                status = True
                break

        client.close()
        return status

    def ssh_login(self):
        """login by ssh
        :returns:

        """
        host = self.conf[self.dev_name]["MGT IP address"]
        port = self.conf[self.dev_name]["port number"]
        usr = self.conf[self.dev_name]["ssh user"]
        passwd = self.conf[self.dev_name]["passwd"]

        # initial the ssh session
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=usr, password=passwd)
        return client

    def image_upgrade(self, filename):
        """upgrade the image on devices
        """

        # if the device is not existed, return directly
        status = self.dev_probe(1)
        if not status:
            print('the device is not available', self.dev_name)

        # upgrade the iamge on device
        client = self.ssh_login()
        commands_jnpr.dev_image_upgrade(client, filename)
        client.close()
        print('Device is rebooted at %s' % threading.currentThread().getName())

        # wait for system reboot
        time.sleep(20)
        status = self.dev_probe(100)
        if not status:
            print('the device is not available', self.dev_name)

    def ping(self, dst_ip):
        """TODO: Docstring for ping.
        :returns: TODO

        """
        # run the ping command
        client = self.ssh_login()
        status = commands_jnpr.rapid_ping(client, dst_ip)
        client.close()
        return status

    def lldp_verification(self, host_port, peer_dev, peer_port):
        """lldp verification SAL function.
        :returns: True if test passed.

        """
        # run show lldp neighbor command
        client = self.ssh_login()
        status = commands_jnpr.lldp_show(client, host_port, peer_dev,
                                         peer_port)
        client.close()
        return status

    def ae_intf_verify(self, ae_intf):
        """ae intf verification SAL function.
        :returns: True if test passed.

        """
        # run show lldp neighbor command
        client = self.ssh_login()
        status = commands_jnpr.ae_intf_show(client, ae_intf)
        client.close()
        return status

    def irb_mac_addr(self):
        """get irb interface mac address

        :returns: mac addr of irb interface
        """
        return self.conf[self.dev_name]["port"]["irb"]["mac address"]

    def mac_entry_get(self, vlan_name, host_port, peer_mac_addr):
        """get mac entry informaton

        :returns: mac addr of irb interface
        """
        client = self.ssh_login()
        status = commands_jnpr.mac_entry_info_get(client, vlan_name, host_port,
                                                  peer_mac_addr)
        client.close()
        return status

    def stp_verify(self, vlan_id, host_port, stp_state):
        """get stp status of special interface

        :returns: True is status is true
        """
        client = self.ssh_login()
        status = commands_jnpr.stp_status(client, vlan_id, host_port,
                                          stp_state)
        client.close()
        return status
