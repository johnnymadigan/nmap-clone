import socket

def dns_resolve_host(target: str):
    """
    Attempt to DNS resolve the IP, returning the IP or None
    """
    try:
        return socket.gethostbyname(target)
    except:
        return None

def is_port_open(ip: str, port: int, timeout_s: float = 0.5):
    """
    Checks if a port is open on a target host using IPv4 and TCP
    """
    if not is_port_in_range(port):
        return False
    
    # AF_INET = IPv4, AF_INET6 = IPv6, AF_BLUETOOTH = Bluetooth, ...
    # SOCK_STREAM = TCP, SOCK_DGRAM = UDP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout_s)
        is_open = False if s.connect_ex((ip, port)) else True
        return is_open

def is_port_in_range(port: int):
    """
    Checks if a port is in the network protocol port range
    """
    return 0 <= port <= 65353

def is_valid_ipv4(target: str | None):
    """
    Checks if an IP is in a valid format
    """
    try:
        if not target:
            return
        
        socket.inet_aton(target)
        return True
    except:
        return False
