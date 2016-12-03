from scapy.all import *
import optparse

def ftpSniff(pkt):
    dest = pkt.getlayer(IP).dst
    raw = pkt.sprintf('%Raw.load%')
    user = re.findall('(?i)USER (.*)', raw)
    passwd = re.findall('(?i)USER (.*)', raw)

    if user:
        print('Detected ftp login to: ' + str(dest))
        print('User account: ' + str(user[0]))
    elif passwd:
        print('Password: ' + str(passwd[0]))

def main():
    parser = optparse.OptionParser('usage %prog ' + '-i<interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print(parser.usage)
        exit(0)
    else:
        conf.iface = options.interface