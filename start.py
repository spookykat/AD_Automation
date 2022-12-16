from info import domain

interface = input("Enter network interface. ")
output = domain.getDomainControllers(interface)

if not output[0]:
    print(output[1])
else:
    print("[+]Great Success")
