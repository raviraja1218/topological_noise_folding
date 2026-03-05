#!/usr/bin/env python
"""
Network connectivity test for IBM Quantum
"""

import socket
import subprocess
import sys

def test_dns(hostname):
    """Test DNS resolution"""
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS resolved: {hostname} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS failed: {e}")
        return False

def test_ping(hostname):
    """Test ping connectivity"""
    try:
        result = subprocess.run(
            ["ping", "-c", "2", hostname],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Ping successful")
            return True
        else:
            print(f"❌ Ping failed")
            return False
    except Exception as e:
        print(f"❌ Ping error: {e}")
        return False

def test_curl(hostname):
    """Test HTTP connectivity"""
    try:
        import urllib.request
        response = urllib.request.urlopen(f"https://{hostname}", timeout=5)
        print(f"✅ HTTP connected: {response.status}")
        return True
    except Exception as e:
        print(f"❌ HTTP failed: {e}")
        return False

print("="*60)
print("🌐 NETWORK CONNECTIVITY TEST")
print("="*60)

hosts = [
    "auth.quantum-computing.ibm.com",
    "api.quantum-computing.ibm.com",
    "quantum-computing.ibm.com",
    "google.com"
]

for host in hosts:
    print(f"\n📡 Testing: {host}")
    test_dns(host)
    if host != "google.com":  # Skip ping for IBM (may be blocked)
        pass
    else:
        test_ping(host)

print("\n" + "="*60)
print("DNS Configuration:")
print("-"*60)
with open("/etc/resolv.conf", "r") as f:
    print(f.read())

print("\nNetwork Interfaces:")
subprocess.run(["ip", "addr", "show"])

print("\n✅ Network test complete")
