#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Cours GTI100
Lab 3 - Partie 2
----------------------------------
Nom et prénom : LAVALLEE, PATRICK
----------------------------------
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.topo import Topo
from time import time
from time import sleep


class Labo3Topology(Topo):
    def __init__(self, nbHosts, nbSwitches, linkbw, **params):
        
        # Base class initialization
        Topo.__init__(self, **params)
        
        # Creating hosts
        hosts = [self.addHost('h%s' % h, ip='10.0.0.%s' % h) 
            for h in range(1, nbHosts+1)]
        
        # Creating switches
        switches = [self.addSwitch('s%s' % s) 
            for s in range(1, nbSwitches+1)] 
        
        # Creating links
        self.addLink(hosts[0], switches[0], bw=linkbw, delay='5ms')
        self.addLink(hosts[1], switches[0], bw=linkbw, delay='4ms')
        self.addLink(hosts[2], switches[7], bw=linkbw, delay='6ms')
        self.addLink(hosts[3], switches[7], bw=linkbw, delay='3ms')
        self.addLink(switches[0], switches[1], bw=linkbw, delay='12ms')
        self.addLink(switches[0], switches[2], bw=linkbw, delay='3ms')
        self.addLink(switches[0], switches[5], bw=linkbw, delay='5ms')
        self.addLink(switches[1], switches[7], bw=linkbw, delay='4ms')
        self.addLink(switches[2], switches[3], bw=linkbw, delay='6ms')
        self.addLink(switches[3], switches[4], bw=linkbw, delay='3ms')
        self.addLink(switches[4], switches[7], bw=linkbw, delay='2ms')
        self.addLink(switches[5], switches[6], bw=linkbw, delay='10ms')
        self.addLink(switches[6], switches[7], bw=linkbw, delay='1ms')

def question1():
    
	# Creating the experiment's topology
    topology = Labo3Topology(nbHosts=4, nbSwitches=8, linkbw=10)
    
	# Connecting the controller to Floodlight Openflow port
	floodLight = RemoteController('c0', ip='127.0.0.1', port=6653)
    
    # Creating the Mininet network
    net = Mininet(topo=topology,
                  controller=floodLight,
                  link=TCLink)
    
    info( '*** Starting network\n')
    # Starting the experiment
    net.start()
	
	# Sleep is used to ensure a 100% success rate during ping
    print "Initializing the experiment..."
    sleep(5)
    
    # Testing network connectivity between all hosts
    net.pingAll()
    
    # Launching an iperf command running in background
    # between h1 and h3. Output will be printed to file.
    # servercommand = 'iperf –s > server.txt &'
    # clientcommand = 'iperf -c 10.0.0.3 > client.txt &'
    # h3.cmd(servercommand)
    # h1.cmd(clientcommand)
    
    CLI( net )
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    question1()