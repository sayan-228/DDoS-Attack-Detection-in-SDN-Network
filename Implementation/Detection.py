#
# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pox.core import core
import pox.openflow.libopenflow_01 as of
from collections import Counter

log = core.getLogger()



class Tutorial (object):
  
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ip address is on
    # which switch port (keys are MACs, values are ports).
    self.ip_to_port = {}
    for i in range(1,11):
        self.ip_to_port['10.0.0.'+str(i)] = i
    
    self.numpackets = 0
    self.d = {}
    self.t = []
    self.arr = []
    self.bots = []    

  def resend_packet (self, packet, packet_in, out_port):
    
    msg = of.ofp_flow_mod()
    #print 'msg = '+ str(msg)
    msg.match = of.ofp_match.from_packet(packet)
    #msg.idle_timeout = 1
    msg.hard_timeout = 1
    #print 'msg.match = '+ str(msg.match)
    msg.data = packet_in
    #print 'msg.data = '+ str(msg.data)
    msg.buffer_id = packet_in.buffer_id
    #print 'msg.buffer_id = '+ str(msg.buffer_id)

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    #print 'action = ' + str(action)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)
    
    

  def act_like_hub (self, packet, packet_in):
    
    self.resend_packet(packet, packet_in, of.OFPP_ALL)


  def act_like_switch (self, packet, packet_in):
    
    #Extract the source and destination IP address from the packet payload
    rawPayLoad = str(packet.payload)   
    splitPayLoad = rawPayLoad.split()
    rawPayLoadType = str(packet.payload.payload)
    splitPayLoadType = rawPayLoadType.split()
    if('ARP' in splitPayLoad[0]):
        srcdstpair = splitPayLoad[-1][:-1]
        srcip = srcdstpair.split('>')[0]
        dstip = srcdstpair.split('>')[1]
        
        
    elif('ICMP' in splitPayLoad[0]):
        srcdstpair = splitPayLoad[1]
        srcip = srcdstpair.split('>')[0]
        dstip = srcdstpair.split('>')[1]   
    
    
        if 'REQUEST' in splitPayLoadType[0]:
            self.numpackets = self.numpackets + 2
            
            if ['h'+str(srcip[-1]),'h'+str(dstip[-1])] not in self.arr:
                self.arr.append(['h'+str(srcip[-1]),'h'+str(dstip[-1])])            
            
    alldest = []
    
    
    for i in self.arr:
        alldest.append(i[1])
        
    alldest = [item for items, c in Counter(alldest).most_common() for item in [items] * c]
    
    if len(alldest)>=1:
        temp= alldest[0]
        k = 1
        pot_cnc = ''
        for i in alldest:
            if i != temp:
                k = k+1
            if k == 2:
                pot_cnc = i
                break
            
        for i in self.arr:
            if pot_cnc == i[1]:
                self.t.append(i[0])
        
        for i in self.t:
            if i in self.d:
                self.d[i][0] = self.d[i][0] + 1
            else:
                self.d[i] = [1,0]
        
        expiredhosts = []
        for i in self.d:
            self.d[i][1] = self.d[i][1]+1
            if self.d[i][1] > 10:
                if self.d[i][0] > 5:
                    if i not in self.bots:
                        self.bots.append(i)
                    expiredhosts.append(i)
                else:
                    expiredhosts.append(i)
                    
        for i in expiredhosts:
            self.d.pop(i)
                
                
        print 'bots = ' + str(self.bots)
        
    if self.numpackets%250 == 0:
        
        for i in self.d:
            self.d[i][1] = self.d[i][1]+1
        self.t = []
        self.arr = []
        
      
    self.resend_packet(packet,packet_in,self.ip_to_port[dstip])
    
       
     
   

  def _handle_PacketIn (self, event):   

    packet = event.parsed 
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
    #print 'packet = ' + str(packet)
    packet_in = event.ofp 
    #self.numpackets = self.numpackets + 1
    #print "num of packets = "+str(self.numpackets)
    self.act_like_switch(packet, packet_in)
    #self.act_like_hub(packet, packet_in)



def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
