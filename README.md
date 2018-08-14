blooming
===============================

version number: 1.0.3
author: Luxebeng

Overview
--------

A(nother) test automation framework for network device.
`blooming` Framework is a generic open source test automation framework for acceptance test-driven development (ATDD). users can create new  from existing ones using the same syntax that is used for creating test cases. 
`blooming` Framework is operating system and application independent. The core framework is implemented using Python 3. 

`blooming` Framework project is hosted on [GitHub](https://github.com/luxebeng/blooming) where you can find source code, an issue tracker, and some further documentation. 

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

```
***device information*** 
{
  "bj340g":{
    "device name": "srx340g",            # device name
    "MGT IP address": "10.208.128.161",  # login IP address
    "port number": 22,                   # ssh login portID
    "ssh user": "root",                  # ssh login user
    "passwd": "Embe1mpls"                # ssh login passwd
  },
  "bj300a":{
    "device name": "srx300a",
    "MGT IP address": "10.208.128.241",
    "port number": 22,
    "ssh user": "root",
    "passwd": "Embe1mpls"
  }
}

*** conmmand type ***
%python3 main.py -f file_name    # file_name is upgrade image name 
```

There is a detail document about L2NG test suites. please refer to documents of [L2NG Test suites](./docs/l2ng_test_sutes.md).

Contributing
------------

TBD
