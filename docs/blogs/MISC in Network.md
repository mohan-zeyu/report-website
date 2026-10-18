VPN and Proxy

Started by RVPN (Remote VPN) of aTrust, I get to know something about the VPN, which is totally different from proxy techniques people usually talk about in daily life. 

Many people still think these two are equivalent due to possibly the advertisement or idiomatic sayings in China.

The physical layer sends bits.

The link layer sends bytes to the next node by MAC address.

The Internet layer sends bytes to specific machine by IP address

The transport layer sends bytes to a process specified by IP + port

Each layer parse the `dst` and `src` from upper layer and resolves it to its useful one.

## How the subnet mask makes sense?

I realize things below from such a problem: The Network Homework asked me, **when would the APR message be present in the requests?**

And the ARP message carries the MAC address of devices. Then as a new learner, I was curious about why we still need the MAC address, even if we could directly use the IP address to locate the destination.  (Here maybe a logic vulnerability: why not broadcast with IP address to match device)

Then actually, the layer 3, IP is packaged by another frame, link layer. So each device just looks at the outside package "address" to define whether its owner, which is exactly the MAC.

So, how would our own laptops, know the destination device's MAC? Then they broadcast the question, "who has `192.168.1.10`?" 

OK, here comes the next question. For sending a request to a remote machine. Here are two cases:

1. You send them to a device just close to you, all under the same router (maybe switch)

2. You want to access `google.com`, the IP address `142.251.150.119`, for example, is located at a very far away place.

Then, if you want to send a packet, your device must decide which MAC it to go, right? Because you have to make the hops starting so that it could finally go somewhere.

- So, for destination IP within the same subnet, your device choose to ask that peer for its MAC directly because it's normally very "close" (why I add quotes here because I have a misunderstanding just now) to you so that you can access it directly.

- Then for others outside, it asks the router / switch for its MAC. Then packets would be sent there.

Then afterwards, each router/switch will update the layer 2 info for next hop.

Here we introduce the concept of subnet and subnet mask.

Because it's the network mask that let us decide whether a destination should be reached by directly or indirectly with intermediate things.

But more questions come.

Previously, my comprehension about the subnet mask is all about the DHCP, assigning private network addresses with a small range, and it's nothing fancy, pretty trivial.

Let's consider one scenario, your dormitory, where is small enough for peer devices to communicate directly by maybe radio waves.

But based on my observation, we are using very different IP addresses. 

For example, someone is at `10.162.x.x` while someone is at `10.110.x.x`. 

Also, interestingly, there are indeed someone in another place who owns maybe the same subnet, beginning with `10.162.x.x`. 

So, conclusively, several subnets can share the same physical equipment, and one subnet can extend across several APs, which is the credit of the VLAN. virtual LAN. Being connected to the same AP does not guarantee being in the same subnet.

However, at first, I felt very puzzled about this design around the campus. 

Because here's a very naive design pattern:

For example, we want everyone's private ip addr to start with the 10

1. We split each dorm as a very small subnet, let's say `/24`.

2. Then inside every dorm (small unit), devices can communicate directly with each other.

3. For upper levels, we can gradually increase the level of subnet.

4. Then if a device wants to send packets outside the subnet, it could turn to the router / switch. 

5. After packets coming to upper level, repeat the same thing until finding the target.

But instead, APs and switches connect rooms and buildings. VLANs, gateways, and sometimes wireless tunnels organize users into logical networks. DHCP supplies each device with the appropriate IP address, mask, and gateway.

Below are some reasons I guess why the campus does such things:

1. A new IP normally breaks an existing TCP connection. Keeping the old IP requires the network to preserve its reachability—for example, by tunneling packets from the original attachment point to your new one.

2. Maybe for better privilege management for students after authenticating. 

3. Also, if the IP addresses change constantly with your physical positions, the network system should manage a huge table for updating your attachment between IP and identity.

4. to be continued ... I haven't come up with more.

OK, let's assume we choose this design. Then here a final problem: the network still should know where to send the packets to you, to the AP physically near you.

So after your device associates with the new AP, (I think it's better by identity keys than MAC), then packets sent to your IP will be turned from the old AP to the new one now so that it could reach you again without losing originally TCP connection.

As you can feel in our campus, the switch between networks under different AP is seamless.

So let's come to the end, does this mechanism breaks out the rule we talked above, the subnet strategy, under which we send packets directly to the peer under the same subnet while to the router when outside the subnet. If all the IPs mix up, how could we still obey that?

Here's the common shift cognition from modern people, I think. Because mostly we think the network transmission are wireless and we always mix the concept of switch and router.

If we split them up, between the router and our devices, there could be many APs/switches as the Layer 2 nodes. So we can still send packets to, let's say, central area, or the controller, where the packets with src and dst under same subnet can always go directly. And all things are ok. The router is not so necessary considering the in-campus communications.

emm... I think it's done here. Of course, there are still many things worth thinking like the cross-campus, or organizing buildings...

But I think above things have already make be grasp the core idea.