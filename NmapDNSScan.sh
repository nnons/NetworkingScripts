#!/bin/bash

# Variables

IP=$1
PORT=$2

if
    [[ -z "$1" ]]; then
    echo "Please enter an IP : "
    exit 0
elif [[ -z "$2" ]]; then
    echo "Please enter a port number : "
    exit 0
fi

pingSweep() {
    echo "\n[+] Running ping sweep"
    echo "======================="
    nmap -sn "$IP"/24 > pingSweep.txt
}

# SMTP Servers
snmpServerInfo() {
    echo "\n[+] Starting SNMP Server Enumeration"
    echo "===================================="
    echo "[+] Running "
    echo "Checking SMTP Commands ... "
    nmap --script smtp-commands "$IP" -p "$PORT"
}
# SMB Servers / Samba

smbServerInfo() {
    echo "\n[+] Starting SMB Server Enumeration"
    echo "===================================="
    echo "[+] Running "
    echo "[+] enum4linux"
    enum4linux -r "$IP" > enumForLinux.txt
    echo "Looking at SMB Permissions ... "
    smbmap -H "$IP" > smbPermissions.txt
    echo "Enumerating Linux Shares ... "
    nmap --script smb-enum-shares "$IP" -p"$PORT" > shareEnumeration.txt
    echo "SMB OS Discovery ... "
    nmap --script smb-os-discovery "$IP" -p 445
    echo "Enumerating NFS Shares ... "
    nmap --script nfs-ls "$IP"
}

quietPingSweep() {
    echo "[+] Running "
    echo "[+] Quiet ping sweep running "
    echo "============================="
    nmap -sn -PN "$IP"/24 > quietPingScan.txt
}

osScan() {
    echo "[+] Running "
    echo "OS Scan and guessing... "
    echo "========================="
    nmap -sT -sV -O --osscan-guess "$IP"/24 > osScan.txt
}

dnsLookup() {
    echo "\n[+] DNS Lookup with wordlist fierce"
    echo "===================================="
    echo "Enter domain name : "
    read domainName
    for name in $(cat /etc/fierce/hosts.txt); do
        host $name."$domainName".com "$IP" -W 2; done | grep 'has address' > forwardDNSLookup
}

reverseDNSLookup() {
    echo "\n[+] Reverse DNS Lookup"
    echo "======================="
    echo "Enter domain name : "
    read domainName
}

vulnerabilityScan() {
    echo "\n[+] Running Vulnerability Scan ... "
    nmap --script +vuln
}
main() {
    while read command args
    do
        echo "What test do you want to run? "
        echo "1) Full SMB Enumeration"
        echo "2) SMTP Enuemration"
        echo "3) Basic Ping Sweep "
        echo "4) Quiet Ping Sweep"
        echo "5) OS Scan"
        echo "6) Forward DNS Lookup"
        echo "7) Reverse DNS Lookup"
        case $command
        in
            quit|exit) exit 0;;
            1) smbServerInfo ;;
            2) snmpServerInfo;;
            3) pingSweep     ;;
            4) quietPingSweep;;
            5) osScan        ;;
            6) forwardDNSLookup;;
            7) reverseDNSLookup;;
            *)
        esac
    done
}

main ""
