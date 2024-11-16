from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel

class MyTopo(Topo):
    def build(self):
        # Tạo các host và switch
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')
        h4 = self.addHost('h4', ip='10.0.0.4')
        s1 = self.addSwitch('s1')

        # Kết nối các host với switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)

def run():
    topo = MyTopo()
    net = Mininet(topo=topo)
    net.start()

    # Kiểm tra kết nối
    print("Pinging all hosts...")
    net.pingAll()

    # Đưa Mininet vào trạng thái CLI
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
