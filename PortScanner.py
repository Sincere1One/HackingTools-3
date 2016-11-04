import optparse
from socket import *
from threading import *

screen_lock = Semaphore(value=1)

def connection_scan(target_host, target_port):
    try:
        connection_socket = socket(AF_INET, SOCK_STREAM)
        connection_socket.connect((target_host, target_port))
        connection_socket.send('Port Scanner\r\n')
        results = connection_socket.recv(100)
        screen_lock.acquire()
        print('%d/tcp open' % target_port)
        print(str(results))
    except:
        screen_lock.acquire()
        print('%d/tcp closed' % target_port)
    finally:
        screen_lock.release()
        connection_socket.close()

def port_scan(target_host, target_ports):
    try:
        target_IP = gethostbyname(target_host)
    except:
        print("Cannot resolve '%s': Unknown host" % target_host)
        return
    try:
        target_name = gethostbyaddr(target_IP)
        print('\nScan Results for: ' + target_name[0])
    except:
        print('\nScan Results for: ' + target_IP)
    setdefaulttimeout(1)

    for x in target_ports:
        t = Thread(target=connection_scan, args=(target_host, int(x)))
        t.start()

def main():
    parser = optparse.OptionParser('usage%prog ' + '-H <target host> -p <target port>')
    parser.add_option('-H', dest='target_host', type='string', help='specify target host')
    parser.add_option('-p', dest='target_port', type='string', help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    target_host = options.target_host
    target_ports = str(options.target_port).split(', ')

    if target_host == None or target_ports[0] == None:
        print(parser.usage)
        exit(0)
    port_scan(target_host, target_ports)

if __name__=="__main__":
    main()