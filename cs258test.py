"""
Script to start mininet with remote controller and a full mesh 4 switch network

"""


from mininet.topo import Topo
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Intf
import time

setLogLevel('info')

c0 = RemoteController('c0', ip="192.168.56.101", port=6633)


class MyTopo( Topo ):
    "Simple topology example."


    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        H1 = self.addHost( 'h1', ip="10.0.1.1/8" )
        H2 = self.addHost( 'h2', ip="10.0.1.2/8" )
	H3 = self.addHost( 'h3', ip="10.0.1.3/8" )
	H4 = self.addHost( 'h4', ip="10.0.1.4/8" )
        

	S1 = self.addSwitch( 's1' )
        S2 = self.addSwitch( 's2' )
	S3 = self.addSwitch( 's3' )
	S4 = self.addSwitch( 's4' )
	S5 = self.addSwitch( 's5' )

        # Add links
        self.addLink( H1, S1 )
        self.addLink( H2, S2 )
	self.addLink( H3, S3 )
	self.addLink( H4, S4 )

	self.addLink(S1, S5)
	self.addLink(S2, S5)
	self.addLink(S3, S5)
	self.addLink(S4, S5)

        self.addLink( S1, S2 )
	#self.addLink( S1, S3 )
	self.addLink( S1, S4 )

	self.addLink( S2, S3 )
	#self.addLink( S2, S4 )

	self.addLink( S3, S4 )



topo = MyTopo()

net = Mininet(topo=topo, controller=c0)
try:
	net.start()
	time.sleep(5)
	net.pingAll()
	CLI(net)


except Exception,e:
	print(str(e)) 
	net.stop()
net.stop()
