 QuestorNet Scanner V2.0

A high-performance Network Reconnaissance tool designed for automated device discovery and hardware vendor identification within a local subnet.

Developed by:Risadi Vidara (Cyber Security Student)



 🚀 Key Features
ARP Network Mapping: Scans the local network efficiently using Address Resolution Protocol.
Real-time Device Discovery: Detects active IP and MAC addresses of all connected devices.
API-Powered Vendor Lookup: Automatically identifies device brands (Apple, Samsung, Tenda, etc.) via MacVendors API integration.
Professional CLI UI: Clean, tabular output designed for security audits.

---

💻 Tech Stack
Language: Python 3
Main Library: Scapy (for packet manipulation)
API Handling: Requests
Target OS: Windows (Requires Npcap)

---

⚙️ How to Run
1. Ensure Npcap is installed on your Windows machine.
2. Install dependencies: `pip install scapy requests`.
3. Run VS Code as Administrator.
4. Execute: `python scanner.py`
