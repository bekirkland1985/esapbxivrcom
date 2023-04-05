import re

from netmiko import ConnectHandler

voiceware = {
    'device_type': 'linux',
    'session_log': 'session.txt',
    'host': '192.161.xxx.xxx',
    'username': 'phonesuite',
    'password': 'xxxxxxxx',
    'port': 51002,  # optional, defaults to 22
    'verbose': True,
    'secret':'xxxxxxxx'
}

net_connect = ConnectHandler(**voiceware)

net_connect.enable(cmd="sudo -i", pattern='password')

net_connect.send_command('psql -U postgres', expect_string=re.escape('postgres=#'))

net_connect.send_command('\c asgi_cc',expect_string=re.escape('asgi_cc=#'))

output3 = net_connect.send_command("INSERT INTO devices (device_type, name, accountcode, username, secret, type, host, context, qualify, VALUES")

output = net_connect.send_command("INSERT INTO huntgroups (id, name, fail_extension, group_type, ringall_time) VALUES (20, 'Main Day', 8025, 1, 24), (21, 'Main Night', 8026, 1, 24);", expect_string=re.escape('INSERT 0 2'))

print(output)

output1 = net_connect.send_command("INSERT INTO huntgroup_devices (huntgroup_id, device_id, priority, ring_duration) VALUES \
(20, (SELECT id FROM devices WHERE username = '502'), 1, 24), \
(20, (SELECT id FROM devices WHERE username = '510'), 2, 24), \
(21, (SELECT id FROM devices WHERE username = '502'), 1, 24),\
(21, (SELECT id FROM devices WHERE username = '510'), 2, 24);", expect_string=re.escape('INSERT 0 4'))

print(output1)

output2 = net_connect.send_command("INSERT INTO extensions (number, type, dest_id, vmail_enabled, timeout, list, priority_enabled, is_guest, context_id, tries, exten_dialing, vm_busy, vm_unavail, vm_temp, emer_blocked) VALUES \
(8001, 5, 20, 'f', -1, 'f', 'f', 'f', 1, 0, 't', -1, -1, -1, 'f'), \
(8002, 5, 21, 'f', -1, 'f', 'f', 'f', 1, 0, 't', -1, -1, -1, 'f');")

print(output2)

print (net_connect.disconnect())
