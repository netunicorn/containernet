#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
import time

from mininet.net import Containernet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log import setLogLevel
setLogLevel('debug')

net = Containernet(controller=Controller)
net.addController('c0')
d1 = net.addDocker(
    'd1',
    dimage="netunicorn/executor-template",
    dcmd=["bash", "-c", "trap 'sigusr1_received=true' SIGUSR1; while [[ -z $sigusr1_received ]]; do sleep 1; done; python3 -m netunicorn.executor"],
    dnameprefix="test1"
)
d2 = net.addDocker(
    'd2',
    dimage="netunicorn/executor-template",
    dcmd=["bash", "-c", "trap 'sigusr1_received=true' SIGUSR1; while [[ -z $sigusr1_received ]]; do sleep 1; done; python3 -m netunicorn.executor"],
    dnameprefix="test1"
)

s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')

net.addLink(d1, s1)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, d2)

net.start()
d1.cmd("kill -SIGUSR1 1")
d2.cmd("kill -SIGUSR1 1")


# wait until containers are stopped
while any(x._is_container_running() for x in [d1, d2]):
    time.sleep(1)

net.stop()

