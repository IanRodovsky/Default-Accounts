# Requires paramiko package

import socket
import telnetlib
import paramiko


def ssh_login(host, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        ssh_session = ssh.get_transport().open_session()
        if ssh_session.active:
            print(f'SSH login successful on {host}:{port} with username "{username}" and password "{password}"')
    except socket.error:
        print(f'Login failed with username "{username}" and password "{password}"')
        return
    else:
        ssh.close()


def telnet_login(host, port, username, password):
    user = bytes(f'{username}\n', 'utf-8')
    pass_ = bytes(f'{password}\n', 'utf-8')
    try:
        telnet = telnetlib.Telnet(host, port)
        telnet.read_until(bytes('Login: ', 'utf-8'))
        telnet.write(user)
        telnet.read_until(bytes('Password: ', 'utf-8'))
        telnet.write(pass_)
        result = telnet.expect([bytes('Last login', 'utf-8')], timeout=2)
        if result[0] >= 0:
            print(f'telnet login successful on {host}:{port} with username "{username}" and password "{password}"')
        telnet.close()
    except EOFError:
        print(f'Login failed with username "{username}" and password "{password}" ')
    except ConnectionRefusedError:
        print('Telnet connection refused.')


host = '127.0.0.1'
with open('defaults.txt', 'r') as file:
    for line in file:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        ssh_login(host, 22, username, password)
        telnet_login(host, 23, username, password)
