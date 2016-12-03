import optparse
from scapy.all import *

"""
q=              query
pq=             previous query
hl=             language
as_epq=         phrase
as_filetype=    file format
as_sitesearch=  specific site restriction
"""

def getGSS(pkt):
    if pkt.haslayer(Raw):
        payload = pkt.getlayer(Raw).load
        if 'GET' in payload and 'google' in payload:
            result = re.findall(r'(?i)\&q=(.*?)\&', payload)
            if result:
                search_str = result[0].split('&')[0]
                search_str = search_str.replace('q=', '').replace('+', ' ').replace('%20', ' ')
                print('Search query: ' + search_str)

def main():
    parser = optparse.OptionParser('usage %prog -i ' + '<interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print(parser.usage)
        exit(0)
    else:
        conf.interface = options.interface
    try:
        print('Initiating Search Sniffer...')
        sniff(filter='tcp port 80', prn=getGSS)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()