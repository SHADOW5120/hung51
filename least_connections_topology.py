from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink

class LeastConnectionsTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        # Thêm switch và máy chủ
        switch = self.addSwitch('s1')
        hosts = []
        for i in range(1, 4):  # Tạo 3 máy chủ
            host = self.addHost(f'h{i}')
            self.addLink(host, switch, bw=10)
            hosts.append(host)

        # Thêm 1 client
        client = self.addHost('client')
        self.addLink(client, switch, bw=10)

topos = {'leastconnections': (lambda: LeastConnectionsTopo())}

if __name__ == '__main__':
    # Chạy Mininet với topology
    topo = LeastConnectionsTopo()
    net = Mininet(topo=topo, controller=RemoteController, link=TCLink)
    net.start()
    net.pingAll()
    net.stop()
