import socket
import requests

# Force IP resolution manually
# First, find the actual IP (run this on a working network)
IBM_IP = "169.63.140.180"  # Example IP - you need the actual one

# Or use a different endpoint
url = "https://api.quantum-computing.ibm.com/api/version"

try:
    # Try with custom DNS
    import dns.resolver
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    answers = resolver.resolve('auth.quantum-computing.ibm.com', 'A')
    ip = str(answers[0])
    print(f"Resolved with Google DNS: {ip}")
except:
    print("DNS resolution failed")
