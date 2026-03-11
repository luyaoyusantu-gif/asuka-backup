import socket
import concurrent.futures
import time
import sys

TARGET = "192.168.31.1" # Default gateway (Router)
PORTS = [21, 22, 23, 53, 80, 135, 139, 443, 445, 1900, 3389, 5000, 8080, 8443] # Common ports

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((TARGET, port))
        if result == 0:
            return port, True
        return port, False
    except Exception as e:
        return port, False
    finally:
        sock.close()

if __name__ == "__main__":
    print(f"[*] Starting 'Asuka Mini-Scanner' against target {TARGET}...")
    start_time = time.time()
    
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scan_port, port): port for port in PORTS}
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                print(f"[+] Port {port} is OPEN")
                open_ports.append(port)
                
    end_time = time.time()
    print(f"\n[*] Scan completed in {end_time - start_time:.2f} seconds.")
    print(f"[*] Total open ports found: {len(open_ports)}")
    if len(open_ports) > 0:
        print(f"[*] Open ports list: {open_ports}")
    else:
        print("[*] No common open ports found. The device seems secure or is ignoring pings.")
