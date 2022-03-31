# DDoS-Attack-Detection-in-SDN-Network
Implementation of DDoS Attack Detection in SDN using OpenFlow

● Implemented a detection mechanism using Mininet VM and POX controller for DDoS attacks mounted by botnets using a C&C server.<br />
● Features of SDN are utilized to effectively block legitimate-looking DDoS attacks mounted by a larger number of bots.<br />

## Required Components
a. Download	Virtualbox:<br />
https://www.virtualbox.org/wiki/Downloads<br />
b. Download	Mininet:<br />
https://github.com/mininet/mininet/wiki/Mininet-VM-Images<br />
c. Configure	the	Virtualbox	so	that	you	can	access	it	through	SSH:<br />
https://github.com/mininet/openflow-tutorial/wiki/Set-up-Virtual-Machine<br />

## Run	a	basic	topology.
a. Run	a	controller:<br />
./pox.py log.level --DEBUG misc.of_tutorial<br />
This loads the controller in ~/pox/pox/misc/of_tutorial.py. This version acts like a	dumb switch	and	floods all packets.<br />
b. Set up a topology that	connects to	the controller:<br />
sudo mn --custom ~/mininet/custom/topo-2sw-2host.py --controller remote<br />
This	loads	the	topology	~/mininet/custom/ topo-2sw-2host.py.	This version	creates	a	simple topology	with one switch	connected	to two hosts<br />

## Resources
https://github.com/mininet/openflow-tutorial/wiki<br />
https://openflow.stanford.edu/display/ONL/POX+Wiki<br />
