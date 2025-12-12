from scapy.all import sniff

def handle_pkt(pkt):
    # We check for the IP layer to get source and destination information
    if pkt.haslayer('IP'):
        print(f"IP: {pkt['IP'].src} -> {pkt['IP'].dst}")

# iface="en0" is typically the Wi-Fi interface on a Mac.
# count=10 tells it to stop after 10 packets.
print("Starting packet sniff (requires sudo)...")
sniff(iface="en0", count=10, prn=handle_pkt)
