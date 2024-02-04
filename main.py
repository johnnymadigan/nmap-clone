#!/usr/bin/python3

import sys
import time
import socket
from ping3 import ping
from datetime import datetime
from progress.bar import FillingSquaresBar

print(" ____   ___   ____  ______       _____   __   ____  ____   ____     ___  ____   ")
print("|    \ /   \ |    \|      |     / ___/  /  ] /    ||    \ |    \   /  _]|    \  ")
print("|  o  )     ||  D  )      |    (   \_  /  / |  o  ||  _  ||  _  | /  [_ |  D  ) ")
print("|   _/|  O  ||    /|_|  |_|     \__  |/  /  |     ||  |  ||  |  ||    _]|    /  ")
print("|  |  |     ||    \  |  |       /  \ /   \_ |  _  ||  |  ||  |  ||   [_ |    \  ")
print("|  |  |     ||  .  \ |  |       \    \     ||  |  ||  |  ||  |  ||     ||  .  \ ")
print("|__|   \___/ |__|\_| |__|        \___|\____||__|__||__|__||__|__||_____||__|\_| ")
print("")

def is_port_open(ip: str, port: int, timeout_s: float = 0.5):
    # IPv4, TCP,
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout_s)
        is_open = False if s.connect_ex((ip, port)) else True
        return is_open







# example target = 137.74.187.102 (ping hackthissite.org) 
target_ip = input("HostIP: ")
# TODO: accept range OR specific ports OR all ports (1, 65535)
min_port = int(input("Min port: "))
max_port = int(input("Max port: "))
# TODO: support for full site name (ASCII) or IP format
# TODO: regex for the IPv4
print(f"Scan for '{target_ip}' started at {datetime.now().strftime("%H:%M")}")








# PING HOST
ping_res = ping(target_ip)
is_target_up = ping_res is not None and ping_res is not False

if (is_target_up):
    print(f"Host is up ({round(ping_res, 2)}s latency)")
else:
    print("Host offline")
    sys.exit()





# SCAN PORTS
scan_res: list[str] = []
num_total_ports = abs(min_port - (max_port + 1))
bar = FillingSquaresBar("Scanning", max=num_total_ports)

try:
    # Scan every port on the target ip
    for port in range(min_port, (max_port + 1)):
        if (is_port_open(target_ip, port)):
            scan_res.append(f"{port}/tcp\topen")

        bar.next()

except socket.error:
    print(f"Lost connection to {target_ip}")

finally:
    bar.finish()

    if (len(scan_res) == 0):
        print("No open ports")
    else:
        for res in scan_res:
            print(res)

    print(f"Scan for '{target_ip}' finished at {datetime.now().strftime("%H:%M %p")}")





# PORT    STATE SERVICE
# 443/tcp open  https




