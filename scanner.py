import scapy.all as scapy
import requests
import socket
import time

def print_banner():
    print("-" * 75)
    print("   QUESTORNET SCANNER V3.0 (PRO) - BY RISADI VIDARA   ")
    print("      Future Cyber Security Consultant | Port Scanner Enabled         ")
    print("-" * 75)

def get_vendor(mac_address):
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.text
        return "Unknown Device"
    except:
        return "N/A"

def scan_ports(ip):
    # බහුලවම පාවිච්චි වන ports කිහිපයක් පරීක්ෂා කරමු
    common_ports = [21, 22, 80, 443, 8080]
    open_ports = []
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1) # වේගවත් scan කිරීමක් සඳහා
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(str(port))
            sock.close()
        except:
            pass
    return ", ".join(open_ports) if open_ports else "None Detected"

def scan(ip):
    print(f"[*] Scanning network: {ip}...")
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        mac = element[1].hwsrc
        ip_address = element[1].psrc
        
        # Vendor හොයමු
        vendor = get_vendor(mac)
        
        # Open Ports 
        print(f"[*] Auditing ports for {ip_address}...")
        ports = scan_ports(ip_address)
        
        client_dict = {"ip": ip_address, "mac": mac, "vendor": vendor, "ports": ports}
        clients_list.append(client_dict)
        time.sleep(0.5)
    return clients_list

def display_result(results_list):
    print("\nIP Address\t\tMAC Address\t\tVendor\t\t\tOpen Ports")
    print("-" * 95)
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}\t{client['vendor'][:20]}\t\t{client['ports']}")

if __name__ == "__main__":
    print_banner()
    target_ip = "192.168.1.1/24" 
    
    try:
        scan_result = scan(target_ip)
        display_result(scan_result)
        print("\n[+] Comprehensive Security Audit Completed.")
    except Exception as e:
        print(f"\n[!] Error: {e}")
