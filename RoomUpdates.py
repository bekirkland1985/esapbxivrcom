import csv
import re
import sys
import netmiko
from netmiko import *
from ttp import ttp

with open('bennigan.csv', newline='\n') as csvfile:
    filearrayread = []
    filereader = csv.reader(csvfile, delimiter=",")
    for row in filereader:
        filearrayread.append(row)

voiceware = {
    'device_type': 'linux',
    'session_log': 'session3.txt',
    'host': '192.161.130.117',
    'username': 'phonesuite',
    'password': 'a63TV42c!',
    'port': 51002,  # optional, defaults to 22
    'verbose': True,
    'secret': 'a63TV42c!'
}
print(netmiko.__version__)

net_connect = ConnectHandler(**voiceware)

net_connect.enable(cmd="sudo -i", pattern='password')

printPrompt = net_connect.find_prompt()

print(printPrompt)

net_connect.send_command('psql -U postgres', expect_string=re.escape('postgres=#'))

printPrompt = net_connect.find_prompt()

print(printPrompt)

net_connect.send_command("\c asgi_cc",expect_string=re.escape("asgi_cc=#"))

printPrompt = net_connect.find_prompt()

print(printPrompt)



output = net_connect.send_command("SELECT number,dest_id FROM extensions; ")

data_to_parse = output

ttp_template = """
{{line | _line_}}
"""

parser = ttp(data=data_to_parse, template=ttp_template)

parser.parse()

results = parser.result(format='table')
extensionarray = {}
for element in results[0]:
    elementString = str(element[0])
    if (elementString[1] != (" ")) and (elementString[1].isnumeric() ):
        splitString = elementString.rsplit('|')
        extensionarray.update({(str(splitString[0].strip())):(str(splitString[-1].strip()))})


with open('failureReport.txt', 'w') as failureReport:
    sys.stdout = failureReport
    idNum = 0
    for x in filearrayread:
        if filearrayread[idNum][0] in extensionarray:
            sheppard = filearrayread[idNum][1]
            gladiator = extensionarray[filearrayread[idNum][0]]
            net_connect.send_command(f"UPDATE extensions SET exten_dialing='f' WHERE number='{filearrayread[idNum][0]}';")
            net_connect.send_command(f"INSERT INTO extensions (number, type, dest_id, vmail_enabled, timeout, list, priority_enabled, is_guest, context_id, tries, exten_dialing, vm_busy, vm_unavail, vm_temp, emer_blocked) VALUES ({sheppard}, 330, {gladiator}, 'f', -1, 'f', 'f', 'f', 1, 0, 't', -1, -1, -1, 'f');")
        if filearrayread[idNum][0] not in extensionarray:
            print(f"Extension {filearrayread[idNum][0]} not found in database, no extension for {sheppard} created.")
        idNum = idNum + 1

    print("Command Successful")

    net_connect.disconnect()

    print('Finished Command!')