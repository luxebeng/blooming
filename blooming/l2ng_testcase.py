from .dev_parser import Dev_Entry
from .l2ng_conf_parser import ConfParser


def ping_l3_intf(host_dev, dst_dev, dst_intf_name):
    """ping irb interface between the different devices
    :arg1: "host_dev" is ping origined device.
           "dst_dev" is the target devcie.
           "dst_intf_name" is target L3 interface.
    :returns:  True if ping from host to dst successfully
    """
    dst = ConfParser(dst_dev)
    dst_ip = dst.l3_intf_ip_get(dst_intf_name)
    host = Dev_Entry(host_dev)
    status = host.ping(dst_ip)
    if status:
        print("ping from %s to %s successfully" % (host_dev, dst_dev))


def verify_lldp(host_dev, host_port):
    """ lldp protocal test case.
        by lldp output, to confirm lldp setup between 2 interfaces.
    :returns: None

    """
    host = ConfParser(host_dev)
    peer_dev, peer_port = host.l2_port_peer(host_port)
    host = Dev_Entry(host_dev)
    status = host.lldp_verification(host_port, peer_dev, peer_port)
    if status:
        print("lldp test case for %s is passed successfully" % host_dev)


def verify_ae_interface(host_dev, ae_intf):
    """TODO: Docstring for verify_ae_interface.
    :returns: True if verification passed.
    """
    host = Dev_Entry(host_dev)
    status = host.ae_intf_verify(ae_intf)
    if status:
        print("ae interface test for %s is passed successfully" % host_dev)

    pass


def verify_mac_learning(host_dev, vlan_name, host_port):
    """ verify the mac learning on special physical interface.
    :arg1: host_dev is the target device
     arg2: vlan_id is the vlan domain
     arg3: host_port is the special physical interface
    :returns: True if mac entry is matched
    """

    # get peer device information from json file
    host = ConfParser(host_dev)
    peer_dev, peer_port = host.l2_port_peer(host_port)
    peer_entry = Dev_Entry(peer_dev)
    peer_irb_mac_addr = peer_entry.irb_mac_addr()

    # get peer device information from mac entry on device
    host_entry = Dev_Entry(host_dev)
    status = host_entry.mac_entry_get(vlan_name, host_port, peer_irb_mac_addr)
    if status:
        print("mac learning test case verified successfully for %s" % host_dev)


def verify_stp(host_dev, vlan_id, host_port, stp_state):
    """ verify stp status on special physical interface.
    :arg1: host_dev is the target device
     arg2: vlan_id is the vlan domain
     arg3: host_port is the special physical interface
     arg4: stp_state is the status of stp state
    :returns: True if mac entry is matched
    """
    # get stp status for special interface
    host_entry = Dev_Entry(host_dev)
    status = host_entry.stp_verify(vlan_id, host_port, stp_state)
    if status:
        print("stp test case verified successfully for %s, %s" %
              (host_dev, host_port))


def l2ng_testcase():

    # ping irb interface between the different devices
    # the parameter is "host device, dst device and dst L3 interface"
    print("******** Ping Test Case ********")
    ping_l3_intf("l2ng-ut-srx345a", "l2ng-ut-srx320a", "irb.2018")
    ping_l3_intf("l2ng-ut-srx320a", "l2ng-ut-srx345a", "irb.2018")
    ping_l3_intf("l2ng-ut-srx550a", "l2ng-ut-srx320a", "irb.2018")
    ping_l3_intf("l2ng-ut-srx320a", "l2ng-ut-srx550a", "irb.2018")
    ping_l3_intf("l2ng-ut-srx320b", "l2ng-ut-srx345a", "irb.2018")
    ping_l3_intf("l2ng-ut-srx345a", "l2ng-ut-srx320b", "irb.2018")

    # aggregation interface test case
    print("******** AE Interface Test Case ********")
    verify_ae_interface("l2ng-ut-srx345a", "ge-5/0/8")
    verify_ae_interface("l2ng-ut-srx320a", "ge-0/0/6")

    # lldp testcase
    print("******** LLDP Test Case ********")
    verify_lldp("l2ng-ut-srx345a", "ge-5/0/8")
    verify_lldp("l2ng-ut-srx320a", "ge-0/0/6")

    # spanning tree testcase
    print("******** STP Test Case ********")
    verify_stp("l2ng-ut-srx345a", "2018", "ge-5/0/8", "FWD")
    verify_stp("l2ng-ut-srx345a", "2018", "ae0", "FWD")
    verify_stp("l2ng-ut-srx320a", "2018", "ge-0/0/5", "FWD")
    verify_stp("l2ng-ut-srx320a", "2018", "ge-0/0/6", "FWD")
    verify_stp("l2ng-ut-srx550a", "2018", "ae0", "FWD")
    verify_stp("l2ng-ut-srx550a", "2018", "ge-6/0/1", "BLK")

    # verify mac learning test suite.
    # mac learning only on L2 interface
    print("******** Mac Learning Test Case ********")
    verify_mac_learning("l2ng-ut-srx345a", "v2018", "ae0")
    verify_mac_learning("l2ng-ut-srx345a", "v2018", "ge-5/0/8")
    verify_mac_learning("l2ng-ut-srx345a", "v2018", "ge-5/0/15")
    verify_mac_learning("l2ng-ut-srx320a", "v2018", "ge-0/0/6")
    verify_mac_learning("l2ng-ut-srx550a", "v2018", "ae0")
