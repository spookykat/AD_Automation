from tools.tools import Command, load_config
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
import glob
import os

def NMAPscan(subnet):
    arguments = load_config()['nmap']['arguments']
    filename = f"nmap_{subnet.replace('/','_')}.xml"
    scan_command = Command(f"nmap {arguments} {subnet} -oX output/{filename}", None, None, "output/nmap", f"nmap_{subnet.replace('/','_')}")
    scan_command.run_command()

def ScanSubnets(subnets):
    with ThreadPoolExecutor(max_workers=load_config()['nmap']['threads']) as executor:
        executor.map(NMAPscan, subnets)

def NMAPsToHTML():
    nmap_files = glob.glob(f'output/nmap_*.xml')
    
    root = None
    for file in nmap_files:
        tree = etree.parse(file)
        if root is None:
            root = tree.getroot()
        else:
            for child in tree.getroot():
                root.append(child)
    
    combined_xml_file = 'combined.xml'
    with open(combined_xml_file, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8", doctype='<!DOCTYPE nmaprun>'))


    # Convert the combined XML file to an HTML file
    convertcommand = Command(f"xsltproc -o output/nmap_report.html /usr/share/nmap/nmap.xsl {combined_xml_file}", None, None, "output/nmap", f"nmap_to_xml")
    convertcommand.run_command()
    # Delete the combined XML file
    os.remove(combined_xml_file)