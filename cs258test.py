"""
Script to start mininet with remote controller and a full mesh 4 switch network

"""


from mininet.topo import Topo
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Intf
from bottle import route, run, template
import requests
import time


setLogLevel('info')

c0 = RemoteController('c0', ip="192.168.56.101", port=6633)


class MyTopo( Topo ):
    def __init__( self ):

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
	self.addLink( S1, S4 )

	self.addLink( S2, S3 )

	self.addLink( S3, S4 )

@route('/cmd/<node>/<cmd>')
def cmd(node='h1', cmd='hostname'):
	out, err, code = net.get( node ).pexec( cmd)
	return out + err

@route('/stop')
def stop():
	net.stop()

@route('/iperf/<node1>/to/<node2>')
def run_iperf(node1='h1', node2='h2'):
	n1 = net.get(node1)
	n2 = net.get(node2)
	out =  net.iperf((n1, n2))
	return out + "\n"

@route('/start_flows')
def start_flows():
	builder = ""
	temp_str = "Adding alternate flow routes to ODL...\n"
	print(temp_str)
	builder += temp_str
	headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}

	url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1"
	response = requests.put(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow1.xml').read())
	temp_str = response.text
	builder += "\n" + temp_str

	time.sleep(2)

	url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/2"
	response = requests.put(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow2.xml').read())
	temp_str = response.text
	builder += "\n" + temp_str

	time.sleep(2)

	url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/3"
	response = requests.put(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow3.xml').read())
	temp_str = response.text
	builder += "\n" + temp_str

	builder += "\n" +  "Start flows: DONE\n"
	return builder

@route('/stop_flows')
def stop_flows():
	builder = "Stopping flows...\n"
	url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1"
	headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
	response = requests.delete(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow1.xml').read())
	temp_str = response.text
	builder += "\n" + response.text

	url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/2"
	headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
	response = requests.delete(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow2.xml').read())
	temp_str = response.text
	builder += "\n" + response.text

	url = "http://71.198.1.196:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/3"
	headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
	response = requests.delete(url, headers=headers, auth=('admin', 'admin'), data=open('set_flow3.xml').read())
	temp_str = response.text	
	builder += "\n" + response.text	

	builder += "\n" + "Stop flows: DONE\n"
	return builder

topo = MyTopo()

net = Mininet(topo=topo, controller=c0)
try:
	net.start()
	time.sleep(5)
	net.pingAll()
	run(host='localhost', port=8085)
#	CLI(net)


except Exception,e:
	print(str(e)) 
	net.stop()
net.stop()
