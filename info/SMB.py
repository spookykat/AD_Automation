import subprocess
def GetSigningDisabled(subnet:str, subnetmask:str):
    file_name = f'relay-{subnet}.txt'
    subnet_complete = f"{subnet}/{subnetmask}"
    subprocess.run(['crackmapexec', 'smb', subnet_complete, '--gen-relay-list', file_name],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return file_name