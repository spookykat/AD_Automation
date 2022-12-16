import subprocess
import re
def getDomainControllers(interface):

    # run the nmcli command with the specified interface

    output = subprocess.run(['ifconfig'], capture_output=True).stdout.decode('utf-8')
    if interface not in output:
        return 0, "Interface doesn't exist"

    output = subprocess.run(['nmcli', 'dev', 'show', interface], capture_output=True).stdout.decode('utf-8')

    # use a regular expression to extract the DNS , DOMAINS
    domain_controller_regex = r'_ldap\.\_tcp\.dc\.\_msdcs\.[^\s]*\s+service\s*=\s*[^\s]*\s+[^\s]*\s+[^\s]*\s+([^\s]*)'
    dns_ip_regex = r'IP4\.DNS\[\d+\]:\s+(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)'
    dns_ips = re.findall(dns_ip_regex, output)

    domain_regex = r'IP4\.DOMAIN\[\d+\]:\s+(\S+)'
    domains = re.findall(domain_regex, output)

    searches_regex = r'IP4\.SEARCHES\[\d+\]:\s+(\S+)'
    searches = re.findall(searches_regex, output)

    domaincontrollers_unparsed = ''
    processes = []
    # remove the prefix from the DNS IPs and print the IPs
    if dns_ips and (searches or domains):
        print(searches)
        for dns_ip in dns_ips:
            dns_ip_parsed = re.sub(r'IP4\.DNS\[\d+\]:\s+', '', dns_ip)
            for domain in domains:
                domain_parsed = re.sub(r'IP4\.DOMAIN\[\d+\]:\s+', '', domain)
                print(domain_parsed)
                p = subprocess.Popen(['nslookup', '-type=SRV', '_ldap._tcp.dc._msdcs.' + domain_parsed, dns_ip_parsed], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                processes.append(p)
                
            for search in searches:
                print(search)
                searches_parsed = re.sub(r'IP4\.SEARCHES\[\d+\]:\s+', '', search)
                p = subprocess.Popen(['nslookup', '-type=SRV', '_ldap._tcp.dc._msdcs.' + searches_parsed, dns_ip_parsed], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                processes.append(p)
    else:
        return 0, "No domain controller found."

    for p in processes:
        stdout, stderr = p.communicate()
        domaincontrollers_unparsed += stdout.decode('utf-8')
    print(domaincontrollers_unparsed)

    domain_controllers = re.findall(domain_controller_regex, domaincontrollers_unparsed)
    processes = []
    for domain_controller in domain_controllers:
        domain_controller_ip = subprocess.run(['dig', '+short',domain_controller[:-1]], capture_output=True).stdout.decode('utf-8')
        with open('DCs.txt', 'a') as f:
            f.write(domain_controller[:-1] + " " + domain_controller_ip + '\n')
        

    return 1