blooming
===============================

version number: 1.0.7
author: Luxebeng

Overview
--------

`blooming` Framework is a generic open source test automation framework for acceptance test-driven development (ATDD). which is operating system and application independent. The core framework is implemented using Python 3. 

Project is hosted on [GitHub](https://github.com/luxebeng/blooming) where you can find source code, an issue tracker, and some further documentation. 

Installation
------------

To install use pip:

    $ pip install blooming


Or clone the repo:

    $ git clone https://github.com/luxebeng/blooming.git
    $ python setup.py install

How does it work
----------------

The test suites is component with series independent module, and all of them can be executed in sequence. 

For each test case, device and configuration file are abstracted as an object. which is defined as a .json file, and all the operation is defined as member function of an object.

For different there are command lists on devices from different vendor, so there is a SAL layer to adapt the commands for different in future. but now it's called directly.

The simple sketch is as follows:
![SW_architecture](docs/media/SW_architecture.png)

Example
-------

at the root folder, there is 2 json files are provided.

`dev.json:`       which define the device information. which is static for a special devices.
```
***device information*** 
{
  "bj340g":{
    "device name": "srx340g",            # device name
    "MGT IP address": "10.208.128.161",  # login IP address
    "port number": 22,                   # ssh login portID
    "ssh user": "root",                  # ssh login user
    "passwd": "Embe1mpls"                # ssh login passwd
  }
}
```

`xxxx_conf.json`: which is config related information. which is depended on the topology of testbed and configuration.
```
{
  "bj340g":{
    "l2 port":{
      "ge-0/0/5":{
        "peer":{
          "dev":"bj300a",
          "port":"ge-0/0/5"
        }
      }
    },
    "l3 intf":{
      "irb.20":{
        "ip addr":"20.0.0.20"
      }
    }
  }
}
```

There is a detail document about L2NG test suites. please refer to documents of [L2NG Test suites](./docs/l2ng_test_sutes.md).

Contributing
------------

TBD
