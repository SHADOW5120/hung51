from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI

def create_topology():
    net = Mininet(controller=RemoteController)
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    # Create a simple topology with a switch and 3 hosts
    s1 = net.addSwitch('s1')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')

    # Add links between switch and hosts
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)

    net.build()
    c0.start()
    s1.start([c0])

    print("Topology is running. Use CLI to interact.")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    create_topology()
