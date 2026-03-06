import scapy.all as scapy
import requests
import socket
import csv
import time

def print_banner():
    print("-" * 95)
    print("   QUESTORNET SCANNER V3.1 (AUDITOR) - BY RISADI VIDARA   ")
    print("      Future Cyber Security Consultant | CSV Reporting & OS Guessing Enabled         ")
    print("-" * 95)

def get_vendor(mac_address):
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.text
        return "Unknown Device"
    except:
        return "N/A"

def guess_os(ip):
    # TTL (Time To Live) අගය පාවිච්චි කරලා OS එක අනුමාන කිරීම
    try:
        pkt = scapy.sr1(scapy.IP(dst=ip)/scapy.ICMP(), timeout=1, verbose=False)
        if pkt:
            ttl = pkt.ttl
            if ttl <= 64:
                return "Linux/Android"
            elif ttl <= 128:
                return "Windows"
            else:
                return f"Unknown (TTL:{ttl})"
        return "Detection Failed"
    except:
        return "N/A"

def scan_ports(ip):
    common_ports = [21, 22, 80, 443, 8080, 3389]
    open_ports = []
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(str(port))
            sock.close()
        except:
            pass
    return ", ".join(open_ports) if open_ports else "None"

def export_to_csv(results_list):
    filename = "network_audit_report.csv"
    if not results_list:
        return
    keys = results_list[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results_list)
    print(f"\n[+] Professional Audit Report saved as: {filename}")

def scan(ip):
    print(f"[*] Starting Network Discovery: {ip}...")
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        ip_addr = element[1].psrc
        mac_addr = element[1].hwsrc
        
        print(f"[*] Auditing {ip_addr}...")
        vendor = get_vendor(mac_addr)
        ports = scan_ports(ip_addr)
        os_type = guess_os(ip_addr)
        
        client_dict = {
            "IP Address": ip_addr, 
            "MAC Address": mac_addr, 
            "Vendor": vendor, 
            "OS Type": os_type,
            "Open Ports": ports
        }
        clients_list.append(client_dict)
        time.sleep(0.5)
    return clients_list

def display_result(results_list):
    print("\nIP Address\t\tMAC Address\t\tVendor\t\t\tOS Type\t\tPorts")
    print("-" * 110)
    for client in results_list:
        print(f"{client['IP Address']}\t{client['MAC Address']}\t{client['Vendor'][:15]}\t\t{client['OS Type']}\t{client['Open Ports']}")

if __name__ == "__main__":
    print_banner()
    # ඔබගේ Default Gateway එක අනුව මෙය වෙනස් කරන්න (ipconfig මඟින් බලන්න)
    target_ip = "192.168.1.1/24" 
    
    try:
        scan_result = scan(target_ip)
        display_result(scan_result)
        export_to_csv(scan_result)
        print("\n[+] Scan Completed Successfully.")
    except Exception as e:
        print(f"\n[!] Error: {e}")