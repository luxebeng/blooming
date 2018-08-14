#!/usr/bin/env python
"""commands_jnpr.py -- API suite for image upgrade
Usage:
Commands implemented on Juniper network devices.because the command line is
implemented specifically for each vendor,so the command line need to be
modified for other vendor devices. but code is common.
In future, this can also be commonized with platfom independently.
"""
import select

# import threading
import json

import paramiko


def dev_image_upgrade(client, filename):

    # display the current version
    print('display system version')
    command = 'exec cli show ' + 'version'
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")

    # upload the file
    print('Upload file %s to remote device' % filename)
    sftp = paramiko.SFTPClient.from_transport(client.get_transport())
    sftp = client.open_sftp()
    sftp.put(filename, '/var/tmp/' + filename)

    # list the uploaded file
    print('List the uploaded image')
    command = 'ls -lt /var/tmp/' + filename
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")

    # assign the next image
    print('Assign the next bootup package')
    command = 'exec cli request system software add /var/tmp/' + \
        filename + ' no-copy no-validate reboot'
    chan = client.get_transport().open_session(timeout=5)
    chan.exec_command(command)
    while True:
        if chan.exit_status_ready():
            break
        rl, wl, xl = select.select([chan], [], [], 0.0)
        if len(rl) > 0:
            print(chan.recv(1024))


def rapid_ping(client, dst_ip):
    """TODO: Docstring for ping.
    :returns: TODO

    """
    status = False
    # run ping command with count 10 rapidly
    command = 'exec cli ping ' + dst_ip + ' count 10 rapid'
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    for line in iter(stdout.readline, ""):
        if ("!!!!!!!!!" in line):
            status = True
    return status


def lldp_show(client, host_port, peer_dev, peer_port):
    """get lldp neighbor informations.
    :returns: True if the output information about neighbor is match with input
    False if dismatch with input parameter
    """
    status = False
    # show lldp neighbors interface xxx
    command = 'exec cli show lldp neighbors interface ' + \
        host_port + ' \| display json'
    stdin, stdout, stderr = client.exec_command(command)
    output = json.loads(stdout.read())

    neighbors = output["lldp-neighbors-information"][0]
    ngbr = neighbors["lldp-neighbor-information"][0]
    system_name = ngbr["lldp-remote-system-name"][0]["data"]
    port_name = ngbr["lldp-remote-port-description"][0]["data"]
    if system_name == peer_dev and port_name == peer_port:
        status = True

    return status


def ae_intf_show(client, ae_intf):
    """get ae interface informations.
    :returns: True if the output information about ae interface is as expected
    """
    status = False
    # show lldp neighbors interface xxx
    command = 'exec cli show interface ' + \
        ae_intf + ' detail \| display json'
    stdin, stdout, stderr = client.exec_command(command)
    output = json.loads(stdout.read())

    ae_phy_info = output["interface-information"][0]["physical-interface"][0]
    status = ae_phy_info["oper-status"][0]["data"]
    if status == "up":
        status = True

    return status


def mac_entry_info_get(client, vlan_name, port, peer_mac_addr):
    """based on the input information,found any mac entry is matched.
    :returns: True if one entry is matched
    """
    status = False
    # show ethernet-switching table interface xxx
    command = 'exec cli show ethernet-switching table interface ' + \
        port + ' \| display json'
    stdin, stdout, stderr = client.exec_command(command)
    output = json.loads(stdout.read())

    mac_db = output["l2ng-l2ald-interface-macdb-vlan"][0]
    mac_entry_info = mac_db["l2ng-l2ald-mac-entry-vlan"][0]
    # "vlan_name, port_name, mac_addr" is matched, then return True
    for mac_entry in mac_entry_info["l2ng-mac-entry"]:
        if mac_entry["l2ng-l2-mac-vlan-name"][0]["data"] == vlan_name and \
                mac_entry["l2ng-l2-mac-address"][0]["data"] == peer_mac_addr:
            status = True
            break

    return status

def stp_status(client, vlan_id, port, stp_state):
    """based on input information,found stp status of special interface
    :returns: True if status is matched
    """
    status = False
    # show spanning-tree interface vlan-id xxx
    command = 'exec cli show spanning-tree interface vlan-id ' + \
        vlan_id + ' \| display json'
    stdin, stdout, stderr = client.exec_command(command)
    output = json.loads(stdout.read())

    stp_instance = output["stp-interface-information"][0]["stp-instance"][0]
    stp_interfaces = stp_instance["stp-interfaces"][0]
    # "vlan_name, port_name, mac_addr" is matched, then return True
    for stp_entry in stp_interfaces["stp-interface-entry"]:
        if stp_entry["interface-name"][0]["data"] == port and \
                stp_entry["port-state"][0]["data"] == stp_state:
            status = True
            break

    return status
