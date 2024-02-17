#!/usr/bin/python3

import sys
import socket
from ping3 import ping
from constants import port_services
from datetime import datetime
from progress.bar import FillingSquaresBar
from utils import is_port_in_range, is_port_open, is_valid_ipv4, dns_resolve_host
                                                        
def main():
    """
    NMAP CLONE
    Example host address: 137.74.187.102 (ping hackthissite.org)
    """

    # Font: Crawford2
    print("")
    print(" ____   ___ ___   ____  ____          __  _       ___   ____     ___ ")
    print("|    \ |   |   | /    ||    \        /  ]| |     /   \ |    \   /  _]")
    print("|  _  || _   _ ||  o  ||  o  )      /  / | |    |     ||  _  | /  [_ ")
    print("|  |  ||  \_/  ||     ||   _/      /  /  | |___ |  O  ||  |  ||    _]")
    print("|  |  ||   |   ||  _  ||  |       /   \_ |     ||     ||  |  ||   [_ ")
    print("|  |  ||   |   ||  |  ||  |       \     ||     ||     ||  |  ||     |")
    print("|__|__||___|___||__|__||__|        \____||_____| \___/ |__|__||_____|")
    print("                                                     by Johnny Madigan")


    target = ""

    while not is_valid_ipv4(target):
        target = input("Host address: ")
        
        if is_valid_ipv4(target):
            break

        resolved_ip = dns_resolve_host(target)
        if is_valid_ipv4(resolved_ip):
            print(f"Resolved {target} -> {resolved_ip}")
            target = resolved_ip
            break

        print("Invalid host address, please try again")
        target = ""

    print("Please specify port range to scan")

    min_port = -1

    while not is_port_in_range(min_port):
        min_port = int(input("Min port: "))
        if not is_port_in_range(min_port):
            print("Port out of scope (0-65353), please try again")

    max_port = -1

    while max_port <= min_port or not is_port_in_range(min_port):
        max_port = int(input("Max port: "))
        if max_port <= min_port:
            print("Port must be greater than min port, please try again")
        elif not is_port_in_range(max_port):
            print("Port out of scope (0-65353), please try again")

    print(f"Scan for '{target}' started at {datetime.now().strftime("%H:%M")}")

    # PING HOST
    ping_res = ping(target)
    is_target_up = ping_res is not None and ping_res is not False

    if (is_target_up):
        print(f"Host is up ({round(ping_res, 2)}s latency)")
    else:
        print("Host offline")
        sys.exit()

    # SCAN PORTS
    print("")
    num_total_ports = abs(min_port - (max_port + 1))
    bar = FillingSquaresBar("Scanning", max=num_total_ports)
    open_ports: list[int] = []

    try:
        for port in range(min_port, (max_port + 1)):
            if (is_port_open(target, port)):
                open_ports.append(port)

            bar.next()

    except socket.error:
        print(f"Lost connection to {target}")

    # PRINT REPORT
    finally:
        bar.finish()

        if (len(open_ports) == 0):
            print("\nNo open ports")
        else:
            open_ports_w_desc: list[str] = [f"{port}/tcp".ljust(10) + "open".ljust(10) + f"{port_services[port] if port_services.get(port) else '-'}" for port in open_ports]
            print("\nPORT".ljust(10) + "STATE".ljust(10) + "SERVICE GUESS 🪪")
            print('\n'.join(open_ports_w_desc))

        print(f"\nScan for '{target}' finished at {datetime.now().strftime("%H:%M %p")}\n")

if __name__ == "__main__":
    main()
