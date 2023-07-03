from tools.tools import Command, load_config
import re
import glob
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor

def scanSubnet(subnet):
    arguments = load_config()['masscan']['arguments']
    scan_command = Command(f"sudo -S masscan {arguments} {subnet} -oG output/masscan_{subnet.replace('/','_')}.grep < sudo_pwd", None, None, "output", "masscan")
    scan_command.run_command()

def extract_unique_subnets(subnet_mask):
    files = glob.glob("output/masscan_*")
    
    subnets = set()
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    
    for file in files:
        with open(file, "r") as f:
            content = f.read()
        ips = ip_pattern.findall(content)
        
        for ip in ips:
            subnet = ip_network(f"{ip}/{subnet_mask}", strict=False)
            subnets.add(str(subnet))

    return list(subnets)

def ScanSubnets(subnets):
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(scanSubnet, subnets)