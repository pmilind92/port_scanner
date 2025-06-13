import pyfiglet # type: ignore
import sys
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

#name
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Defining a target
if len(sys.argv) == 2:

    # translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
elif len(sys.argv) == 1:
    # Prompt user for input if no command-line argument is provided
    target_input = input("Enter the hostname or IP address to scan: ")
    target = socket.gethostbyname(target_input)
else:
    print("Invalid amount of arguments.")
    print("Syntax: python port_scanner.py <hostname> or python port_scanner.py")
    sys.exit()

# Add Banner
print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)

def scan_port(ip_target, port_to_scan):
    """Scans a single port on the target IP."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5) # Reduced timeout for faster scanning
        result = s.connect_ex((ip_target, port_to_scan))
        if result == 0:
            return port_to_scan # Return open port number
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        pass # Port is closed or filtered
    except socket.error as e:
        print(f"Socket error on port {port_to_scan}: {e}") # Log other socket errors
    finally:
        if 's' in locals() and s: # Ensure socket is closed if it was opened
            s.close()
    return None

try:
    # Use ThreadPoolExecutor to scan ports concurrently
    # Adjust max_workers based on your system and network capabilities
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Create a list of future objects
        futures = [executor.submit(scan_port, target, port) for port in range(1, 65535)]
        for future in as_completed(futures):
            open_port = future.result()
            if open_port:
                print(f"Port {open_port} is open")
except KeyboardInterrupt:
    print("\nExitting Program !!!!")
    sys.exit()
except socket.gaierror:
    print("\nHostname Could Not Be Resolved !!!!")
    sys.exit()
except socket.error:
    print("\nServer not responding !!!!")
    sys.exit()
