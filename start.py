import info.domain as domain

interface = input()
output = domain.getDomainControllers(interface)

if not output[0]:
    print(output[1])
else:
    print("[+]Great Success")
