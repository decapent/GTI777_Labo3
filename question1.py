#!/usr/bin/python
# -*- coding: utf-9 -*-
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
    net = Mininet(controller=Controller)

    info( '*** Adding controller\n' )
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    info( '*** Adding hosts\n' )
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
    net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s8)
	net.addLink(h4, s8)
	net.addLink(s1, s2)
	net.addLink(s1, s3)
	net.addLink(s1, s6)
	net.addLink(s2, s8)
	net.addLink(s3, s4)
	net.addLink(s4, s5)
	net.addLink(s5, s8)
	net.addLink(s6, s7)
	net.addLink(s7, s8)
	
    info( '*** Starting network\n')
    net.start()
	
	
    # votre code...
			
	



	
    info( '*** Running CLI\n' )
    CLI( net )
    info( '*** Stopping network' )
    net.stop()



if __name__ == '__main__':
    setLogLevel( 'info' )
    question1()