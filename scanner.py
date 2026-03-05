import scapy.all as scapy
import requests
import time

def print_banner():
    print("-" * 65)
    print("   QUESTORNET SCANNER V2.0 - BY RISADI VIDARA   ")
    print("      Future Cyber Security Consultant         ")
    print("-" * 65)

def get_vendor(mac_address):
    
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return "Unknown Device"
    except:
        return "N/A"

def scan(ip):
    print(f"[*] Scanning network: {ip}...")
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        mac = element[1].hwsrc
        #  Vendor 
        vendor = get_vendor(mac)
        client_dict = {"ip": element[1].psrc, "mac": mac, "vendor": vendor}
        clients_list.append(client_dict)
        time.sleep(1) 
    return clients_list

def display_result(results_list):
    print("\nIP Address\t\tMAC Address\t\tVendor/Brand")
    print("-" * 75)
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}\t{client['vendor']}")

if __name__ == "__main__":
    print_banner()
    target_ip = "192.168.1.1/24" 
    
    try:
        scan_result = scan(target_ip)
        display_result(scan_result)
        print("\n[+] Advanced Scan Completed.")
    except Exception as e:
        print(f"\n[!] Error: {e}")