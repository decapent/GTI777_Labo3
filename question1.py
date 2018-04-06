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


class IPerfConfig():
	def __init__(self, **params):
		
		"""
		  Encapsulates the concept of running various iperf commands.
		  Commands are intended to be ran in background and append
		  all traffic to a log file.
		"""
		
	    self.TCPCommands = {
		    "CLIENT" : "sudo iperf -c 10.0.0.3 -t 180 -i 10 >> client.txt &",
			"SERVER" : "sudo iperf –s -t 180 -i 10 >> server.txt &"
		}
		
		self.UDPCommands = {
			"CLIENT" : "sudo iperf -c 10.0.0.3 -t 180 -i 10 >> client.txt &",
			"SERVER" : "sudo iperf -s -u -t 180 -i 10 >> server.txt &"
		}


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

def question1(totalExperimentTime):
    
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
    info( "Initializing the experiment..." )
    sleep(3)
    
    # Testing network connectivity between all hosts
    net.pingAll()
    info("*** Running the experiment for %s seconds \n" % totalExperimentTime)	
    
    # The clock is ticking!
    start = time()
    elapsed = 0
    
    info("Obtaining client(h1) and server(h3) hosts \n")
    hosts = [ net.getNodeByName( h ) for h in topology.hosts() ]
    client, server = hosts[0], hosts[2]
    
    # Launching an iperf command running in background
    # Output will be printed to file.
	config = IPerfConfig()
    server.cmd(config.TCPCommands["SERVER"])
    client.cmd(config.TCPCommands["CLIENT"])
	
    while elapsed < totalExperimentTime:
	    elapsed = time() - start
        isUDPTransfer = False
        if elapsed > 180 and elapsed < 360 and not isUDPTransfer: # Between 3 and 6 minutes
			server.cmd(config.UDPCommands["SERVER"])
            client.cmd(config.UDPCommands["CLIENT"])
		    isUDPTransfer = True
        elif elapsed > 360 and isUDPTransfer: # After 6 minutes
            server.cmd(config.TCPCommands["SERVER"])
            client.cmd(config.TCPCommands["CLIENT"])
			isUDPTransfer = False
        
        # Sleeping the script for 2 seconds. Since commands were
        # launched in background, sleeping won't interfere with 
        # the network's traffic.
		net.ping((client, server))
        sleep(2)

    info( '*** Stopping network' )
    net.stop()
    
if __name__ == '__main__':
    setLogLevel( 'info' )
	
    TOTAL_EXP_TIME = 540 #seconds
    question1(TOTAL_EXP_TIME)