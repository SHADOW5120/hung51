from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel

class FatTreeTopo(Topo):
    def build(self):
        # Example fat tree with 2 pods, each with 2 switches and 2 hosts
        pod1 = self.addSwitch('s1')
        pod2 = self.addSwitch('s2')

        # Hosts for pod1
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Hosts for pod2
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Connect hosts to switches
        self.addLink(h1, pod1)
        self.addLink(h2, pod1)
        self.addLink(h3, pod2)
        self.addLink(h4, pod2)

        # Connect switches
        self.addLink(pod1, pod2)

def run():
    setLogLevel('info')
    topo = FatTreeTopo()
    net = Mininet(topo=topo, controller=Controller)
    net.start()

    # Start the CLI interface to interact with the network
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
