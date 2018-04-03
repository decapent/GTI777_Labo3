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
from time import time



def question1():
    # creating the Mininet object which supports an external controller
    net = Mininet(controller=RemoteController, link=TCLink)

    info( '*** Adding controller\n' )
    # Connecting the controller to Floodlight Openflow port 
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    info( '*** Adding hosts\n' )
    # Hosts are created with static IP
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')

    info( '*** Adding switch\n' )
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    s7 = net.addSwitch('s7')
    s8 = net.addSwitch('s8')
	
    info( '*** Creating links\n' )
    # Creating the topology of the whole network under test
    linkbw = 10
    net.addLink(h1, s1, bw=linkbw, delay='5ms')
    net.addLink(h2, s1, bw=linkbw, delay='4ms')
    net.addLink(h3, s8, bw=linkbw, delay='6ms')
    net.addLink(h4, s8, bw=linkbw, delay='3ms')
    net.addLink(s1, s2, bw=linkbw, delay='12ms')
    net.addLink(s1, s3, bw=linkbw, delay='3ms')
    net.addLink(s1, s6, bw=linkbw, delay='5ms')
    net.addLink(s2, s8, bw=linkbw, delay='4ms')
    net.addLink(s3, s4, bw=linkbw, delay='6ms')
    net.addLink(s4, s5, bw=linkbw, delay='3ms')
    net.addLink(s5, s8, bw=linkbw, delay='2ms')
    net.addLink(s6, s7, bw=linkbw, delay='10ms')
    net.addLink(s7, s8, bw=linkbw, delay='1ms')
	
    info( '*** Starting network\n')
    # Starting the experiment
    net.start()
	
    # Testing network connectivity between all hosts
    net.pingAll()
    
    # Launching an iperf command running in background
    # between h1 and h3. Output will be printed to file.
    performanceCommand = 'iperf -s > out.txt &'
    h3.cmd(performanceCommand)
	
    info( '*** Running CLI\n' )
    CLI( net )
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    question1()