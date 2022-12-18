from info import domain, SMB

interface = input("Enter network interface. (eg. eth0) ")
subnet_unparsed = input("Enter subnet. (eg. 192.168.0.0/24)  ")

subnet = subnet_unparsed.split('/')[0]
subnetmask = subnet_unparsed.split('/')[1]

print(subnet)
print(subnetmask)
output = domain.getDomainControllers(interface)

if not output[0]:
    print(output[1])
else:
    print("[+]Great Success, Found Domain Controller(s)")
