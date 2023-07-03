from info import domain, SMB
from tools import tools,nmap, masscan
import threading
import time

#interface = input("Enter network interface. (eg. eth0) ")
#subnet_unparsed = input("Enter subnet. (eg. 192.168.0.0/24)  ")
#
#subnet = subnet_unparsed.split('/')[0]
#subnetmask = subnet_unparsed.split('/')[1]
#
#print(subnet)
#print(subnetmask)
#'''output = domain.getDomainControllers(interface)
#
#if not output[0]:
#    print(output[1])
#else:
#    print("[+]Great Success, Found Domain Controller(s)")'''
#
#SMB_class = SMB.SMB(['192.168.56.11'], 'vagrant', 'vagrant')
#
#signingthread = threading.Thread(target=SMB.SMB.GetSigningDisabled,args=[subnet,subnetmask])
#spraythread = threading.Thread(target=SMB_class.SprayUserIsPass)
#passpolthread = threading.Thread(target=SMB_class.GetPassPol)
#
#signingthread.start()
#spraythread.start()
#passpolthread.start()
#
#
#signingthread.join()
#spraythread.join()
#passpolthread.join()

print(tools.load_config())


subnets = []
if(tools.load_config()['masscan']['enabled']):
    #masscan.scanSubnets(tools.load_config()['masscan']['targets'])
    subnets += masscan.extract_unique_subnets(24)

if(tools.load_config()['nmap']['enabled']):
    subnets += tools.load_config()['nmap']['targets']
    uniquesubnets = list(set(subnets))
    nmap.ScanSubnets(uniquesubnets)
    nmap.NMAPsToHTML()