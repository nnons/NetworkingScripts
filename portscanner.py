#!/usr/bin/env python2.7
import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)
def connScan(tgtHost, tgtPort):
    try:
        connSock = socket(AF_INET, SOCK_STREAM)
        connSock.connect((tgtHost, tgtPort))
        connSock.send('Hello\r\n')
        results = connSock.recv(100)
        screenLock.acquire()
        print '[+]%d/tcp open' % tgtPort
        print '[+] ' + str(results)
    except:
        screenLock.acquire()
        print '[-]%d/tcp closed' % tgtPort
    finally:
        screenLock.release()
        connSock.close()


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print "[-] Cannot resolve '%s' : Unknown host" % tgtHost
        return
    try:
        tgtName = gethostbyadr(tgtIP)
        print '\n[+] Scan Results for : ' + tgtName[0]
    except:
        print '\n[+] Scan Results for: ' + tgtIP

    setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    parser = optparse.OptionParser(usage='Usage %prog -H' + \
            ' <target host> -p <target port>')

    parser.add_option('-H', dest='tgtHost', type='string', \
            help='specify target host')

    parser.add_option('-p', dest='tgtPort', type='int', \
            help='specify target port')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')

    if (tgtHost == None) | (tgtPorts[0] == None):
        print parser.usage
        exit(0)

    portScan(tgtHost, tgtPorts)

if  __name__ == '__main__':
    main()
