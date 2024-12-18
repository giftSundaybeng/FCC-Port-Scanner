
import socket
import re
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    try:
        # Validate and resolve the target
        if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', target):  # Check if target is IP
            socket.inet_aton(target)
            ip_address = target
        else:
            ip_address = socket.gethostbyname(target)  # Resolve URL to IP

        # Scan ports in the range
        for port in range(port_range[0], port_range[1] + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Set timeout for faster scanning
                if s.connect_ex((ip_address, port)) == 0:
                    open_ports.append(port)

        # Handle verbose output
        if verbose:
            host_display = target if not target.isnumeric() else ip_address
            result = f"Open ports for {host_display} ({ip_address})\n"
            result += "PORT     SERVICE\n"
            for port in open_ports:
                service_name = ports_and_services.get(port, "unknown")
                result += f"{port:<8}{service_name}\n"
            return result.strip()

        return open_ports

    except socket.gaierror:
        return "Error: Invalid hostname"
    except OSError:
        return "Error: Invalid IP address"
